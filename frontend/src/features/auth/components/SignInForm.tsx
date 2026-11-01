"use client";

import Link from "next/link";
import { Alert } from "@/components/ui/Alert";
import { Button } from "@/components/ui/Button";
import { PasswordField } from "@/components/ui/PasswordField";
import { TextField } from "@/components/ui/TextField";
import { ROUTES } from "@/constants/routes";
import { login } from "@/lib/api/auth";
import { AuthCard } from "@/features/auth/components/AuthCard";
import { useAuthForm } from "@/features/auth/hooks/useAuthForm";
import { validateSignIn } from "@/features/auth/validation";

export function SignInForm() {
    const form = useAuthForm({ validate: validateSignIn, submit: login });

    return (
        <AuthCard
            title="Sign in"
            subtitle="Welcome back. Enter your credentials to continue."
            footer={
                <>
                    Don&apos;t have an account?{" "}
                    <Link href={ROUTES.signUp} className="font-medium text-blue-600 hover:underline">
                        Sign up free
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
                    autoComplete="current-password"
                    placeholder="••••••••"
                    value={form.password}
                    onChange={(event) => form.setPassword(event.target.value)}
                    error={form.fieldErrors.password}
                />

                {form.formError && <Alert>{form.formError}</Alert>}

                <Button type="submit" fullWidth loading={form.submitting}>
                    {form.submitting ? "Please wait..." : "Sign in"}
                </Button>
            </form>
        </AuthCard>
    );
}