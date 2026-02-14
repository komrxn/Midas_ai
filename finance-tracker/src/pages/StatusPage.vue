<script setup lang="ts">
import { Button } from 'primevue';
import { useI18n } from 'vue-i18n';
import { backArrow } from '@/assets/icons';
import PageWrapper from '@/components/UI/PageWrapper.vue';
import VIcon from '@/components/UI/VIcon.vue';
import { useStatusPage } from '@/composables/useStatusPage';

const { t } = useI18n();
const { pageTitle, pageDescription, pageIcon, pageType } = useStatusPage();
</script>

<template>
  <PageWrapper :title="pageTitle">
    <div class="status-page">
      <VIcon :icon="pageIcon" class="icon" span-bg="var(--p-red-500)" color="var(--white)" />

      <div class="font-16-r">
        {{ pageDescription }}
      </div>

      <Button
        v-if="pageType === 'approved'"
        :label="t('common.backToMainPage')"
        text
        size="large"
        :icon="backArrow"
        @click="$router.push({ name: 'main' })"
      />
    </div>
  </PageWrapper>
</template>

<style scoped lang="scss">
.status-page {
  padding-top: 3.6rem;
  display: flex;
  flex-direction: column;
  gap: 5rem;
  align-items: center;
  justify-content: center;
  text-align: center;
}
.icon {
  width: 15rem;
  border-radius: var(--radius-round);
}
</style>
