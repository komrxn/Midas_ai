<script setup lang="ts">
import { Toast } from 'primevue';
import ConfirmationModal from '@/components/UI/confirmations/ConfirmationModal.vue';
import { useConfirmationsStore } from '@/store/confirmations';

const confirmationsStore = useConfirmationsStore();
</script>

<template>
  <component :is="$route.meta.layoutComponent">
    <slot />
  </component>

  <div v-if="confirmationsStore.confirmations.length" id="confirmations-wrapper">
    <ConfirmationModal v-for="confirmation in confirmationsStore.confirmations" :key="confirmation.id">
      <component :is="confirmation.component" />
    </ConfirmationModal>
  </div>

  <Toast />
</template>
