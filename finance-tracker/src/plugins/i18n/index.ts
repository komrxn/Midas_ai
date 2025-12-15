import type { MessageSchema } from './types';
import { createI18n } from 'vue-i18n';

import en from './locales/en';
import ru from './locales/ru';
import uz from './locales/uz';

import { DEFAULT_LANGUAGE, flagIcons, getCurrentLocale, langNames } from './models';

export const i18n = createI18n<[MessageSchema], 'ru-RU' | 'en-US' | 'uz-UZ'>({
  legacy: false,
  locale: getCurrentLocale(),
  fallbackLocale: DEFAULT_LANGUAGE,
  globalInjection: true,
  warnHtmlMessage: false,
  messages: {
    'ru-RU': ru,
    'en-US': en,
    'uz-UZ': uz,
  },
});

export const locales = i18n.global.availableLocales.map((ln) => {
  return { name: langNames[ln], value: ln, icon: flagIcons[ln] };
});
