<script setup lang="ts">
import { Dialog } from 'primevue';
import { ref } from 'vue';

const visible = ref(true);
</script>

<template>
  <Dialog
    v-model:visible="visible"
    :closable="false"
    modal
    :show-header="false"
    class="confirmation-dialog"
  >
    <slot />
  </Dialog>
</template>

<style scoped lang="scss"></style>
