"use client";

import { useRedirectIfSignedIn } from "@/hooks/useAuth";

/** Renders nothing; sends already-signed-in users away from the auth pages. */
export function RedirectIfSignedIn() {
    useRedirectIfSignedIn();
    return null;
}