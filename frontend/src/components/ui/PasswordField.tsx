"use client";

import { useState } from "react";
import { EyeIcon, EyeOffIcon } from "@/components/icons";
import { TextField, type TextFieldProps } from "@/components/ui/TextField";

export function PasswordField(props: Omit<TextFieldProps, "type" | "endAdornment">) {
    const [visible, setVisible] = useState(false);

    return (
        <TextField
            {...props}
            type={visible ? "text" : "password"}
            endAdornment={
                <button
                    type="button"
                    onClick={() => setVisible((current) => !current)}
                    aria-label={visible ? "Hide password" : "Show password"}
                    aria-pressed={visible}
                    className="flex h-full w-10 items-center justify-center text-zinc-400 hover:text-zinc-700"
                >
                    {visible ? <EyeOffIcon className="h-4 w-4" /> : <EyeIcon className="h-4 w-4" />}
                </button>
            }
        />
    );
}