<script lang="ts" setup>
import { onBeforeMount } from 'vue';
import { useThemeMode } from '@/composables/UI/';
import AppLayout from '@/layouts/AppLayout.vue';
import { getCurrentLocale, setCurrentLocale } from '@/plugins/i18n/models';
// import { usePageTransitionStore } from '@/store/pageTransitionStore.ts';

const { setTheme } = useThemeMode();

onBeforeMount(() => {
  setCurrentLocale(getCurrentLocale());
  setTheme();
});

// const pageTransition = usePageTransitionStore();
</script>

<template>
  <div id="app">
    <!-- Show Telegram required message if not in Telegram -->
    <TelegramRequired v-if="!isTelegramMode && !hasToken" />
    
    <!-- Main app if in Telegram or has token -->
    <AppLayout v-else>
      <router-view v-slot="{ Component, route }">
        <!-- <transition :name="pageTransition.transitionName"> -->
          <component :is="Component" :key="route.path" />
        <!-- </transition> -->
      </router-view>
    </AppLayout>
  </div>
</template>

<style scoped lang="scss"></style>
