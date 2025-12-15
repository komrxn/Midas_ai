<template>
    <VDrawer v-model:visible="localVisible" @update:visible="handleVisibilityChange">
        <template #header>
            <h2 class="transaction-filter-form__title">{{ t('filters.transactionFilters') }}</h2>
        </template>

        <VForm @submit-form="handleSubmit" class="transaction-filter-form__form-wrapper">
            <div class="transaction-filter-form__form">
                <div class="transaction-filter-form__form-section">
                    <VSelect v-model="formData.type" :options="typeOptions" option-label="label" option-value="value"
                        :placeholder="t('filters.allTypes')" :label="t('transactions.typeLabel')" size="small"
                        class="font-14-r" />
                </div>

                <div class="transaction-filter-form__form-section">
                    <VSelect v-model="formData.category_id" :options="categoriesOptions" option-label="name"
                        option-value="id" :placeholder="t('filters.allCategories')" :label="t('filters.category')"
                        size="small" class="font-14-r" />
                </div>

                <div class="transaction-filter-form__form-section">
                    <VSelect v-model="formData.currency" :options="currencyOptions" option-label="label"
                        option-value="value" :placeholder="t('filters.allCurrencies')" :label="t('debts.currency')"
                        size="small" class="font-14-r" />
                </div>

                <div class="transaction-filter-form__form-section">
                    <VInputText v-model="formData.start_date" type="date" :label="t('filters.startDate')" size="small"
                        class="font-14-r" />
                </div>

                <div class="transaction-filter-form__form-section">
                    <VInputText v-model="formData.end_date" type="date" :label="t('filters.endDate')" size="small"
                        class="font-14-r" />
                </div>

                <div class="transaction-filter-form__form-section">
                    <VInputText v-model="formData.search" :placeholder="t('filters.searchByDescription')"
                        :label="t('filters.search')" size="small" class="font-14-r" />
                </div>
            </div>

            <div class="transaction-filter-form__footer">
                <div class="transaction-filter-form__buttons">
                    <Button :label="t('filters.reset')" severity="secondary" outlined fluid @click="handleReset"
                        class="transaction-filter-form__button" />
                    <Button :label="t('filters.apply')" type="submit" fluid severity="primary"
                        class="transaction-filter-form__button" />
                </div>
            </div>
        </VForm>
    </VDrawer>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue';
import { storeToRefs } from 'pinia';
import { useI18n } from 'vue-i18n';
import { Button } from 'primevue';
import VDrawer from '@/components/UI/VDrawer.vue';
import VForm from '@/components/Form/VForm.vue';
import VInputText from '@/components/Form/VInputText.vue';
import VSelect from '@/components/Form/VSelect.vue';
import type { GetTransactionsParams } from '@/composables/Transactions/types';
import { useCategoriesStore } from '@/store/categoriesStore';
import { formatDateToAPIDatetime } from '@/utils';

const { t } = useI18n();

/**
 * Преобразует datetime в формат даты для input type="date" (YYYY-MM-DD)
 * @param datetimeString - строка с датой в формате YYYY-MM-DDTHH:mm:ss или YYYY-MM-DD
 * @returns Строка в формате YYYY-MM-DD
 */
const formatDatetimeToDate = (datetimeString: string): string => {
    if (!datetimeString) {
        return '';
    }
    // Если строка содержит T, берем только часть до T
    if (datetimeString.includes('T')) {
        return datetimeString.split('T')[0];
    }
    return datetimeString;
};

const props = defineProps<{
    visible: boolean;
    currentFilters?: GetTransactionsParams;
}>();

const emit = defineEmits<{
    (e: 'update:visible', value: boolean): void;
    (e: 'apply', filters: GetTransactionsParams): void;
    (e: 'reset'): void;
}>();

const { categories } = storeToRefs(useCategoriesStore());

const localVisible = ref(props.visible);

const typeOptions = computed(() => [
    { label: t('filters.allTypes'), value: '' },
    { label: t('transactions.income'), value: 'income' },
    { label: t('transactions.expense'), value: 'expense' },
]);

