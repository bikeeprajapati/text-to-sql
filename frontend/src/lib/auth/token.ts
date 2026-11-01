const TOKEN_KEY = "access_token";

// localStorage only exists in the browser, and access to it can be blocked
// (e.g. private browsing), so every call is guarded.

export function getToken(): string | null {
    if (typeof window === "undefined") return null;
    try {
        return window.localStorage.getItem(TOKEN_KEY);
    } catch {
        return null;
    }
}

export function setToken(token: string): void {
    try {
        window.localStorage.setItem(TOKEN_KEY, token);
    } catch {
        // The user just won't stay signed in after a reload
    }
}

export function clearToken(): void {
    try {
        window.localStorage.removeItem(TOKEN_KEY);
    } catch {
        // Nothing to clear
    }
}