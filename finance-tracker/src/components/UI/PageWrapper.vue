<script setup lang="ts">
import { Button } from 'primevue';
import { computed, useSlots } from 'vue';
import { backArrow } from '@/assets/icons';

const props = defineProps<{
  title?: string
  backEnabled?: boolean
  bgColor?: string
  textColor?: string
}>();

const emit = defineEmits<{
  (e: 'back-button-clicked'): void
}>();

const bg = computed<string>(() => props.bgColor ? props.bgColor : 'var(--site-bg)');
const color = computed<string>(() => props.textColor ? props.textColor : 'var(--text-color)');

const slots = useSlots();
</script>

<template>
  <div class="page-wrapper">
    <div class="page-header content">
      <div class="side-items">
        <Button
          v-if="props.backEnabled"
          :icon="backArrow"
          text
          fluid
          class="back-button"
          @click="emit('back-button-clicked')"
        />
      </div>
      <div v-if="props.title" class="title">
        {{ props.title }}
      </div>
      <div class="side-items">
        <slot name="title-append" />
      </div>
    </div>
    <div class="page-content content">
      <slot />
    </div>

    <div class="page-footer content" :class="[slots['page-footer'] && 'has-content']">
      <slot name="page-footer" />
    </div>
  </div>
</template>

<style scoped lang="scss">
.content {
  --px: 2.4rem;
  @include media-max($mobile) {
    --px: 1.6rem;
  }
}
.page-wrapper {
  padding: 3rem 0 0;
  min-height: 100dvh;
  max-height: 100dvh;
  color: v-bind(color);
  background: v-bind(bg);
  position: relative;
  display: flex;
  flex-direction: column;

  .side-items {
    min-width: 9.5rem;
    max-width: 9.5rem;
  }
  @include media-max($mobile) {
    padding-top: 2.6rem;
    .side-items {
      min-width: 5rem;
      max-width: 5rem;
    }
  }
}
.page-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  position: relative;
  min-height: 4.4rem;
  padding-left: var(--px);
  padding-right: var(--px);
}
.back-button {
  --p-button-text-primary-color: var(--text-color);
  min-width: 3.5rem;
}

.title {
  flex-grow: 1;
  text-align: center;
  font: var(--font-22-b);
}

.page-content {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  position: relative;
  margin-top: 2rem;
  padding-left: var(--px);
  padding-right: var(--px);
  overflow-y: auto;
  overflow-x: hidden;
}

.page-footer {
  padding: 1.5rem var(--px) 0;
  color: v-bind(color);
  background: v-bind(bg);
  transition: var(--transition-fast);
  position: relative;
  @include media-max($mobile) {
    padding-top: 1.3rem;
  }
  &.has-content {
    border-radius: var(--radius-l) var(--radius-l) 0 0;
    box-shadow: 0 0 10px 0 rgba(0, 0, 0, 0.25);
    padding-bottom: 1.5rem;
    @include media-max($mobile) {
      padding-bottom: 1.3rem;
    }
  }
}
</style>
