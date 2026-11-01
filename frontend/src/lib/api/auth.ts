import type { TokenResponse } from "@/types/api";
import { clearToken, setToken } from "@/lib/auth/token";
import { request } from "@/lib/api/client";

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