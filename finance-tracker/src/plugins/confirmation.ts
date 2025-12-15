import type { ConfirmationTypes, IProps } from '@/store/confirmations/types';
import { useConfirmationsStore } from '@/store/confirmations';

const create = (type: ConfirmationTypes) => async (props: Omit<IProps, 'type'>): Promise<boolean> => {
  const { setConfirmation, closeConfirmation } = useConfirmationsStore();
  const { id, result } = await setConfirmation({ ...props, type });
  closeConfirmation(id);
  return result;
};

export const $confirm: Record<ConfirmationTypes, (props: Omit<IProps, 'type'>) => Promise<boolean>> = {
  default: create('default'),
  success: create('success'),
  info: create('info'),
  error: create('error'),
};
