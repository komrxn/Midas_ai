<template>
    <div class="subscription-page">
        <div class="subscription-page__header">
            <Button :icon="arrowLeft" severity="secondary" @click="router.back()"
                class="subscription-page__header-button" />
            <h1 class="gold-text">{{ t('subscription.title') }}</h1>
            <div class="subscription-page__header-empty" />
        </div>

        <div class="subscription-page__content">
            <!-- Шаг 1: Выбор тарифа -->
            <div v-if="step === 'plan'" class="subscription-page__step">
                <div class="subscription-page__intro">
                    <div class="subscription-page__icon">
                        <VIcon icon="👑" class="subscription-page__icon-svg" />
                    </div>
                    <h2 class="subscription-page__intro-title">{{ t('subscription.introTitle') }}</h2>
                    <p class="subscription-page__intro-subtitle">{{ t('subscription.introSubtitle') }}</p>
                </div>

                <div class="subscription-page__plans">
                    <div 
                        v-for="plan in availablePlans" 
                        :key="plan.id" 
                        class="subscription-page__plan"
                        :class="{ 'subscription-page__plan--selected': selectedPlan === plan.id }"
                        @click="selectPlan(plan.id)"
                    >
                        <div v-if="plan.badge" class="subscription-page__plan-badge">
                            {{ plan.badge }}
                        </div>
                        <div class="subscription-page__plan-content">
                            <h3 class="subscription-page__plan-title">{{ plan.title }}</h3>
                            <p class="subscription-page__plan-subtitle">{{ plan.subtitle }}</p>
                            <div class="subscription-page__plan-features">
                                <div v-for="feature in plan.features" :key="feature" class="subscription-page__plan-feature">
                                    <VIcon :icon="successIcon" class="subscription-page__plan-check" />
                                    <span>{{ feature }}</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <div v-if="selectedPlan" class="subscription-page__button-container">
                    <Button 
                        :label="t('subscription.continue')" 
                        fluid
                        class="subscription-page__button" 
                        @click="goToPeriodStep"
                    />
                </div>
            </div>

            <!-- Шаг 2: Выбор периода -->
            <div v-if="step === 'period'" class="subscription-page__step">
                <h2 class="subscription-page__step-title">{{ t('subscription.selectPeriod') }}</h2>
                <div class="subscription-page__periods">
                    <div 
                        v-for="period in periods" 
                        :key="period.id"
                        class="subscription-page__period"
                        :class="{ 'subscription-page__period--selected': selectedPeriod === period.id }"
                        @click="selectPeriod(period.id)"
                    >
                        <div class="subscription-page__period-content">
                            <h3 class="subscription-page__period-title">{{ period.title }}</h3>
                            <p v-if="period.savings" class="subscription-page__period-savings">{{ period.savings }}</p>
                            <div class="subscription-page__period-price">
                                <span class="subscription-page__period-amount">{{ period.price }}</span>
                                <span class="subscription-page__period-currency">UZS</span>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="subscription-page__button-container">
                    <Button 
                        :label="t('common.back')" 
                        severity="primary"
                        outlined
                        fluid
                        class="subscription-page__button-secondary"
                        @click="goToPlanStep"
                    />
                    <Button 
                        :label="t('subscription.continue')" 
                        fluid
                        class="subscription-page__button" 
                        :disabled="!selectedPeriod"
                        @click="goToPaymentStep"
                    />
                </div>
            </div>

            <!-- Шаг 3: Выбор способа оплаты -->
            <div v-if="step === 'payment'" class="subscription-page__step">
                <h2 class="subscription-page__step-title">{{ t('subscription.selectPaymentMethod') }}</h2>
                <div class="subscription-page__payment-methods">
                    <div 
                        class="subscription-page__payment-method"
                        :class="{ 'subscription-page__payment-method--selected': selectedPaymentMethod === 'payme' }"
                        @click="selectPaymentMethod('payme')"
                    >
                        <div class="subscription-page__payment-method-content">
                            <h3 class="subscription-page__payment-method-title">Payme</h3>
                        </div>
                    </div>
                    <div 
                        class="subscription-page__payment-method"
                        :class="{ 'subscription-page__payment-method--selected': selectedPaymentMethod === 'click' }"
                        @click="selectPaymentMethod('click')"
                    >
                        <div class="subscription-page__payment-method-content">
                            <h3 class="subscription-page__payment-method-title">Click</h3>
                        </div>
                    </div>
                </div>

                <div class="subscription-page__summary">
                    <div class="subscription-page__summary-item">
                        <span>{{ t('subscription.plan') }}:</span>
                        <span class="subscription-page__summary-value">{{ selectedPlanTitle }}</span>
                    </div>
                    <div class="subscription-page__summary-item">
                        <span>{{ t('subscription.period') }}:</span>
                        <span class="subscription-page__summary-value">{{ selectedPeriodTitle }}</span>
                    </div>
                    <div class="subscription-page__summary-item subscription-page__summary-item--total">
                        <span>{{ t('subscription.total') }}:</span>
                        <span class="subscription-page__summary-value">{{ selectedPrice }} UZS</span>
                    </div>
                </div>

                <div class="subscription-page__button-container">
                    <Button 
                        :label="t('common.back')" 
                        severity="primary"
                        outlined
                        fluid
                        class="subscription-page__button-secondary"
                        @click="goToPeriodStep"
                    />
                    <Button 
                        :label="t('subscription.pay', { price: selectedPrice })" 
                        fluid
                        class="subscription-page__button" 
                        :loading="loading"
                        :disabled="!selectedPaymentMethod"
                        @click="handlePay"
                    />
                </div>
            </div>

            <!-- Пробный период -->
            <div v-if="step === 'plan' && !isTrialUsed && !hasActiveSubscription" class="subscription-page__trial">
                <Button 
                    :label="t('subscription.startTrial')" 
                    severity="secondary"
                    outlined
                    fluid
                    class="subscription-page__trial-button"
                    :loading="loading"
                    @click="handleActivateTrial"
                />
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useI18n } from 'vue-i18n';
import { Button } from 'primevue';
import VIcon from '@/components/UI/VIcon.vue';
import successIcon from '@/assets/icons/status/success.svg?raw';
import { arrowLeft } from '@/assets/icons';
import router from '@/router/router';
import subscriptionApi from '@/api/subscription';
import { useToastStore } from '@/store/toastsStore';

