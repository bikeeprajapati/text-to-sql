import { Logo } from "@/components/brand/Logo";
import { CheckIcon } from "@/components/icons";

const FEATURES = [
    "Read-only, validated SQL execution",
    "AI asks clarifying questions, not just guesses",
    "Query history for every conversation",
];

export function AuthBrandPanel() {
    return (
        <aside className="hidden flex-col justify-between bg-zinc-900 p-12 text-white md:flex">
            <Logo tone="onDark" />

            <div className="max-w-md">
                <p className="text-4xl font-medium leading-tight tracking-tight">
                    Turn plain English into SQL, instantly.
                </p>
                <p className="mt-5 text-sm leading-relaxed text-zinc-400">
                    Ask questions in plain language and get precise SQL, with a clarification engine that
                    eliminates guesswork.
                </p>

                <ul className="mt-10 space-y-4">
                    {FEATURES.map((feature) => (
                        <li key={feature} className="flex items-center gap-3 text-sm text-zinc-300">
                            <span className="flex h-5 w-5 shrink-0 items-center justify-center rounded bg-white text-zinc-900">
                                <CheckIcon className="h-3 w-3" />
                            </span>
                            {feature}
                        </li>
                    ))}
                </ul>
            </div>

            <p className="text-xs text-zinc-500">&copy; 2026 QueryIQ</p>
        </aside>
    );
}