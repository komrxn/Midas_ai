<script setup lang="ts">
import { computed } from 'vue';

const props = defineProps<{
  icon: string
  spanBg?: string
  color?: string
  noFill?: boolean
}>();

const colorVal = computed(() => props.color || 'unset');
const background = computed(() => props.spanBg || 'transparent');
</script>

<template>
  <span
    :style="{ color: colorVal, background }"
    :class="[noFill && 'no-fill']"
    v-html="props.icon"
  />
</template>

<style scoped lang="scss">
span {
  display: inline-block;
  font-size: 0;
  overflow: hidden;
  text-align: center;
  :deep(svg) {
    width: auto;
    max-width: 100%;
    max-height: 100%;
    transition: var(--transition-fast);

    &[fill]:not([fill='none']) {
      fill: currentColor;
    }
  }
  &:not(.no-fill) {
    :deep(svg) {
      [fill]:not([fill='none']) {
        fill: currentColor;
      }
      [stroke]:not([stroke='none']) {
        stroke: currentColor;
      }
    }
  }
}
</style>
