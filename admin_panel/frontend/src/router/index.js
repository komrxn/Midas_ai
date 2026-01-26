import { createRouter, createWebHistory } from 'vue-router';
import { useAuthStore } from '../stores/auth';
import Login from '../views/Login.vue';
import Dashboard from '../views/Dashboard.vue';
import Users from '../views/Users.vue';

const routes = [
    { path: '/login', name: 'Login', component: Login, meta: { guest: true } },
    {
        path: '/',
        component: () => import('../components/Layout.vue'),
        meta: { requiresAuth: true },
        children: [
            { path: '', redirect: '/dashboard' },
            { path: 'dashboard', name: 'Dashboard', component: Dashboard },
            { path: 'users', name: 'Users', component: Users },
        ]
    }
];

const router = createRouter({
    history: createWebHistory('/adminpanel'), // Important: base path
    routes,
});

router.beforeEach((to, from, next) => {
    const authStore = useAuthStore();

    if (to.meta.requiresAuth && !authStore.isAuthenticated) {
        next('/login');
    } else if (to.meta.guest && authStore.isAuthenticated) {
        next('/dashboard');
    } else {
        next();
    }
});

export default router;
