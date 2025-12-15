<script setup lang="ts">
import { computed, onBeforeMount, onBeforeUnmount } from 'vue';

const props = defineProps<{
  duration: number
  size: number
}>();

const emit = defineEmits<{
  (e: 'loaded'): void
}>();

let timer: NodeJS.Timeout;
const timeout = props.duration * 400;

const sizeValue = computed(() => `${props.size}px`);
const strokeWidth = computed(() => `${props.size / 6}px`);
const progressBg = computed(() => `var(--p-green-500)`);

onBeforeMount(() => {
  timer = setTimeout(() => emit('loaded'), timeout);
});

onBeforeUnmount(() => {
  clearTimeout(timer);
});
</script>

<template>
  <svg class="circle" :style="{ '--duration': `${duration}s` }">
    <circle class="progress" :cx="props.size / 2" :cy="props.size / 2" :r="props.size / 2 - 5" />
  </svg>
</template>

<style scoped lang="scss">
.circle {
  min-width: v-bind(sizeValue);
  width: v-bind(sizeValue);
  height: v-bind(sizeValue);

  .progress {
    fill: none;
    stroke-width: v-bind(strokeWidth);
    stroke: v-bind(progressBg);
    stroke-linecap: round;
    stroke-dasharray: 326.56;
    stroke-dashoffset: 60;
    transform: rotate(-90deg);
    transform-origin: 50% 50%;
    animation: big var(--duration) ease-in-out;
  }
}
@keyframes big {
  from {
    stroke-dashoffset: 326.56;
  }
  to {
    stroke-dashoffset: 60;
  }
}
</style>
