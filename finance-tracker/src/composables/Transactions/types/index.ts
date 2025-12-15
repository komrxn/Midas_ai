export type TransactionType = 'income' | 'expense';
export type Currency = 'uzs' | 'usd' | 'eur' | 'rub';

export interface Transaction {
    id: string;
    type: TransactionType;
    amount: string;
    currency: Currency;
    description: string;
    category_id: string;
    transaction_date: string;
    user_id: string;
    ai_parsed_data: any | null;
    ai_confidence: number | null;
    created_at: string;
    updated_at: string;
}

export interface TransactionsResponse {
    total: number;
    items: Transaction[];
    page: number;
    page_size: number;
}

export interface GetTransactionsParams {
    page?: number;
    page_size?: number;
    type?: TransactionType;
    category_id?: string;
    start_date?: string; // ISO date string
    end_date?: string; // ISO date string
    currency?: Currency;
    search?: string; // Поиск по описанию
}

export interface TransactionFormData {
    type: TransactionType;
    amount: number;
    currency: Currency;
    description: string;
    category_id: string;
    transaction_date: string;
}

export interface TransactionCreateData {
    type: TransactionType;
    amount: string;
    currency: Currency;
    description: string;
    category_id: string;
    transaction_date: string;
}

export interface TransactionUpdateData {
    type?: TransactionType;
    amount?: string;
    currency?: Currency;
    description?: string;
    category_id?: string;
    transaction_date?: string;
}

// Группировка транзакций по дням
export interface TransactionGroup {
    date: string; // Дата в формате YYYY-MM-DD
    dateLabel: string; // Форматированная дата для отображения
    transactions: Transaction[];
    totalIncome: number;
    totalExpense: number;
}
