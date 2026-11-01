import type { ChatResponse, HistoryResponse } from "@/types/api";
import { request } from "@/lib/api/client";

export function sendMessage(message: string, sessionId: string | null): Promise<ChatResponse> {
    return request<ChatResponse>("/api/chat", {
        method: "POST",
        body: { session_id: sessionId, message },
    });
}

export function getHistory(sessionId: string): Promise<HistoryResponse> {
    return request<HistoryResponse>(`/api/history?session_id=${encodeURIComponent(sessionId)}`);
}