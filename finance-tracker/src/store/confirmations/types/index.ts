import type { VNode } from 'vue';
import type { DeepKeyOf, MessageSchema } from '@/plugins/i18n/types';

export interface IConfirmation {
  id: number
  component: VNode
}

export interface IConfirmResponse {
  id: number
  result: boolean
}

export type ConfirmationTypes = 'default' | 'success' | 'info' | 'error';

export interface IProps {
  title?: DeepKeyOf<MessageSchema>
  subtitle?: DeepKeyOf<MessageSchema>
  type: ConfirmationTypes
}

export interface IEmits {
  (e: 'accept'): void
  (e: 'reject'): void
}
