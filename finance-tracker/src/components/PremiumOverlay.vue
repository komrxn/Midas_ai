<template>
  <div v-if="!isActive" class="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4">
    <div class="bg-white dark:bg-gray-800 rounded-2xl shadow-2xl max-w-md w-full p-6 text-center transform transition-all scale-100">
      <div class="mb-4 flex justify-center">
        <div class="w-16 h-16 bg-blue-100 dark:bg-blue-900/30 rounded-full flex items-center justify-center">
          <span class="text-3xl">🌟</span>
        </div>
      </div>
      
      <h3 class="text-xl font-bold mb-2 text-gray-900 dark:text-white">
        {{ $t('subscription.premium_required_title') }}
      </h3>
      
      <p class="text-gray-600 dark:text-gray-300 mb-6">
        {{ $t('subscription.premium_required_desc') }}
      </p>
      
      <div class="space-y-3">
        <button 
          @click="router.push('/subscription')" 
          class="w-full py-3 px-4 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-xl transition shadow-lg shadow-blue-500/30 flex items-center justify-center gap-2"
        >
          <span>{{ $t('subscription.activate_btn') }}</span>
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clip-rule="evenodd" />
          </svg>
        </button>
        
        <button 
          @click="router.push('/')"
          class="w-full py-3 px-4 bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 text-gray-700 dark:text-gray-200 font-medium rounded-xl transition"
        >
          {{ $t('common.cancel') }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useRouter } from 'vue-router';
import { useUserStore } from '@/store/userStore';

const router = useRouter();
const userStore = useUserStore();

const isActive = computed(() => {
  return userStore.user?.is_active || userStore.user?.is_premium;
});
</script>
