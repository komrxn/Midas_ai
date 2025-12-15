<script setup lang="ts">
import type { IEmits, IProps } from '@/store/confirmations/types';
import { Button, Card } from 'primevue';
import { computed } from 'vue';
import { useI18n } from 'vue-i18n';
import VIcon from '@/components/UI/VIcon.vue';
import { ConfirmationTypesColor, ConfirmationTypesIcon } from '@/store/confirmations/models';

const props = defineProps<IProps>();
const emit = defineEmits<IEmits>();
const { t } = useI18n();

const color = computed(() => ConfirmationTypesColor[props.type]);
const icon = computed(() => ConfirmationTypesIcon[props.type]);
</script>

<template>
  <Card class="card">
    <template #content>
      <div class="header-wrapper">
        <VIcon :icon="icon" :color="color" class="icon" />

        <h1 v-if="title" class="font-22-b">
          {{ t(title) }}
        </h1>
      </div>

      <div v-if="subtitle" class="subtitle">
        {{ t(subtitle) }}
      </div>

      <div class="buttons">
        <Button v-if="type === 'default'" fluid severity="secondary" @click="emit('reject')">
          {{ t('confirmations.reject') }}
        </Button>
        <Button fluid @click="emit('accept')">
          {{ type === 'default' ? t('confirmations.accept') : 'Оk' }}
        </Button>
      </div>
    </template>
  </Card>
</template>

<style scoped lang="scss">
.card {
  width: 100%;
  max-width: 36rem;
  :deep(.p-card-content) {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }
  .header-wrapper {
    display: flex;
    gap: 0.5rem;
    align-items: center;
    .icon {
      width: 4.5rem;
      min-width: 4.5rem;
    }
  }
  .subtitle {
    font: var(--font-16-r);
    line-height: 1.2;
  }
  .buttons {
    display: flex;
    gap: 1rem;
    padding-top: 1rem;
  }
}
</style>
