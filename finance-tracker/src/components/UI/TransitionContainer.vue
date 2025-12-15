<script setup lang="ts">
defineProps<{
  name: 'fade' | 'slide-in-right' | 'slide-in-left' | 'scale-fade'
  keyId?: string | number
}>();
</script>

<template>
  <div class="transition-container">
    <Transition :name="name">
      <div :key="keyId" class="transition-element">
        <slot />
      </div>
    </Transition>
  </div>
</template>

<style scoped lang="scss">
.transition-container {
  max-width: 100%;
  position: relative;
  .transition-element + .transition-element {
    position: absolute;
    inset: 0;
  }
}
</style>
