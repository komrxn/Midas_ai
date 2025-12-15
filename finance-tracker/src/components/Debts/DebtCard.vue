<template>
    <div class="debt-card">
        <div class="debt-card__content">
            <div class="debt-card__icon" :class="`debt-card__icon--${debt.type}`">
                <VIcon :icon="debt.type === DebtType.I_OWE ? arrowDownLeft : arrowUpRight" />
            </div>
            <div class="debt-card__info">
                <h3 class="debt-card__name">{{ debt.person_name }}</h3>
                <div class="debt-card__meta">
                    <span class="debt-card__amount" :class="`debt-card__amount--${debt.type}`">
                        {{ debt.type === DebtType.I_OWE ? '-' : '+' }}{{ formatAmount(debt.amount) }} {{
                            debt.currency.toUpperCase() }}
                    </span>
                    <span class="debt-card__status" :class="`debt-card__status--${debt.status}`">
                        {{ statusLabel }}
                    </span>
                </div>
                <p v-if="debt.description" class="debt-card__description">{{ debt.description }}</p>
                <p v-if="debt.due_date" class="debt-card__date">{{ t('debts.dueDate') }}: {{ formatDate(debt.due_date)
                }}</p>
            </div>
        </div>
        <div class="debt-card__menu-wrapper">
            <Button @click="toggleMenu" :icon="menuDots" text class="debt-card__menu-button" />
            <TieredMenu ref="menu" :model="menuItems" popup />
        </div>
    </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue';
import { useI18n } from 'vue-i18n';
import { Button, TieredMenu } from 'primevue';
import type { MenuItem } from 'primevue/menuitem';
import type { Debt } from '@/composables/Debts/types';
import { DebtType, DebtStatus } from '@/composables/Debts/types';
import { menuDots, arrowUpRight, arrowDownLeft } from '@/assets/icons';
import VIcon from '@/components/UI/VIcon.vue';
import { formatAmount, formatDate } from '@/utils';

const { t } = useI18n();

const props = defineProps<{
    debt: Debt;
}>();

const emit = defineEmits<{
    (e: 'remove'): void;
    (e: 'edit'): void;
    (e: 'mark-paid'): void;
}>();

const menu = ref();

const toggleMenu = (event: Event) => {
    menu.value.toggle(event);
};

const statusLabel = computed(() => {
    const labels: Record<DebtStatus, string> = {
        [DebtStatus.OPEN]: t('debts.open'),
        [DebtStatus.OVERDUE]: t('debts.overdue'),
        [DebtStatus.PAID]: t('debts.paid'),
    };
    return labels[props.debt.status];
});

const menuItems = computed<MenuItem[]>(() => [
    ...(props.debt.status !== DebtStatus.PAID ? [{
        label: t('debts.markAsPaid'),
        command: () => {
            emit('mark-paid');
        },
    }] : []),
    {
        label: t('common.edit'),
        command: () => {
            emit('edit');
        },
    },
    {
        label: t('common.delete'),
        command: () => {
            emit('remove');
        },
    },
]);

</script>

<style scoped lang="scss">
.debt-card {
    background: var(--gold-card-bg);
    border-radius: var(--radius-l);
    padding: 1.6rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1.2rem;
    border: 1px solid var(--gold-border);
    box-shadow: var(--gold-shadow);
    position: relative;
    overflow: hidden;

    &::before {
        content: '';
        position: absolute;
        inset: 0;
        border-radius: var(--radius-l);
        background: var(--gold-card-radial);
        pointer-events: none;
        opacity: 0;
        transition: opacity 0.3s ease;
    }

    &:hover {
        border-color: var(--gold-border-hover);
        box-shadow: var(--gold-shadow-hover);

        &::before {
            opacity: 1;
        }
    }

    &__content {
        display: flex;
        align-items: center;
        gap: 1.2rem;
        flex: 1;
        position: relative;
        z-index: 1;
    }

    &__icon {
        width: 4.4rem;
        height: 4.4rem;
        display: flex;
        justify-content: center;
        align-items: center;
        border-radius: 1.2rem;
        flex-shrink: 0;
        background: linear-gradient(135deg, rgba(255, 215, 0, 0.2) 0%, rgba(255, 165, 0, 0.15) 100%);
        border: 1px solid rgba(255, 215, 0, 0.3);
        box-shadow: 0 2px 8px rgba(255, 215, 0, 0.2);
        color: var(--primary-600);

        &--i_owe {
            background: linear-gradient(135deg, rgba(255, 65, 43, 0.15) 0%, rgba(255, 100, 82, 0.1) 100%);
            border-color: rgba(255, 65, 43, 0.3);
            color: rgb(255, 65, 43);
        }

        &--owe_me {
            background: linear-gradient(135deg, rgba(90, 204, 62, 0.15) 0%, rgba(138, 222, 116, 0.1) 100%);
            border-color: rgba(90, 204, 62, 0.3);
            color: rgb(90, 204, 62);
        }
    }

    &__info {
        display: flex;
        flex-direction: column;
        gap: 0.4rem;
        flex: 1;
        min-width: 0;
    }

    &__name {
        font: var(--font-16-b);
        margin: 0;
        color: var(--text-color);
    }

    &__meta {
        display: flex;
        align-items: center;
        gap: 0.8rem;
        flex-wrap: wrap;
    }

    &__amount {
        font: var(--font-16-b);
        color: var(--text-color);

        &--i_owe {
            color: rgb(255, 65, 43);
        }

        &--owe_me {
            color: rgb(90, 204, 62);
        }
    }

    &__status {
        font: var(--font-12-r);
        padding: 0.2rem 0.6rem;
        border-radius: var(--radius-s);
        background-color: var(--secondary-200);
        color: var(--text-color-secondary);

        &--open {
            background-color: rgba(90, 204, 62, 0.15);
            color: rgb(90, 204, 62);
        }

        &--overdue {
            background-color: rgba(255, 65, 43, 0.15);
            color: rgb(255, 65, 43);
        }

        &--paid {
            background-color: var(--secondary-200);
            color: var(--text-color-secondary);
        }
    }

    &__description {
        font: var(--font-12-r);
        color: var(--text-color-secondary);
        margin: 0;
    }

    &__date {
        font: var(--font-12-r);
        color: var(--text-color-secondary);
        margin: 0;
    }

    &__menu-wrapper {
        position: relative;
        flex-shrink: 0;
        z-index: 1;
    }

    &__menu-button {
        width: 2.4rem;
        height: 2.4rem;
    }
}
</style>
