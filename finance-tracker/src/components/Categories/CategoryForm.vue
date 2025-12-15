<template>
    <VDrawer v-model:visible="localVisible" @update:visible="handleVisibilityChange">
        <template #header>
            <h2 class="category-form__title">{{ isEditMode ? t('categories.editCategory') : t('categories.addCategory') }}</h2>
        </template>

        <VForm @submit-form="handleSubmit" class="category-form__form-wrapper">

            <div class="category-form__form">
                <div class="category-form__form-section">
                    <VSelect v-model="formData.type" :options="typeOptions" option-label="label" option-value="value"
                        :placeholder="t('categories.selectCategoryType')" :label="t('categories.type')" :rules="typeRules" size="small"
                        class="font-14-r" :disabled="isEditMode && isDefaultCategory" />
                </div>

                <div class="category-form__form-section">
                    <VInputText v-model="formData.name" :placeholder="t('categories.enterCategoryName')" :label="t('categories.name')"
                        :rules="nameRules" size="small" class="font-14-r" />
                </div>

                <div class="category-form__form-section">
                    <VInputText v-model="formData.icon" :placeholder="t('categories.enterIcon')" :label="t('categories.icon')"
                        size="small" class="font-14-r" />
                </div>

                <!-- <div class="category-form__form-section">
                    <div class="category-form__color-wrapper">
                        <label class="category-form__form-info-label">Цвет</label>
                        <div class="category-form__color-input-wrapper">
                            <input v-model="formData.color" type="color" class="category-form__color-input" />
                            <VInputText v-model="formData.color" placeholder="#2ECC71" label="" size="small"
                                class="font-14-r" />
                        </div>
                    </div>
                </div> -->
            </div>

            <div class="category-form__footer">
                <Button :label="isEditMode ? t('common.save') : t('categories.saveCategory')" type="submit" fluid
                    severity="primary" class="category-form__submit" />
            </div>
        </VForm>
    </VDrawer>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue';
import { useI18n } from 'vue-i18n';
import { Button } from 'primevue';
import VDrawer from '@/components/UI/VDrawer.vue';
import VForm from '@/components/Form/VForm.vue';
import VInputText from '@/components/Form/VInputText.vue';
import VSelect from '@/components/Form/VSelect.vue';
import type { FormRule } from '@/composables/Form/types';
import type { CategoryFormData } from '@/composables/Categories/types';
import { CategoryType } from '@/composables/Categories/types';

const { t } = useI18n();

const props = withDefaults(
    defineProps<{
        visible: boolean;
        editData?: CategoryFormData & { isDefault?: boolean } | null;
    }>(),
    {
        editData: null,
    }
);

const emit = defineEmits<{
    (e: 'update:visible', value: boolean): void;
    (e: 'submit', data: CategoryFormData): void;
}>();

const localVisible = ref(props.visible);
const isEditMode = computed(() => !!props.editData);
const isDefaultCategory = computed(() => props.editData?.isDefault || false);

const typeOptions = computed(() => [
    { label: t('transactions.income'), value: CategoryType.INCOME },
    { label: t('transactions.expense'), value: CategoryType.EXPENSE },
]);

watch(() => props.visible, (newValue) => {
    localVisible.value = newValue;
    if (newValue && props.editData) {
        formData.value = {
            name: props.editData.name,
            type: props.editData.type,
            icon: props.editData.icon || '',
            color: props.editData.color || '#2ECC71',
        };
    } else if (!newValue) {
        resetForm();
    }
});

watch(() => props.editData, (newData) => {
    if (newData && localVisible.value) {
        formData.value = {
            name: newData.name,
            type: newData.type,
            icon: newData.icon || '',
            color: newData.color || '#2ECC71',
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

const formData = ref<CategoryFormData>({
    name: '',
    type: CategoryType.EXPENSE,
    icon: '',
    color: '#2ECC71',
});

const nameRules: FormRule<string>[] = [
    (value) => {
        if (!value || value.trim().length === 0) return t('categories.enterCategoryNameError');
        if (value.trim().length < 2) return t('categories.categoryNameMinLength');
        return true;
    },
];

const typeRules: FormRule<string | number>[] = [
    (value) => {
        if (!value) return t('categories.selectCategoryType');
        return true;
    },
];

const resetForm = () => {
    formData.value = {
        name: '',
        type: CategoryType.EXPENSE,
        icon: '',
        color: '#2ECC71',
    };
};

const handleSubmit = () => {
    emit('submit', { ...formData.value });
    localVisible.value = false;
    emit('update:visible', false);
    resetForm();
};

</script>

<style scoped lang="scss">
.category-form {
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

    &__form-info {
        padding: 1.6rem;
        background-color: var(--card-default);
        border-radius: var(--radius-l);
    }

    &__form-info-label {
        font: var(--font-14-r);
        display: block;
        margin-bottom: 0.8rem;
        color: var(--text-color);
    }

    &__form-info-text {
        font: var(--font-12-r);
        color: var(--text-color-secondary);
        margin: 0;
    }

    &__checkbox-wrapper {
        display: flex;
        align-items: center;
        gap: 0.8rem;
        padding: 1rem 0 0 0;
    }

    &__checkbox-label {
        font: var(--font-14-r);
        color: var(--text-color);
        cursor: pointer;
    }

    &__footer {
        padding: 2rem 0 .6rem 0;
        border-top: 1px solid var(--border-light);
        margin-top: auto;
    }

    &__submit {
        width: 100%;
    }

    &__color-wrapper {
        display: flex;
        flex-direction: column;
        gap: 0.8rem;
    }

    &__color-input-wrapper {
        display: flex;
        align-items: center;
        gap: 1rem;
    }

    &__color-input {
        width: 5rem;
        height: 3.6rem;
        border: 1px solid var(--border-light);
        border-radius: var(--radius-s);
        cursor: pointer;
        background: transparent;
    }
}
</style>
