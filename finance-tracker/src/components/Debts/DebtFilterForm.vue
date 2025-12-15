<template>
    <VDrawer v-model:visible="localVisible" @update:visible="handleVisibilityChange">
        <template #header>
            <h2 class="debt-filter-form__title">{{ t('debts.debtFilters') }}</h2>
        </template>

        <VForm @submit-form="handleSubmit" class="debt-filter-form__form-wrapper">
            <div class="debt-filter-form__form">
                <div class="debt-filter-form__form-section">
                    <VSelect v-model="formData.type" :options="typeOptions" option-label="label" option-value="value"
                        :placeholder="t('debts.allTypes')" :label="t('debts.type')" size="small" class="font-14-r" />
                </div>

                <div class="debt-filter-form__form-section">
                    <VSelect v-model="formData.status" :options="statusOptions" option-label="label" option-value="value"
                        :placeholder="t('debts.allStatuses')" :label="t('debts.status')" size="small" class="font-14-r" />
                </div>
            </div>

            <div class="debt-filter-form__footer">
                <div class="debt-filter-form__buttons">
                    <Button :label="t('filters.reset')" severity="secondary" outlined fluid @click="handleReset"
                        class="debt-filter-form__button" />
                    <Button :label="t('filters.apply')" type="submit" fluid severity="primary"
                        class="debt-filter-form__button" />
                </div>
            </div>
        </VForm>
    </VDrawer>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue';
import { useI18n } from 'vue-i18n';
import { Button } from 'primevue';
import VDrawer from '@/components/UI/VDrawer.vue';
import VForm from '@/components/Form/VForm.vue';
import VSelect from '@/components/Form/VSelect.vue';
import type { DebtType, DebtStatus } from '@/composables/Debts/types';
import { useDebtTypeFilterOptions, useDebtStatusFilterOptions } from '@/composables/Debts/data';

const { t } = useI18n();

export interface DebtFilters {
    type?: DebtType | 'all';
    status?: DebtStatus | 'all';
}

const props = defineProps<{
    visible: boolean;
    currentFilters?: DebtFilters;
}>();

const emit = defineEmits<{
    (e: 'update:visible', value: boolean): void;
    (e: 'apply', filters: DebtFilters): void;
    (e: 'reset'): void;
}>();

const localVisible = ref(props.visible);

const typeOptions = useDebtTypeFilterOptions();
const statusOptions = useDebtStatusFilterOptions();

const formData = ref<{
    type: DebtType | 'all';
    status: DebtStatus | 'all';
}>({
    type: 'all',
    status: 'all',
});

watch(() => props.visible, (newValue) => {
    localVisible.value = newValue;
    if (newValue && props.currentFilters) {
        formData.value = {
            type: props.currentFilters.type || 'all',
            status: props.currentFilters.status || 'all',
        };
    } else if (!newValue) {
        resetForm();
    }
});

watch(() => props.currentFilters, (newFilters) => {
    if (newFilters && localVisible.value) {
        formData.value = {
            type: newFilters.type || 'all',
            status: newFilters.status || 'all',
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
        type: 'all',
        status: 'all',
    };
};

const handleReset = () => {
    resetForm();
    emit('reset');
    localVisible.value = false;
    emit('update:visible', false);
};

const handleSubmit = () => {
    const filters: DebtFilters = {};
    if (formData.value.type && formData.value.type !== 'all') {
        filters.type = formData.value.type;
    }
    if (formData.value.status && formData.value.status !== 'all') {
        filters.status = formData.value.status;
    }

    emit('apply', filters);
    localVisible.value = false;
    emit('update:visible', false);
};
</script>

<style scoped lang="scss">
.debt-filter-form {
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

