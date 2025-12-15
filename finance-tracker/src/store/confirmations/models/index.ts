import type { ConfirmationTypes } from '../types';
import error from '@/assets/icons/status/error.svg?raw';
import info from '@/assets/icons/status/info.svg?raw';
import success from '@/assets/icons/status/success.svg?raw';
import warning from '@/assets/icons/status/warning.svg?raw';

export const ConfirmationTypesColor: Record<ConfirmationTypes, string> = {
  default: 'var(--p-orange-500)',
  success: 'var(--p-green-500)',
  info: 'var(--p-sky-500)',
  error: 'var(--p-red-500)',
};

export const ConfirmationTypesIcon: Record<ConfirmationTypes, string> = {
  default: warning,
  error, info, success,
};
