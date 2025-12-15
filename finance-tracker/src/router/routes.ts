import type { RouteRecordRaw } from 'vue-router';

const routes: RouteRecordRaw[] = [

  {
    path: '/',
    name: 'main',
    component: () => import('@/pages/Main.vue'),
    meta: {
      layout: 'Default',
    },
  },

  {
    path: '/example',
    name: 'example',
    component: () => import('@/pages/Example.vue'),
    meta: {
      layout: 'Default',
    },
  },
  {
    path: '/limits',
    name: 'limits',
    component: () => import('@/pages/Limits.vue'),
    meta: {
      layout: 'Default',
    },
  },
  {
    path: '/categories',
    name: 'categories',
    component: () => import('@/pages/Categories.vue'),
    meta: {
      layout: 'Default',
    },
  },
  {
    path: '/debts',
    name: 'debts',
    component: () => import('@/pages/Debts.vue'),
    meta: {
      layout: 'Default',
    },
  },
  {
    path: '/analytics',
    name: 'analytics',
    component: () => import('@/pages/Analytics.vue'),
    meta: {
      layout: 'Default',
    },
  },
  {
    path: '/transactions',
    name: 'transactions',
    component: () => import('@/pages/Transactions.vue'),
    meta: {
      layout: 'Default',
    },
  },
  {
    path: '/settings',
    name: 'settings',
    component: () => import('@/pages/Settings.vue'),
    meta: {
      layout: 'Default',
    },
  },
  {
    path: '/status/:type',
    name: 'status',
    component: () => import('@/pages/StatusPage.vue'),
  },

  {
    path: '/:pathMatch(.*)*',
    name: 'not-found',
    component: () => import('@/pages/Page404.vue'),
    meta: {
      layout: 'Empty',
    },
  },
];

export default routes;
