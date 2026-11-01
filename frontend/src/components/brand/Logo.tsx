import { BoltIcon } from "@/components/icons";

interface LogoProps {
    /** "onDark" for dark backgrounds (white mark), "onLight" for light backgrounds. */
    tone?: "onDark" | "onLight";
}

export function Logo({ tone = "onDark" }: LogoProps) {
    const onDark = tone === "onDark";

    return (
        <div className="flex items-center gap-2.5">
            <span
                className={`flex h-7 w-7 items-center justify-center rounded-md ${onDark ? "bg-white text-zinc-900" : "bg-zinc-900 text-white"
                    }`}
            >
                <BoltIcon className="h-4 w-4" />
            </span>
            <span className={`text-sm font-medium ${onDark ? "text-white" : "text-zinc-900"}`}>QueryIQ</span>
        </div>
    );
}