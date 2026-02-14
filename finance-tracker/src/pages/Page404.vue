<script lang="ts" setup>
import { Button } from 'primevue';
import { useRouter } from 'vue-router';
import { useI18n } from 'vue-i18n';
import { backArrow } from '@/assets/icons';

const $router = useRouter();
const { t } = useI18n();
</script>

<template>
  <div class="error-page">
    <h1 class="font-30-b">
      {{ t('errors.notFound') }}
    </h1>

    <Button :label="t('common.backToMainPage')" text size="large" :icon="backArrow" @click="$router.push({ name: 'main' })" />
  </div>
</template>

<style scoped lang="scss">
.error-page {
  --p-button-gap: 1.2rem;

  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  gap: 1.2rem;

  :deep(.p-button-icon-svg) {
    height: 1.6rem;
  }
}
</style>
