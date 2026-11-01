"use client";

import { useId, type InputHTMLAttributes, type ReactNode } from "react";

export interface TextFieldProps extends Omit<InputHTMLAttributes<HTMLInputElement>, "id" | "className"> {
    label: string;
    /** Validation message; replaces the hint while present. */
    error?: string | null;
    hint?: string;
    /** Content rendered inside the right edge of the input (e.g. a show/hide button). */
    endAdornment?: ReactNode;
}

export function TextField({ label, error, hint, endAdornment, ...inputProps }: TextFieldProps) {
    const id = useId();
    const messageId = `${id}-message`;
    const message = error ?? hint;

    return (
        <div>
            <label htmlFor={id} className="mb-1.5 block text-xs font-medium text-zinc-700">
                {label}
            </label>

            <div className="relative">
                <input
                    id={id}
                    aria-invalid={error ? true : undefined}
                    aria-describedby={message ? messageId : undefined}
                    className={`w-full rounded-lg border bg-white py-2.5 pl-3.5 text-sm placeholder:text-zinc-400 focus:outline-none ${endAdornment ? "pr-10" : "pr-3.5"
                        } ${error ? "border-red-400 focus:border-red-500" : "border-zinc-200 focus:border-zinc-900"}`}
                    {...inputProps}
                />
                {endAdornment && <div className="absolute inset-y-0 right-0 flex items-center">{endAdornment}</div>}
            </div>

            {message && (
                <p id={messageId} className={`mt-1.5 text-xs ${error ? "text-red-600" : "text-zinc-500"}`}>
                    {message}
                </p>
            )}
        </div>
    );
}