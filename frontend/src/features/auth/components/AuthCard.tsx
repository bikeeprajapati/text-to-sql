import type { ReactNode } from "react";

interface AuthCardProps {
    title: string;
    subtitle: string;
    children: ReactNode;
    footer: ReactNode;
}

export function AuthCard({ title, subtitle, children, footer }: AuthCardProps) {
    return (
        <section>
            <h1 className="text-xl font-semibold">{title}</h1>
            <p className="mt-1 text-xs text-zinc-500">{subtitle}</p>

            <div className="mt-7">{children}</div>

            <p className="mt-6 text-center text-xs text-zinc-500">{footer}</p>
        </section>
    );
}