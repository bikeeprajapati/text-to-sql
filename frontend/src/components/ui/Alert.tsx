import type { ReactNode } from "react";

export function Alert({ children }: { children: ReactNode }) {
    return (
        <p role="alert" className="rounded-lg bg-red-50 px-3.5 py-2.5 text-xs text-red-700">
            {children}
        </p>
    );
}