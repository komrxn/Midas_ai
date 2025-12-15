import type { ToastDesignTokens } from '@primeuix/themes/types/toast';
import type { ToastPassThroughOptions } from 'primevue';

export const toastConfig = (): ToastDesignTokens => {
  return {
    root: {
      width: '30rem',
    },
    content: {
      padding: '1.2rem 1.2rem 1.1rem',
      gap: '.87rem',
    },
    text: {
      gap: '.4rem',
    },
    icon: {
      size: '2rem',
    },
    closeIcon: {
      size: '1.4rem',
    },
    closeButton: {
      width: '2rem',
      height: '2rem',
    },

    colorScheme: {
      light: {
        success: {
          detailColor: '{stone.700}',
        },
        error: {
          detailColor: '{stone.700}',
        },
        info: {
          detailColor: '{stone.700}',
        },
        warn: {
          detailColor: '{stone.700}',
        },
      },
    },
  };
};

export const toastPt = (): ToastPassThroughOptions => {
  return {
    summary: {
      class: 'font-18-b',
    },
    detail: {
      class: 'font-14-r',
    },
  };
};
