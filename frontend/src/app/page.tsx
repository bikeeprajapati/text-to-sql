"use client";

import { useState } from "react";
import { register, sendMessage, getHistory, getToken } from "@/lib/api";

export default function Home() {
  const [output, setOutput] = useState("Click the button to test the API client.");
  const [loading, setLoading] = useState(false);

  async function runTest() {
    setLoading(true);
    try {
      const email = `frontend_test_${Date.now()}@example.com`;
      await register(email, "testpassword123");
      const chat = await sendMessage("show me all customers", null);
      const history = await getHistory(chat.session_id);
      setOutput(
        JSON.stringify({ email, tokenStored: Boolean(getToken()), chat, history }, null, 2)
      );
    } catch (error) {
      setOutput(error instanceof Error ? `Error: ${error.message}` : "Unknown error");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="p-8 font-mono text-sm">
      <button
        onClick={runTest}
        disabled={loading}
        className="mb-4 rounded bg-black px-4 py-2 text-white disabled:opacity-50"
      >
        {loading ? "Running..." : "Test API"}
      </button>
      <pre className="whitespace-pre-wrap">{output}</pre>
    </main>
  );
}