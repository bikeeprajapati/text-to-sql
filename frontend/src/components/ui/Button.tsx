import type { ButtonHTMLAttributes } from "react";

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
    loading?: boolean;
    fullWidth?: boolean;
}

export function Button({
    loading = false,
    fullWidth = false,
    disabled,
    className = "",
    children,
    ...props
}: ButtonProps) {
    return (
        <button
            disabled={disabled || loading}
            aria-busy={loading}
            className={`rounded-lg bg-zinc-900 px-4 py-2.5 text-sm font-medium text-white transition-colors hover:bg-zinc-800 disabled:cursor-not-allowed disabled:opacity-50 ${fullWidth ? "w-full" : ""
                } ${className}`}
            {...props}
        >
            {children}
        </button>
    );
}