const { t } = useI18n();
const toast = useToastStore();

const loading = ref(false);
const isTrialUsed = ref(false);
const hasActiveSubscription = ref(false);

const step = ref<'plan' | 'period' | 'payment'>('plan');
const selectedPlan = ref<string | null>(null);
const selectedPeriod = ref<'month' | 'quarter' | null>(null);
const selectedPaymentMethod = ref<'payme' | 'click' | null>(null);

const availablePlans = computed(() => [
    {
        id: 'plus',
        title: t('subscription.plans.plus.title'),
        subtitle: t('subscription.plans.plus.subtitle'),
        badge: null,
        features: [
            t('subscription.plans.plus.features.ai'),
            t('subscription.plans.plus.features.messages'),
            t('subscription.plans.plus.features.voice'),
            t('subscription.plans.plus.features.photos'),
            t('subscription.plans.plus.features.noAds'),
        ],
    },
    {
        id: 'pro',
        title: t('subscription.plans.pro.title'),
        subtitle: t('subscription.plans.pro.subtitle'),
        badge: null,
        features: [
            t('subscription.plans.pro.features.ai'),
            t('subscription.plans.pro.features.messages'),
            t('subscription.plans.pro.features.voice'),
            t('subscription.plans.pro.features.photos'),
            t('subscription.plans.pro.features.multiCurrency'),
            t('subscription.plans.pro.features.noAds'),
        ],
    },
    {
        id: 'premium',
        title: t('subscription.plans.premium.title'),
        subtitle: t('subscription.plans.premium.subtitle'),
        badge: t('subscription.plans.premium.badge'),
        features: [
            t('subscription.plans.premium.features.ai'),
            t('subscription.plans.premium.features.messages'),
            t('subscription.plans.premium.features.voice'),
            t('subscription.plans.premium.features.photos'),
            t('subscription.plans.premium.features.multiCurrency'),
            t('subscription.plans.premium.features.priority'),
            t('subscription.plans.premium.features.noAds'),
        ],
    },
]);

