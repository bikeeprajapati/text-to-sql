const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8000";
const TOKEN_KEY = "access_token";

// ---- Types: these mirror the backend's response shapes ----

export type QueryStatus = "clarification_needed" | "executed" | "failed";

export interface ClarificationQuestion {
    question: string;
    options: string[] | null;
}

export interface ChatResponse {
    session_id: string;
    status: QueryStatus;
    message: string;
    clarification: ClarificationQuestion | null;
    generated_sql: string | null;
    result: Record<string, unknown>[] | null;
}

export interface HistoryItem {
    id: string;
    session_id: string;
    question: string;
    generated_sql: string | null;
    status: QueryStatus;
    created_at: string;
}

export interface HistoryResponse {
    items: HistoryItem[];
    total: number;
}

interface TokenResponse {
    access_token: string;
    token_type: string;
}

export class ApiError extends Error {
    status: number;

    constructor(status: number, message: string) {
        super(message);
        this.status = status;
    }
}

// ---- Token storage (localStorage only exists in the browser) ----

export function getToken(): string | null {
    if (typeof window === "undefined") return null;
    try {
        return window.localStorage.getItem(TOKEN_KEY);
    } catch {
        return null;
    }
}

function setToken(token: string): void {
    try {
        window.localStorage.setItem(TOKEN_KEY, token);
    } catch {
        // Storage can be blocked (e.g. private browsing); the user just won't stay logged in
    }
}

export function clearToken(): void {
    try {
        window.localStorage.removeItem(TOKEN_KEY);
    } catch {
        // ignore
    }
}

// ---- Core request helper ----

async function readErrorMessage(response: Response): Promise<string> {
    try {
        const body = await response.json();
        const detail = body?.detail;

        if (typeof detail === "string") return detail;

        // FastAPI validation errors (422) arrive as a list of {msg: ...}
        if (Array.isArray(detail) && detail.length > 0) {
            return detail
                .map((item: { msg?: string }) => (item.msg ?? "Invalid input").replace(/^Value error, /, ""))
                .join("; ");
        }
    } catch {
        // body wasn't JSON
    }
    return `Request failed (${response.status})`;
}

async function request<T>(
    path: string,
    options: { method?: string; body?: unknown; auth?: boolean } = {}
): Promise<T> {
    const { method = "GET", body, auth = true } = options;

    const headers: Record<string, string> = {};
    if (body !== undefined) headers["Content-Type"] = "application/json";
    if (auth) {
        const token = getToken();
        if (token) headers["Authorization"] = `Bearer ${token}`;
    }

    let response: Response;
    try {
        response = await fetch(`${API_URL}${path}`, {
            method,
            headers,
            body: body !== undefined ? JSON.stringify(body) : undefined,
        });
    } catch {
        throw new ApiError(0, "Can't reach the server. Is the backend running?");
    }

    if (!response.ok) {
        // An expired or invalid token: forget it so the UI sends the user back to sign in
        if (response.status === 401 && auth) clearToken();
        throw new ApiError(response.status, await readErrorMessage(response));
    }

    return (await response.json()) as T;
}

// ---- Public API ----

export async function register(email: string, password: string): Promise<void> {
    const token = await request<TokenResponse>("/api/auth/register", {
        method: "POST",
        body: { email, password },
        auth: false,
    });
    setToken(token.access_token);
}

export async function login(email: string, password: string): Promise<void> {
    const token = await request<TokenResponse>("/api/auth/login", {
        method: "POST",
        body: { email, password },
        auth: false,
    });
    setToken(token.access_token);
}

export function logout(): void {
    clearToken();
}

export function sendMessage(message: string, sessionId: string | null): Promise<ChatResponse> {
    return request<ChatResponse>("/api/chat", {
        method: "POST",
        body: { session_id: sessionId, message },
    });
}

export function getHistory(sessionId: string): Promise<HistoryResponse> {
    return request<HistoryResponse>(`/api/history?session_id=${encodeURIComponent(sessionId)}`);
}