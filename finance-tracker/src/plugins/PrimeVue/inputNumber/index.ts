import type { InputNumberDesignTokens } from '@primeuix/themes/types/inputnumber';
import type { InputNumberProps } from 'primevue';
import type { ButtonProps } from 'primevue/button';
import type { RendererElement, RendererNode, VNode } from 'vue';

const INPUT_BUTTONS_SEVERITY: ButtonProps['severity'] = 'primary';

export const inputNumberConfig = (): InputNumberDesignTokens => {
  return {
    button: {
      width: '5rem',
      color: `{button.${INPUT_BUTTONS_SEVERITY}.color}`,
      hoverColor: `{button.${INPUT_BUTTONS_SEVERITY}.hover.color}`,
      activeColor: `{button.${INPUT_BUTTONS_SEVERITY}.active.color}`,

      background: `{button.${INPUT_BUTTONS_SEVERITY}.background}`,
      hoverBackground: `{button.${INPUT_BUTTONS_SEVERITY}.hover.background}`,
      activeBackground: `{button.${INPUT_BUTTONS_SEVERITY}.active.background}`,

      borderColor: 'transparent',
      hoverBorderColor: 'transparent',
      activeBorderColor: 'transparent',
    },
  };
};

export const inputNumberPt = (instance?: VNode<RendererNode, RendererElement, InputNumberProps>) => {
  return {
    ...(instance?.props?.buttonLayout === 'horizontal' && {
      incrementButton: {
        innerHTML: '+',
        class: 'font-30-r',
      },
      decrementButton: {
        innerHTML: '-',
        class: 'font-30-r',
      },
    }),
  };
};
