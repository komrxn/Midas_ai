import type { StatusTypes } from '../types';
import rejected from '@/assets/icons/status/error.svg?raw';
import approved from '@/assets/icons/status/success.svg?raw';

export const statusIcons: Record<StatusTypes, string> = { approved, rejected, close: rejected };
