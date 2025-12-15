import type { CardDesignTokens } from '@primeuix/themes/types/card';

export const cardConfig = (): CardDesignTokens => {
  return {
    colorScheme: {
      light: {
        root: {
          color: 'var(--black)',
        },
      },
      dark: {
        root: {
          color: 'var(--white)',
        },
      },
    },
  };
};
