<script setup>
import { ref } from 'vue';
import { useAuthStore } from '../stores/auth';
import { Loader2 } from 'lucide-vue-next';

const authStore = useAuthStore();
const email = ref('');
const password = ref('');
const loading = ref(false);
const error = ref('');

const handleSubmit = async () => {
  loading.value = true;
  error.value = '';
  try {
    await authStore.login(email.value, password.value);
  } catch (e) {
    error.value = e.response?.data?.detail || 'Login failed. Please check credentials.';
  } finally {
    loading.value = false;
  }
};
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-background relative overflow-hidden">
    <!-- Decor -->
    <div class="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-primary/20 rounded-full blur-[120px]"></div>
    <div class="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-secondary/20 rounded-full blur-[120px]"></div>

    <div class="w-full max-w-md glass p-8 rounded-2xl relative z-10 mx-4 border border-white/10 shadow-2xl">
      <div class="text-center mb-8">
        <h1 class="text-3xl font-bold bg-gradient-to-r from-primary to-secondary bg-clip-text text-transparent mb-2">
            Baraka Admin
        </h1>
        <p class="text-gray-400">Restricted Access Portal</p>
      </div>

      <form @submit.prevent="handleSubmit" class="space-y-6">
        <div>
          <label class="block text-sm font-medium text-gray-400 mb-2">Email</label>
          <input 
            v-model="email" 
            type="email" 
            required
            class="input-field"
            placeholder="admin@baraka.ai"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-400 mb-2">Password</label>
          <input 
            v-model="password" 
            type="password" 
            required
            class="input-field"
            placeholder="••••••••"
          />
        </div>

        <div v-if="error" class="p-3 bg-danger/10 border border-danger/20 rounded-lg text-danger text-sm text-center">
            {{ error }}
        </div>

        <button 
          type="submit" 
          :disabled="loading"
          class="w-full btn btn-primary flex items-center justify-center"
        >
          <Loader2 v-if="loading" class="w-5 h-5 animate-spin mr-2" />
          {{ loading ? 'Authenticating...' : 'Sign In' }}
        </button>
      </form>
      
      <div class="mt-8 text-center text-xs text-gray-600">
        Unauthorized access attempts are monitored and logged.
      </div>
    </div>
  </div>
</template>
