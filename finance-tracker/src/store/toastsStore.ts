import type { ToastMessageOptions } from 'primevue/toast';
import { defineStore } from 'pinia';
import { useToast } from 'primevue/usetoast';
import { h } from 'vue';
import VIcon from '@/components/UI/VIcon.vue';
import { i18n } from '@/plugins/i18n';
import { getCurrentLocale, smsErrorsEnum } from '@/plugins/i18n/models';

type ToastsSeverity = Exclude<ToastMessageOptions['severity'], undefined>;

export const useToastStore = defineStore('toast', () => {
  const toast = useToast();
  const life = 4000;

  const defaultTitles: Partial<Record<ToastsSeverity, string>> = {
    success: 'toast.success',
    error: 'toast.error',
    warn: 'toast.warn',
    info: 'toast.info',
  };

  const fireToast = (severity: ToastsSeverity, title: string, text?: string, icon?: string) => {
    const summary = text ? title : i18n.global.t(defaultTitles[severity]!);
    const message = text || title;

    const detail = (message && smsErrorsEnum[message]) ? smsErrorsEnum[message][getCurrentLocale()] : message;

    const toastOptions: any = { severity, summary, detail, life };
    
    if (icon) {
      toastOptions.icon = () => h(VIcon, { icon });
    }

    toast.add(toastOptions);
  };

  return {
    success: (title: string, text?: string, icon?: string) => fireToast('success', title, text, icon),
    info: (title: string, text?: string, icon?: string) => fireToast('info', title, text, icon),
    warning: (title: string, text?: string, icon?: string) => fireToast('warn', title, text, icon),
    error: (title: string, text?: string, icon?: string) => fireToast('error', title, text, icon),
  };
});
