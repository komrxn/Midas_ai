<script setup lang="ts">
import { ITransaction } from '@/composables/Main/types';
import VIcon from './VIcon.vue';
import { Button } from 'primevue';
import { formatAmount } from '@/utils';

defineProps<{
    transaction: ITransaction;
}>();
</script>

<template>
    <Button fluid class="transaction-button" text>
        <div class="transaction-button__content">
            <div class="transaction-button__content__icon">
                <VIcon :icon="transaction.icon" />
            </div>
            <h1 class="font-16-r">{{ transaction.title }}</h1>
        </div>
        <div class="transaction-button__amount">
            <p class="font-16-r">-{{ formatAmount(transaction.amount) }} <span class="font-12-r">UZS</span>
            </p>
            <p class="font-12-r transaction-button__time">{{ transaction.date }}</p>
        </div>
    </Button>
</template>

<style scoped lang="scss">
.transaction-button {
    display: flex;
    border-radius: 1.6rem;
    // border: 1px solid var(--gold-border);
    // box-shadow: var(--gold-shadow);
    width: 100%;
    color: var(--text-color) !important;
    padding: .6rem 1rem .6rem .2rem;
    justify-content: space-between;

    &__content {
        display: flex;
        align-items: center;
        gap: 1rem;

        &__icon {
            width: 4.4rem;
            height: 4.4rem;
            display: flex;
            justify-content: center;
            align-items: center;
            border-radius: 50%;
            background-color: rgba(255, 217, 0, 0.1);
            color: var(--primary-500);
        }
    }

    &__amount {
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        align-items: flex-end;
        gap: .8rem;
    }

    &__time {
        color: var(--text-color-secondary);
    }
}
</style>