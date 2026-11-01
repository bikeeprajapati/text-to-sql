import type { SVGProps } from "react";

type IconProps = SVGProps<SVGSVGElement>;

const strokeProps = {
    fill: "none",
    stroke: "currentColor",
    strokeLinecap: "round",
    strokeLinejoin: "round",
} as const;

export function BoltIcon(props: IconProps) {
    return (
        <svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" {...props}>
            <path d="M13 2 3 14h9l-1 8 10-12h-9l1-8z" />
        </svg>
    );
}

export function CheckIcon(props: IconProps) {
    return (
        <svg viewBox="0 0 24 24" {...strokeProps} strokeWidth={3} aria-hidden="true" {...props}>
            <path d="M5 12.5l4.5 4.5L19 7.5" />
        </svg>
    );
}

export function EyeIcon(props: IconProps) {
    return (
        <svg viewBox="0 0 24 24" {...strokeProps} strokeWidth={1.8} aria-hidden="true" {...props}>
            <path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12z" />
            <circle cx="12" cy="12" r="3" />
        </svg>
    );
}

export function EyeOffIcon(props: IconProps) {
    return (
        <svg viewBox="0 0 24 24" {...strokeProps} strokeWidth={1.8} aria-hidden="true" {...props}>
            <path d="M17.9 17.9A10.4 10.4 0 0 1 12 19c-6.5 0-10-7-10-7a17.7 17.7 0 0 1 4.1-5" />
            <path d="M9.9 5.2A9.7 9.7 0 0 1 12 5c6.5 0 10 7 10 7a17.6 17.6 0 0 1-2.2 3.2" />
            <path d="M9.9 9.9a3 3 0 0 0 4.2 4.2" />
            <path d="M3 3l18 18" />
        </svg>
    );
}