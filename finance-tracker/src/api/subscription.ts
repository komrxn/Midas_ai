import type { AxiosResponse } from 'axios';
import $axios from './index';

export interface SubscriptionStatus {
    is_active: boolean
    is_premium: boolean
    subscription_type: string | null
    subscription_ends_at: string | null
    is_trial_used: boolean
    expires_at: string | null
}

export interface PaymentLinkResponse {
    url: string
    click_trans_id: string
    amount: number
}

export default {
    async getStatus(): Promise<AxiosResponse<SubscriptionStatus>> {
        return $axios.get('/subscriptions/status');
    },

    async activateTrial(): Promise<AxiosResponse<SubscriptionStatus>> {
        return $axios.post('/subscriptions/trial');
    },

    async generatePaymentLink(planId: string = 'monthly', provider: string = 'click'): Promise<AxiosResponse<PaymentLinkResponse>> {
        return $axios.post('/subscriptions/pay', {
            plan_id: planId,
            provider,
        });
    },
};
