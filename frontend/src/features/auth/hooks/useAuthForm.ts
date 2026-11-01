"use client";

import { useState, type FormEvent } from "react";
import { useRouter } from "next/navigation";
import { ROUTES } from "@/constants/routes";
import { ApiError } from "@/lib/api/client";
import type { Credentials, FieldErrors } from "@/features/auth/validation";

interface UseAuthFormOptions {
    validate: (values: Credentials) => FieldErrors;
    submit: (email: string, password: string) => Promise<void>;
}

/** Shared state and submit flow for the sign in and sign up forms. */
export function useAuthForm({ validate, submit }: UseAuthFormOptions) {
    const router = useRouter();

    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [fieldErrors, setFieldErrors] = useState<FieldErrors>({});
    const [formError, setFormError] = useState<string | null>(null);
    const [submitting, setSubmitting] = useState(false);

    async function handleSubmit(event: FormEvent<HTMLFormElement>) {
        event.preventDefault();

        const trimmedEmail = email.trim();
        const errors = validate({ email: trimmedEmail, password });

        setFieldErrors(errors);
        setFormError(null);
        if (Object.keys(errors).length > 0) return;

        setSubmitting(true);
        try {
            await submit(trimmedEmail, password);
            router.replace(ROUTES.home);
        } catch (error) {
            setFormError(error instanceof ApiError ? error.message : "Something went wrong. Please try again.");
            setSubmitting(false);
        }
    }

    return { email, setEmail, password, setPassword, fieldErrors, formError, submitting, handleSubmit };
}