export type QueryStatus = "clarification_needed" | "executed" | "failed";

export interface ClarificationQuestion {
    question: string;
    options: string[] | null;
}

export interface ChatResponse {
    session_id: string;
    status: QueryStatus;
    message: string;
    clarification: ClarificationQuestion | null;
    generated_sql: string | null;
    result: Record<string, unknown>[] | null;
}

export interface HistoryItem {
    id: string;
    session_id: string;
    question: string;
    generated_sql: string | null;
    status: QueryStatus;
    created_at: string;
}

export interface HistoryResponse {
    items: HistoryItem[];
    total: number;
}

export interface TokenResponse {
    access_token: string;
    token_type: string;
}