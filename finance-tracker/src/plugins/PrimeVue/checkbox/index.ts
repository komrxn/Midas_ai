import type { CheckboxDesignTokens } from '@primeuix/themes/types/checkbox';

export const checkboxConfig = (): CheckboxDesignTokens => {
  return {
    root: {
      width: '2rem',
      height: '2rem',
      borderColor: 'var(--secondary-600)',
      hoverBorderColor: 'var(--primary-500)',
    },
    icon: {
      size: '1.2rem',
      checkedColor: 'var(--primary-surface-color)',
    },
  };
};
