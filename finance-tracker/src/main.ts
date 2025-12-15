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
  .use(ToastService)
  .mount('#app');

app.config.globalProperties.$formRules = formRules(i18n.global.t);
