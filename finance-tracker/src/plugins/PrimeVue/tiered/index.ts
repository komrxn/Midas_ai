import { TieredMenuDesignTokens } from "@primeuix/themes/types/tieredmenu";
import { TieredMenuPassThroughOptions } from "primevue";

export const tieredMenuConfig = (): TieredMenuDesignTokens => {
    return {
        item: {
            padding: '1rem .8rem',
        },
        colorScheme: {
            light: {
                item: {
                    color: 'var(--text-color)',
                    focusColor: 'var(--text-color)',
                }
            },
            dark: {
                item: {
                    color: 'var(--text-color)',
                    focusColor: 'var(--text-color)',
                }
            }
        }
    }
};

export const tieredMenuPt = (): TieredMenuPassThroughOptions => {
    return {
        itemLabel: {
            class: 'font-12-r',
        }
    };
};
