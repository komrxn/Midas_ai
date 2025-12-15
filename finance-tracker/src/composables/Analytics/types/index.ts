export type Period = 'day' | 'week' | 'month' | 'year';
export type CategoryType = 'income' | 'expense';
export type Granularity = 'hour' | 'day' | 'week' | 'month';

export type Currency = 'uzs' | 'usd' | 'eur' | 'rub';

// Balance Response
export interface BalanceResponse {
    balance: string;
    total_income: string;
    total_expense: string;
    currency: Currency;
    period_label: string;
}

// Category Breakdown Response
export interface CategoryBreakdownItem {
    category_id: string;
    category_name: string;
    category_slug: string;
    amount: string;
    percentage: number;
    transaction_count: number;
    color: string;
}

export interface CategoryBreakdownResponse {
    categories: CategoryBreakdownItem[];
    total: string;
    currency: Currency;
}

// Trends Response
export interface TrendDataPoint {
    date: string;
    income: string;
    expense: string;
    balance: string;
}

export interface TrendsResponse {
    data: TrendDataPoint[];
    granularity: string;
    currency: Currency;
}

// Trend Info (для income_trend и expense_trend)
export interface TrendInfo {
    current_value: string;
    previous_value: string;
    change_percentage: number;
    is_up: boolean;
}

// Summary Response
export interface SummaryResponse {
    balance: BalanceResponse;
    category_breakdown: CategoryBreakdownResponse;
    trends: TrendsResponse;
    income_trend: TrendInfo;
    expense_trend: TrendInfo;
}

// Request Parameters
export interface GetBalanceParams {
    period: Period;
}

export interface GetCategoriesParams {
    period: Period;
    type: CategoryType;
}

export interface GetTrendsParams {
    period: Period;
    granularity: Granularity;
}

export interface GetSummaryParams {
    period: Period;
    type?: CategoryType;
    granularity?: Granularity;
}
