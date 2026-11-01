"use client";

import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/Button";
import { ROUTES } from "@/constants/routes";
import { useRequireAuth } from "@/hooks/useAuth";
import { logout } from "@/lib/api/auth";

export default function Home() {
  const router = useRouter();
  const signedIn = useRequireAuth();

  // While we check (or while redirecting to sign in) render nothing
  if (!signedIn) return null;

  function handleSignOut() {
    logout();
    router.replace(ROUTES.signIn);
  }

  return (
    <main className="flex min-h-screen flex-col items-center justify-center gap-4 p-8">
      <h1 className="text-2xl font-semibold">You&apos;re signed in</h1>
      <p className="text-zinc-500">The chat page comes next.</p>
      <Button onClick={handleSignOut}>Sign out</Button>
    </main>
  );
}