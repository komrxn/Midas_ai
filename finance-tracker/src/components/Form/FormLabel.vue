<script setup lang="ts">
import { Message } from 'primevue';
import { loadingIcon } from '@/assets/icons/';

const props = defineProps<{
  label?: string
  for?: string
  errorMessage?: string
  labelClass?: string
  loading?: boolean
}>();
</script>

<template>
  <div class="form-label">
    <label
      v-if="props.label"
      :for="props.for"
      :class="props.labelClass"
    >
      <span v-html="props.label" />
      <span v-if="loading" class="rotate-animation" v-html="loadingIcon" />
    </label>
    <slot />
    <Message v-if="errorMessage" severity="error" class="w-full" size="small" variant="simple">
      {{ errorMessage }}
    </Message>
  </div>
</template>

<style scoped lang="scss">
.form-label {
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
  width: 100%;
  label {
    font: var(--font-14-r);
    cursor: pointer;
    display: flex;
    align-items: flex-start;
    gap: .5rem;
  }

  .rotate-animation {
    width: 1.4rem;
    height: 1.4rem;
  }

  &:has(input[type='checkbox']) {
    flex-direction: row-reverse;
    justify-content: flex-end;
    align-items: center;
  }
}
</style>
