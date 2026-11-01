"use client";

import Link from "next/link";
import { Alert } from "@/components/ui/Alert";
import { Button } from "@/components/ui/Button";
import { PasswordField } from "@/components/ui/PasswordField";
import { TextField } from "@/components/ui/TextField";
import { ROUTES } from "@/constants/routes";
import { register } from "@/lib/api/auth";
import { AuthCard } from "@/features/auth/components/AuthCard";
import { useAuthForm } from "@/features/auth/hooks/useAuthForm";
import { PASSWORD_MIN_LENGTH, validateSignUp } from "@/features/auth/validation";

export function SignUpForm() {
    const form = useAuthForm({ validate: validateSignUp, submit: register });

    return (
        <AuthCard
            title="Create your account"
            subtitle="Sign up to start asking questions."
            footer={
                <>
                    Already have an account?{" "}
                    <Link href={ROUTES.signIn} className="font-medium text-blue-600 hover:underline">
                        Sign in
                    </Link>
                </>
            }
        >
            <form onSubmit={form.handleSubmit} noValidate className="space-y-4">
                <TextField
                    label="Email"
                    type="email"
                    autoComplete="email"
                    placeholder="you@company.com"
                    value={form.email}
                    onChange={(event) => form.setEmail(event.target.value)}
                    error={form.fieldErrors.email}
                />

                <PasswordField
                    label="Password"
                    autoComplete="new-password"
                    placeholder="••••••••"
                    hint={`At least ${PASSWORD_MIN_LENGTH} characters.`}
                    value={form.password}
                    onChange={(event) => form.setPassword(event.target.value)}
                    error={form.fieldErrors.password}
                />

                {form.formError && <Alert>{form.formError}</Alert>}

                <Button type="submit" fullWidth loading={form.submitting}>
                    {form.submitting ? "Please wait..." : "Create account"}
                </Button>
            </form>
        </AuthCard>
    );
}