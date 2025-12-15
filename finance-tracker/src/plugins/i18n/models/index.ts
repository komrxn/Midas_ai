import enIcon from '@/assets/icons/flags/en.svg?raw';
import ruIcon from '@/assets/icons/flags/ru.svg?raw';
import uzIcon from '@/assets/icons/flags/uz.svg?raw';

export type TLangs = 'ru-RU' | 'en-US' | 'uz-UZ';
export const DEFAULT_LANGUAGE: TLangs = 'ru-RU';

const LOCAL_STORAGE_LOCALE_KEY = 'locale';

export const getCurrentLocale = () => {
  return localStorage.getItem(LOCAL_STORAGE_LOCALE_KEY) as TLangs || DEFAULT_LANGUAGE;
};

export const setCurrentLocale = (value: TLangs) => {
  localStorage.setItem(LOCAL_STORAGE_LOCALE_KEY, value);
  document.documentElement.lang = value;
};

export const flagIcons: Record<TLangs, string> = {
  'en-US': enIcon,
  'ru-RU': ruIcon,
  'uz-UZ': uzIcon,
};

export const langNames: Record<TLangs, string> = {
  'en-US': 'Eng',
  'ru-RU': 'Рус',
  'uz-UZ': 'O‘z',
};

export const smsErrorsEnum: Record<string, Record<TLangs, string>> = {
  WRONG_OTP: {
    'ru-RU': 'Неверный код подтверждения',
    'en-US': 'Invalid verification code',
    'uz-UZ': 'Noto‘g‘ri tasdiqlash kodi',
  },
  TOO_MANY_TRIES: {
    'ru-RU': 'Превышено количество попыток',
    'en-US': 'Too many attempts',
    'uz-UZ': 'Urinishlar soni cheklangan',
  },
  TOO_MANY_SMS: {
    'ru-RU': 'Отправлено слишком много SMS на номер',
    'en-US': 'Too many SMS sent to the number',
    'uz-UZ': 'Raqamga juda ko‘p SMS yuborildi',
  },
  INVALID_BODY: {
    'ru-RU': 'Неверное тело запроса',
    'en-US': 'Invalid request body',
    'uz-UZ': 'So‘rov tanasi noto‘g‘ri',
  },
  OTP_NOT_FOUND: {
    'ru-RU': 'Код подтверждения не найден',
    'en-US': 'Verification code not found',
    'uz-UZ': 'Tasdiqlash kodi topilmadi',
  },
  GATEWAY_UNAVAILABLE: {
    'ru-RU': 'СМС-шлюз недоступен',
    'en-US': 'SMS gateway unavailable',
    'uz-UZ': 'SMS shlyuzi mavjud emas',
  },
};
