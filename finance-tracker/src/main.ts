import { LineChart, PieChart } from 'echarts/charts';
import { GridComponent, LegendComponent, TitleComponent, TooltipComponent } from 'echarts/components';
import { use } from 'echarts/core';
import { CanvasRenderer } from 'echarts/renderers';
import { createPinia } from 'pinia';

import PrimeVue from 'primevue/config';
import ToastService from 'primevue/toastservice';
import { createApp } from 'vue';
import App from '@/App.vue';
import { formRules } from '@/composables/Form/models';
import { i18n } from '@/plugins/i18n';
import { options } from '@/plugins/PrimeVue';
import router from '@/router/router.ts';
import '@/styles/main.scss';

use([
  CanvasRenderer,
  PieChart,
  LineChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent,
]);

const app = createApp(App);

const pinia = createPinia();

app
  .use(i18n)
  .use(pinia)
  .use(router)
  .use(PrimeVue, options)
  .use(ToastService);

app.config.globalProperties.$formRules = formRules(i18n.global.t);

// Telegram Web App automatic authentication
async function initApp() {
  const { authenticateViaTelegram, isTelegramWebApp } = await import('@/telegramAuth');

  if (isTelegramWebApp()) {
    console.log('[App] Running in Telegram WebApp, attempting authentication...');

    try {
      const token = await authenticateViaTelegram();

      if (token) {
        // Store token (you might already have a token service)
        localStorage.setItem('access_token', token);
        console.log('[App] ✅ Telegram authentication successful');
      }
      else {
        console.warn('[App] No initData from Telegram');
      }
    }
    catch (error) {
      console.error('[App] Telegram authentication failed:', error);
      // Fallback: user will see auth required screen
    }
  }
  else {
    console.log('[App] Not in Telegram WebApp');
  }

  // Mount app
  app.mount('#app');
}

initApp();
