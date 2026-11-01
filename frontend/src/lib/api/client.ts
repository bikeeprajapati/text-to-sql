import { API_URL } from "@/config/env";
import { clearToken, getToken } from "@/lib/auth/token";

export class ApiError extends Error {
    readonly status: number;

    constructor(status: number, message: string) {
        super(message);
        this.name = "ApiError";
        this.status = status;
    }
}

interface RequestOptions {
    method?: "GET" | "POST" | "PUT" | "PATCH" | "DELETE";
    body?: unknown;
    /** Attach the stored bearer token. Defaults to true. */
    auth?: boolean;
}

async function readErrorMessage(response: Response): Promise<string> {
    try {
        const body: unknown = await response.json();
        const detail = (body as { detail?: unknown })?.detail;

        if (typeof detail === "string") return detail;

        // FastAPI validation errors (422) arrive as a list of { msg: "..." }
        if (Array.isArray(detail) && detail.length > 0) {
            return detail
                .map((item) => {
                    const message = (item as { msg?: unknown })?.msg;
                    return typeof message === "string" ? message.replace(/^Value error, /, "") : "Invalid input";
                })
                .join("; ");
        }
    } catch {
        // The body wasn't JSON
    }
    return `Request failed (${response.status})`;
}

export async function request<T>(path: string, options: RequestOptions = {}): Promise<T> {
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