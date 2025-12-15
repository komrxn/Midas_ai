import type { MessageDesignTokens } from '@primeuix/themes/types/message';

export const messageConfig = (): MessageDesignTokens => {
  return {
    root: {
      borderRadius: '.7rem',
    },

    content: {
      padding: '1.2rem 2rem',
      sm: {
        padding: '0.6rem 0.8rem 0.5rem',
      },
    },
    text: {
      fontSize: '1.4rem',
      sm: {
        fontSize: '1.2rem',
      },
    },
  };
};
