import type { SelectDesignTokens } from '@primeuix/themes/types/select';
import type { SelectPassThroughOptions, SelectProps } from 'primevue';
import type { RendererElement, RendererNode, VNode } from 'vue';

export const selectConfig = (): SelectDesignTokens => {
  return {
    list: {
      padding: '0',
    },
    option: {
      padding: '1rem',
    },

    colorScheme: {
      light: {
        option: {
          color: 'var(--black)',
          focusColor: 'var(--black)',
          selectedColor: 'var(--primary-surface-color)',
          selectedFocusColor: 'var(--primary-surface-color)',
          focusBackground: 'var(--secondary-300)',
          selectedBackground: 'var(--primary-500)',
          selectedFocusBackground: 'var(--primary-500)',
        },
      },
      dark: {
        option: {
          color: 'var(--white)',
        },
      },
    },
  };
};

export const selectPt = (instance?: VNode<RendererNode, RendererElement, SelectProps>): SelectPassThroughOptions => {
  return {
    label: {
      class: (!instance || !instance.props?.size) ? 'font-14-b' : instance.props.size === 'small' ? 'font-12-r' : 'font-18-b',
    },
    option: {
      class: (!instance || !instance.props?.size) ? 'font-14-b' : instance.props.size === 'small' ? 'font-12-r' : 'font-18-b',
    },
  };
};
