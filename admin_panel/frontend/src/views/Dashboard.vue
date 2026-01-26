<script setup>
import { ref, onMounted } from 'vue';
import { useAuthStore } from '../stores/auth';
import { Users, CreditCard, Activity, TrendingUp } from 'lucide-vue-next';

const authStore = useAuthStore();

const stats = [
    { name: 'Total Users', value: 'Loading...', icon: Users, color: 'text-primary' },
    { name: 'Active Subscriptions', value: 'Loading...', icon: CreditCard, color: 'text-success' },
    { name: 'Monthly Revenue', value: 'Loading...', icon: TrendingUp, color: 'text-warning' },
    { name: 'System Health', value: '100%', icon: Activity, color: 'text-accent' },
];

// In a real app, fetch stats from API
</script>

<template>
    <div>
        <h1 class="text-3xl font-bold mb-8">
            Welcome back, <span class="bg-gradient-to-r from-primary to-secondary bg-clip-text text-transparent">{{ authStore.admin?.email?.split('@')[0] }}</span>
        </h1>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <div v-for="stat in stats" :key="stat.name" class="glass p-6 rounded-xl border border-white/5">
                <div class="flex items-center justify-between mb-4">
                    <span class="text-gray-400 font-medium">{{ stat.name }}</span>
                    <component :is="stat.icon" :class="`w-6 h-6 ${stat.color}`" />
                </div>
                <div class="text-2xl font-bold">{{ stat.value }}</div>
            </div>
        </div>

        <div class="mt-8 glass p-8 rounded-xl border border-white/5 text-center min-h-[400px] flex items-center justify-center flex-col">
            <Activity class="w-16 h-16 text-gray-600 mb-4 opacity-50" />
            <h3 class="text-xl font-medium text-gray-300">Analytics Dashboard</h3>
            <p class="text-gray-500 mt-2">Detailed charts and metrics coming soon.</p>
        </div>
    </div>
</template>
