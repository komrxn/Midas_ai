<script setup lang="ts"></script>

<template>
  <div class="app-inner">
    <slot />
  </div>
</template>

<style scoped lang="scss">
.app-inner {
  width: 100%;
  min-height: 100dvh;
  display: flex;
  flex-direction: column;
  position: relative;
  // overflow: hidden;
}
</style>