const periods = computed(() => {
    if (!selectedPlan.value) return [];
    
    const prices = {
        plus: { month: 34999, quarter: 94999 },
        pro: { month: 49999, quarter: 119999 },
        premium: { month: 89999, quarter: 229999 },
    };

    const planPrices = prices[selectedPlan.value as keyof typeof prices];
    if (!planPrices) return [];

    return [
        {
            id: 'month' as const,
            title: t('subscription.periods.month'),
            price: planPrices.month.toLocaleString('ru-RU'),
            savings: null,
        },
        {
            id: 'quarter' as const,
            title: t('subscription.periods.quarter'),
            price: planPrices.quarter.toLocaleString('ru-RU'),
            savings: t('subscription.periods.savings'),
        },
    ];
});

const selectedPlanTitle = computed(() => {
    const plan = availablePlans.value.find(p => p.id === selectedPlan.value);
    return plan?.title || '';
});

const selectedPeriodTitle = computed(() => {
    if (!selectedPeriod.value) return '';
    return periods.value.find(p => p.id === selectedPeriod.value)?.title || '';
});

const selectedPrice = computed(() => {
    if (!selectedPlan.value || !selectedPeriod.value) return '0';
    const period = periods.value.find(p => p.id === selectedPeriod.value);
    return period?.price || '0';
});

const selectPlan = (planId: string) => {
    selectedPlan.value = planId;
    selectedPeriod.value = null;
    selectedPaymentMethod.value = null;
};

const selectPeriod = (periodId: 'month' | 'quarter') => {
    selectedPeriod.value = periodId;
};

const selectPaymentMethod = (method: 'payme' | 'click') => {
    selectedPaymentMethod.value = method;
};

const goToPeriodStep = () => {
    if (selectedPlan.value) {
        step.value = 'period';
    }
};

const goToPaymentStep = () => {
    if (selectedPlan.value && selectedPeriod.value) {
        step.value = 'payment';
    }
};

const goToPlanStep = () => {
    step.value = 'plan';
    selectedPeriod.value = null;
    selectedPaymentMethod.value = null;
};

const handlePay = async () => {
    if (!selectedPlan.value) return;

    loading.value = true;
    try {
        const { data } = await subscriptionApi.generatePaymentLink(selectedPlan.value);
        if (data.url) {
            window.location.href = data.url;
        }
    } catch (error) {
        toast.error(t('subscription.paymentError'));
        console.error('Payment error:', error);
    } finally {
        loading.value = false;
    }
};

const handleActivateTrial = async () => {
    loading.value = true;
    try {
        await subscriptionApi.activateTrial();
        toast.success(t('subscription.trialActivated'));
        await checkStatus();
    } catch (error) {
        toast.error(t('subscription.trialError'));
        console.error('Trial error:', error);
    } finally {
        loading.value = false;
    }
};

const checkStatus = async () => {
    try {
        const { data } = await subscriptionApi.getStatus();
        isTrialUsed.value = data.is_trial_used;
        hasActiveSubscription.value = data.is_active;
    } catch (e) {
        console.error('Status check failed', e);
    }
};

onMounted(() => {
    checkStatus();
});
</script>

