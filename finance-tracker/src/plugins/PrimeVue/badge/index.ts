import type { BadgeDesignTokens } from '@primeuix/themes/types/badge';
import type { BadgePassThroughOptions, BadgeProps } from 'primevue';
import type { RendererElement, RendererNode, VNode } from 'vue';

export const badgeConfig = (): BadgeDesignTokens => {
  return {
    colorScheme: {
      light: {
        primary: {
          background: 'var(--primary-500)',
          color: 'var(--primary-surface-color)',
        },
      },
      dark: {
        primary: {
          background: 'var(--primary-500)',
          color: 'var(--primary-surface-color)',
        },
      },
    },
    root: {
      height: '2.5rem',
      padding: '.4rem',
      minWidth: '2.5rem',
      borderRadius: 'var(--radius-m)',
    },
    sm: {
      height: 'auto',
      minWidth: '2rem',
    },
    lg: {
      height: '3rem',
      minWidth: '3rem',
    },
  };
};

export const badgePt = (instance: VNode<RendererNode, RendererElement, BadgeProps>): BadgePassThroughOptions => {
  return {
    root: {
      class: !instance.props?.size ? 'font-14-r' : instance.props.size === 'small' ? 'font-12-r' : 'font-18-r',
    },
  };
};
