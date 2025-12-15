import type en from '@/plugins/i18n/locales/en.ts';

export type MessageSchema = typeof en;

export type DeepKeyOf<TObj extends object> = {
  [K in keyof TObj & string]: TObj[K] extends object
    ? `${K}` | `${K}.${DeepKeyOf<TObj[K]>}`
    : `${K}`;
}[keyof TObj & string];