const currencyOptions = computed(() => [
    { label: t('filters.allCurrencies'), value: '' },
    { label: 'UZS', value: 'uzs' },
    { label: 'USD', value: 'usd' },
    { label: 'EUR', value: 'eur' },
    { label: 'RUB', value: 'rub' },
]);

const categoriesOptions = computed(() => {
    return [{ id: '', name: t('filters.allCategories') }, ...categories.value];
});

const formData = ref<{
    type: string;
    category_id: string;
    currency: string;
    start_date: string;
    end_date: string;
    search: string;
}>({
    type: '',
    category_id: '',
    currency: '',
    start_date: '',
    end_date: '',
    search: '',
});

watch(() => props.visible, (newValue) => {
    localVisible.value = newValue;
    if (newValue && props.currentFilters) {
        formData.value = {
            type: props.currentFilters.type || '',
            category_id: props.currentFilters.category_id || '',
            currency: props.currentFilters.currency || '',
            start_date: formatDatetimeToDate(props.currentFilters.start_date || ''),
            end_date: formatDatetimeToDate(props.currentFilters.end_date || ''),
            search: props.currentFilters.search || '',
        };
    } else if (!newValue) {
        resetForm();
    }
});

watch(() => props.currentFilters, (newFilters) => {
    if (newFilters && localVisible.value) {
        formData.value = {
            type: newFilters.type || '',
            category_id: newFilters.category_id || '',
            currency: newFilters.currency || '',
            start_date: formatDatetimeToDate(newFilters.start_date || ''),
            end_date: formatDatetimeToDate(newFilters.end_date || ''),
            search: newFilters.search || '',
        };
    }
});

const handleVisibilityChange = (value: boolean) => {
    localVisible.value = value;
    emit('update:visible', value);
    if (!value) {
        resetForm();
    }
};

const resetForm = () => {
    formData.value = {
        type: '',
        category_id: '',
        currency: '',
        start_date: '',
        end_date: '',
        search: '',
    };
};

const handleReset = () => {
    resetForm();
    emit('reset');
    localVisible.value = false;
    emit('update:visible', false);
};

const handleSubmit = () => {
    // Убираем пустые строки и undefined значения
    const filters: GetTransactionsParams = {};
    if (formData.value.type && formData.value.type.trim() !== '') {
        filters.type = formData.value.type as 'income' | 'expense';
    }
    if (formData.value.category_id && formData.value.category_id.trim() !== '') {
        filters.category_id = formData.value.category_id;
    }
    if (formData.value.currency && formData.value.currency.trim() !== '') {
        filters.currency = formData.value.currency as 'uzs' | 'usd' | 'eur' | 'rub';
    }
    if (formData.value.start_date && formData.value.start_date.trim() !== '') {
        // Преобразуем дату в формат datetime для API (T00:00:00 для начала дня)
        filters.start_date = formatDateToAPIDatetime(formData.value.start_date, false);
    }
    if (formData.value.end_date && formData.value.end_date.trim() !== '') {
        // Преобразуем дату в формат datetime для API (T23:59:59 для конца дня)
        filters.end_date = formatDateToAPIDatetime(formData.value.end_date, true);
    }
    if (formData.value.search && formData.value.search.trim() !== '') {
        filters.search = formData.value.search;
    }

    emit('apply', filters);
    localVisible.value = false;
    emit('update:visible', false);
};
</script>

<style scoped lang="scss">
.transaction-filter-form {
    &__form-wrapper {
        display: flex;
        flex-direction: column;
        height: 100%;
    }

    &__title {
        font: var(--font-20-b);
        margin: 0;
    }

    &__form {
        display: flex;
        flex-direction: column;
        gap: 1.2rem;
        padding-bottom: 1.6rem;
    }

    &__form-section {
        display: flex;
        flex-direction: column;
        gap: 0.8rem;
    }

    &__footer {
        padding: 2rem 0 .6rem 0;
        border-top: 1px solid var(--border-light);
        margin-top: auto;
    }

    &__buttons {
        display: flex;
        gap: 1.2rem;
    }

    &__button {
        flex: 1;
    }
}
</style>
