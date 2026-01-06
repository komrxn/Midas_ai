export interface User {
    id: string;
    telegram_id: number;
    phone_number: string;
    name: string;
    default_currency: string;
    created_at: string;
    is_premium: boolean;
    subscription_type?: string;
    subscription_ends_at?: string;
    is_trial_used: boolean;
    is_active: boolean;
    voice_usage_count?: number;
    photo_usage_count?: number;
}

