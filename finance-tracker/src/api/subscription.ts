import $axios from './index';
import type { AxiosResponse } from 'axios';

export interface SubscriptionStatus {
    is_active: boolean;
    is_premium: boolean;
    subscription_type: string | null;
    subscription_ends_at: string | null;
    is_trial_used: boolean;
    expires_at: string | null;
}

export interface PaymentLinkResponse {
    url: string;
    click_trans_id: string;
    amount: number;
}

export default {
    async getStatus(): Promise<AxiosResponse<SubscriptionStatus>> {
        return $axios.get('/subscriptions/status');
    },

    async activateTrial(): Promise<AxiosResponse<SubscriptionStatus>> {
        return $axios.post('/subscriptions/trial');
    },

    async generatePaymentLink(
        planId: string, 
        period: 'month' | 'quarter' = 'month',
        paymentMethod: 'payme' | 'click' = 'payme'
    ): Promise<AxiosResponse<PaymentLinkResponse>> {
        return $axios.post('/subscriptions/pay', { 
            plan_id: planId,
            period: period,
            payment_method: paymentMethod
        });
    }
};
