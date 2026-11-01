"use client";

import { useEffect, useSyncExternalStore } from "react";
import { useRouter } from "next/navigation";
import { ROUTES } from "@/constants/routes";
import { getToken } from "@/lib/auth/token";

type AuthState = "unknown" | "signed-in" | "signed-out";

function subscribe(onChange: () => void) {
    // Fires when the token changes in another tab (e.g. signing out there)
    window.addEventListener("storage", onChange);
    return () => window.removeEventListener("storage", onChange);
}

export function useAuthState(): AuthState {
    return useSyncExternalStore<AuthState>(
        subscribe,
        () => (getToken() ? "signed-in" : "signed-out"),
        // On the server and during hydration we can't know yet
        () => "unknown"
    );
}

/** For protected pages: redirects to sign in when there's no token. Returns true once signed in. */
export function useRequireAuth(): boolean {
    const router = useRouter();
    const state = useAuthState();

    useEffect(() => {
        if (state === "signed-out") router.replace(ROUTES.signIn);
    }, [state, router]);

    return state === "signed-in";
}

/** For sign in / sign up pages: skips them when the user is already signed in. */
export function useRedirectIfSignedIn(): void {
    const router = useRouter();
    const state = useAuthState();

    useEffect(() => {
        if (state === "signed-in") router.replace(ROUTES.home);
    }, [state, router]);
}