<style scoped lang="scss">
.subscription-page {
    width: 100%;
    padding: 2.4rem;
    padding-bottom: 12rem;
    min-height: 100dvh;
    display: flex;
    flex-direction: column;

    &__header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 2rem;
    }

    &__header-button {
        width: 3.6rem;
        height: 3.6rem;
    }

    &__header-empty {
        width: 3.6rem;
        height: 3.6rem;
    }

    &__content {
        display: flex;
        flex-direction: column;
        gap: 2.4rem;
        flex: 1;
    }

    &__step {
        display: flex;
        flex-direction: column;
        gap: 2.4rem;
    }

    &__step-title {
        font: var(--font-24-b);
        color: var(--text-color);
        margin: 0;
        text-align: center;
    }

    &__intro {
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        gap: 1.2rem;
    }

    &__icon {
        width: 8rem;
        height: 8rem;
        border-radius: 2rem;
        background: var(--gold-card-bg);
        border: 1px solid var(--gold-border);
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 0.8rem;
        position: relative;
        overflow: hidden;

        &::before {
            content: '';
            position: absolute;
            inset: 0;
            border-radius: 2rem;
            background: var(--gold-card-radial);
            pointer-events: none;
        }
    }

    &__icon-svg {
        font-size: 4rem;
        position: relative;
        z-index: 1;
    }

    &__intro-title {
        font: var(--font-24-b);
        color: var(--text-color);
        margin: 0;
    }

    &__intro-subtitle {
        font: var(--font-14-r);
        color: var(--text-color-secondary);
        margin: 0;
        opacity: 0.8;
    }

    &__plans {
        display: flex;
        flex-direction: column;
        gap: 1.2rem;
    }

    &__plan {
        position: relative;
        padding: 1.6rem;
        background: var(--card-default);
        border-radius: 1.6rem;
        border: 2px solid var(--border-light);
        cursor: pointer;
        transition: all 0.3s ease;

        &:hover {
            border-color: var(--border-medium);
            transform: translateY(-2px);
        }

        &--selected {
            background: var(--gold-card-bg);
            border-color: var(--gold-border);
            box-shadow: var(--gold-shadow);
            position: relative;
            overflow: hidden;

            &::before {
                content: '';
                position: absolute;
                inset: 0;
                border-radius: 1.6rem;
                background: var(--gold-card-radial);
                pointer-events: none;
            }
        }
    }

    &__plan-badge {
        position: absolute;
        top: 1.2rem;
        right: 1.2rem;
        padding: 0.4rem 0.8rem;
        background: linear-gradient(135deg, rgba(147, 51, 234, 0.8) 0%, rgba(147, 51, 234, 0.6) 100%);
        border-radius: 1.2rem;
        font: var(--font-12-b);
        color: var(--white);
        z-index: 1;
    }

    &__plan-content {
        display: flex;
        flex-direction: column;
        gap: 1.2rem;
        position: relative;
        z-index: 1;
    }

    &__plan-title {
        font: var(--font-20-b);
        color: var(--text-color);
        margin: 0;
    }

    &__plan-subtitle {
        font: var(--font-14-r);
        color: var(--text-color-secondary);
        margin: 0;
    }

    &__plan-features {
        display: flex;
        flex-direction: column;
        gap: 0.8rem;
    }

    &__plan-feature {
        display: flex;
        align-items: center;
        gap: 0.8rem;
        font: var(--font-14-r);
        color: var(--text-color);
    }

    &__plan-check {
        width: 1.6rem;
        height: 1.6rem;
        flex-shrink: 0;
        color: var(--gold-text-color, rgba(220, 180, 0, 1));
    }

    &__periods {
        display: flex;
        flex-direction: column;
        gap: 1.2rem;
    }

    &__period {
        position: relative;
        padding: 1.6rem;
        background: var(--card-default);
        border-radius: 1.6rem;
        border: 2px solid var(--border-light);
        cursor: pointer;
        transition: all 0.3s ease;

        &:hover {
            border-color: var(--border-medium);
            transform: translateY(-2px);
        }

        &--selected {
            background: var(--gold-card-bg);
            border-color: var(--gold-border);
            box-shadow: var(--gold-shadow);
            position: relative;
            overflow: hidden;

            &::before {
                content: '';
                position: absolute;
                inset: 0;
                border-radius: 1.6rem;
                background: var(--gold-card-radial);
                pointer-events: none;
            }
        }
    }

    &__period-content {
        display: flex;
        flex-direction: column;
        gap: 0.8rem;
        position: relative;
        z-index: 1;
    }

    &__period-title {
        font: var(--font-18-b);
        color: var(--text-color);
        margin: 0;
    }

    &__period-savings {
        font: var(--font-14-r);
        color: var(--gold-text-color, rgba(220, 180, 0, 1));
        margin: 0;
    }

    &__period-price {
        display: flex;
        align-items: baseline;
        gap: 0.4rem;
        margin-top: 0.4rem;
    }

    &__period-amount {
        font: var(--font-24-b);
        color: var(--gold-text-color, rgba(220, 180, 0, 1));
    }

    &__period-currency {
        font: var(--font-14-r);
        color: var(--text-color-secondary);
    }

    &__payment-methods {
        display: flex;
        flex-direction: column;
        gap: 1.2rem;
    }

    &__payment-method {
        position: relative;
        padding: 1.6rem;
        background: var(--card-default);
        border-radius: 1.6rem;
        border: 2px solid var(--border-light);
        cursor: pointer;
        transition: all 0.3s ease;

        &:hover {
            border-color: var(--border-medium);
            transform: translateY(-2px);
        }

        &--selected {
            background: var(--gold-card-bg);
            border-color: var(--gold-border);
            box-shadow: var(--gold-shadow);
            position: relative;
            overflow: hidden;

            &::before {
                content: '';
                position: absolute;
                inset: 0;
                border-radius: 1.6rem;
                background: var(--gold-card-radial);
                pointer-events: none;
            }
        }
    }

    &__payment-method-content {
        display: flex;
        align-items: center;
        justify-content: space-between;
        position: relative;
        z-index: 1;
    }

    &__payment-method-title {
        font: var(--font-18-b);
        color: var(--text-color);
        margin: 0;
    }

    &__summary {
        display: flex;
        flex-direction: column;
        gap: 1.2rem;
        padding: 1.6rem;
        background: var(--card-default);
        border-radius: 1.6rem;
        border: 1px solid var(--border-light);
    }

    &__summary-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        font: var(--font-14-r);
        color: var(--text-color);

        &--total {
            padding-top: 1.2rem;
            border-top: 1px solid var(--border-light);
            font: var(--font-16-b);
        }
    }

    &__summary-value {
        font-weight: 600;
        color: var(--gold-text-color, rgba(220, 180, 0, 1));
    }

    &__button-container {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        display: flex;
        flex-direction: column;
        gap: 1rem;
        padding: 1.6rem 2.4rem;
        background: var(--card-default);
        border-top: 1px solid var(--border-light);
        z-index: 100;
        box-shadow: 0 -4px 16px rgba(0, 0, 0, 0.1);
    }

    &__button {
        padding: 1.6rem;
        font: var(--font-16-b);
        background: linear-gradient(135deg, rgba(220, 180, 0, 0.9) 0%, rgba(200, 160, 0, 0.9) 100%) !important;
        border: 1px solid var(--gold-border) !important;
        color: var(--text-color) !important;
        border-radius: 1.6rem;
        transition: all 0.3s ease;

        &:hover:not(:disabled) {
            background: linear-gradient(135deg, rgba(220, 180, 0, 1) 0%, rgba(200, 160, 0, 1) 100%) !important;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(220, 180, 0, 0.3);
        }

        &:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }
    }

    &__button-secondary {
        padding: 1.6rem;
        font: var(--font-16-b);
        border-radius: 1.6rem;
    }

    &__trial {
        margin-top: 1.2rem;
    }

    &__trial-button {
        padding: 1.6rem;
        font: var(--font-16-b);
        border-radius: 1.6rem;
    }
}
</style>
