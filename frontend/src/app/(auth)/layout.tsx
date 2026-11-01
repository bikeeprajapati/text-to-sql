import type { ReactNode } from "react";
import { DM_Sans } from "next/font/google";
import { Logo } from "@/components/brand/Logo";
import { AuthBrandPanel } from "@/features/auth/components/AuthBrandPanel";
import { RedirectIfSignedIn } from "@/features/auth/components/RedirectIfSignedIn";

const dmSans = DM_Sans({ subsets: ["latin"] });

export default function AuthLayout({ children }: { children: ReactNode }) {
    return (
        <div className={`${dmSans.className} grid min-h-screen md:grid-cols-2`}>
            <RedirectIfSignedIn />
            <AuthBrandPanel />

            <main className="flex items-center justify-center bg-zinc-100 p-8 text-zinc-900">
                <div className="w-full max-w-sm">
                    <div className="mb-10 md:hidden">
                        <Logo tone="onLight" />
                    </div>
                    {children}
                </div>
            </main>
        </div>
    );
}