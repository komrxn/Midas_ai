<script setup>
import { computed } from 'vue';
import { useRoute } from 'vue-router';
import { useAuthStore } from '../stores/auth';
import { LayoutDashboard, Users, LogOut, Shield } from 'lucide-vue-next';

const route = useRoute();
const authStore = useAuthStore();

const navigation = [
  { name: 'Dashboard', href: '/dashboard', icon: LayoutDashboard },
  { name: 'Users', href: '/users', icon: Users },
  // { name: 'Admins', href: '/admins', icon: Shield },
];

const logout = () => {
    authStore.logout();
};
</script>

<template>
  <div class="min-h-screen flex bg-background text-gray-100">
    <!-- Sidebar -->
    <aside class="w-64 bg-surface border-r border-white/5 flex flex-col">
      <div class="h-16 flex items-center px-6 border-b border-white/5">
        <div class="text-xl font-bold bg-gradient-to-r from-primary to-secondary bg-clip-text text-transparent">
          Baraka Admin
        </div>
      </div>
      
      <nav class="flex-1 p-4 space-y-1">
        <router-link
          v-for="item in navigation"
          :key="item.name"
          :to="item.href"
          class="flex items-center px-4 py-3 rounded-lg text-sm font-medium transition-colors"
          :class="[
            route.path === item.href
              ? 'bg-primary/10 text-primary'
              : 'text-gray-400 hover:bg-white/5 hover:text-white'
          ]"
        >
          <component :is="item.icon" class="w-5 h-5 mr-3" />
          {{ item.name }}
        </router-link>
      </nav>
      
      <div class="p-4 border-t border-white/5">
        <div class="flex items-center px-4 py-2 mb-2">
            <div class="w-8 h-8 rounded-full bg-gradient-to-br from-primary to-secondary flex items-center justify-center text-xs font-bold">
                A
            </div>
            <div class="ml-3">
                <p class="text-sm font-medium text-white">{{ authStore.admin?.email }}</p>
                <p class="text-xs text-gray-500">Super Admin</p>
            </div>
        </div>
        <button 
          @click="logout"
          class="w-full flex items-center px-4 py-2 text-sm font-medium text-gray-400 hover:text-danger hover:bg-danger/10 rounded-lg transition-colors"
        >
          <LogOut class="w-5 h-5 mr-3" />
          Sign out
        </button>
      </div>
    </aside>

    <!-- Main content -->
    <main class="flex-1 flex flex-col min-w-0 overflow-hidden">
        <header class="h-16 glass flex items-center justify-between px-6 sticky top-0 z-10 w-full lg:hidden">
             <!-- Mobile header logic would go here -->
             <span>Menu</span>
        </header>

        <div class="flex-1 overflow-auto p-8">
            <router-view></router-view>
        </div>
    </main>
  </div>
</template>
