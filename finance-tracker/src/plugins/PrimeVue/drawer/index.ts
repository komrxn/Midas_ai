import type { DrawerDesignTokens } from '@primeuix/themes/types/drawer';
import { DrawerPassThroughOptions, DrawerProps } from 'primevue';
import { RendererElement, RendererNode, VNode } from 'vue';

export const drawerConfig = (): DrawerDesignTokens => {
    return {
        root: {
            background: 'var(--card-accent)',
            borderColor: 'transparent',
        }
    };
};

export const drawerPt = (instance?: VNode<RendererNode, RendererElement, DrawerProps>): DrawerPassThroughOptions => {
    return {

    };
};
