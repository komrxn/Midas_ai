<script setup lang="ts">
import { computed, onBeforeMount, ref } from 'vue';
import { storeToRefs } from 'pinia';
import { useRouter } from 'vue-router';
import { Button } from 'primevue';
import TransactionCard from '@/components/Transactions/TransactionCard.vue';
import TransactionDetails from '@/components/Transactions/TransactionDetails.vue';
import VDrawer from '@/components/UI/VDrawer.vue';
import { useTransactionsStore } from '@/store/transactionsStore';
import { useCategoriesStore } from '@/store/categoriesStore';
import { getStartOfDayString, formatDateToAPIDatetime } from '@/utils';
import type { Transaction } from '@/composables/Transactions/types';

const router = useRouter();
const transactionsStore = useTransactionsStore();
const categoriesStore = useCategoriesStore();

const { groupedTransactions, loading } = storeToRefs(transactionsStore);
const { loadTransactions } = transactionsStore;
const { loadCategories } = categoriesStore;

// Показываем только первую группу (сегодняшний день)
const todayTransactions = computed(() => {
    if (groupedTransactions.value.length === 0) return null;
    return groupedTransactions.value[0];
});

const handleViewAll = () => {
    router.push({ name: 'transactions' });
};

const detailsDrawerVisible = ref(false);
const selectedTransaction = ref<Transaction | null>(null);

const handleTransactionClick = (transaction: Transaction) => {
    selectedTransaction.value = transaction;
    detailsDrawerVisible.value = true;
};

onBeforeMount(async () => {
    // Загружаем только транзакции за сегодня (один день)
    // Преобразуем дату в формат datetime для API (T00:00:00 для начала, T23:59:59 для конца)
    const todayDateString = getStartOfDayString();
    const startDate = formatDateToAPIDatetime(todayDateString, false); // 00:00:00
    const endDate = formatDateToAPIDatetime(todayDateString, true); // 23:59:59

    await Promise.all([
        loadCategories(),
        loadTransactions({
            start_date: startDate,
            end_date: endDate,
            page_size: 10, // Ограничиваем количество для главной страницы
        }, false, true) // force = true, чтобы всегда загружать свежие данные для главной страницы
    ]);

    // После загрузки сбрасываем фильтры, чтобы они не мешали при переходе на страницу транзакций
    // Но только если мы не на странице транзакций
    if (router.currentRoute.value.name !== 'transactions') {
        transactionsStore.currentFilters = undefined;
        transactionsStore.isLoaded = false;
    }
});
</script>

<template>
    <div class="main-transactions">
        <div class="main-transactions__header">
            <h1 class="font-20-b gold-text">Транзакции</h1>
            <Button label="Посмотреть все" text size="small" @click="handleViewAll" />
        </div>
        <div v-if="loading" class="main-transactions__loading">
            <p class="font-14-r">Загрузка...</p>
        </div>
        <div v-else-if="todayTransactions && todayTransactions.transactions.length > 0" class="main-transactions__list">
            <TransactionCard v-for="transaction in todayTransactions.transactions.slice(0, 5)" :key="transaction.id"
                :transaction="transaction" @click="handleTransactionClick" />
        </div>
        <div v-else class="main-transactions__empty">
            <p class="font-14-r">Нет транзакций за сегодня</p>
        </div>

        <VDrawer v-model:visible="detailsDrawerVisible">
            <template #header>
                <h2 class="transaction-details-drawer__title">Детали транзакции</h2>
            </template>
            <TransactionDetails v-if="selectedTransaction" :transaction="selectedTransaction" />
        </VDrawer>
    </div>
</template>

<style scoped lang="scss">
.main-transactions {
    background: var(--gold-card-bg);
    padding: 1.2rem;
    border-radius: 1.6rem;
    margin-top: 1.2rem;
    border: 1px solid var(--gold-border);
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

    &__header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin: 0 0 2rem 0;
        position: relative;
        z-index: 1;
    }

    &__list {
        display: flex;
        flex-direction: column;
        gap: 0.8rem;
        position: relative;
        z-index: 1;
    }

    &__loading {
        display: flex;
        justify-content: center;
        padding: 2rem;
        position: relative;
        z-index: 1;
    }

    &__empty {
        display: flex;
        justify-content: center;
        padding: 2rem;
        position: relative;
        z-index: 1;
        color: var(--text-color-secondary);
    }
}

.transaction-details-drawer {
    &__title {
        font: var(--font-20-b);
        margin: 0;
    }
}
</style>
