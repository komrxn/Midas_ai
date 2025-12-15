import type { IConfirmation, IConfirmResponse, IProps } from '@/store/confirmations/types';
import { defineStore } from 'pinia';
import { h, ref } from 'vue';
import VConfirm from '@/components/UI/confirmations/VConfirm.vue';

export const useConfirmationsStore = defineStore('confirmations', () => {
  const confirmations = ref<IConfirmation[]>([]);
  const closeConfirmation = (id: number) => {
    confirmations.value = confirmations.value.filter(i => i.id !== id);
  };

  const setConfirmation = (props: IProps) => {
    const id = Date.now();
    return new Promise<IConfirmResponse>((resolve) => {
      const component = {
        id,
        component: h(VConfirm, {
          ...props,
          onAccept: () => resolve({ id, result: true }),
          onReject: () => resolve({ id, result: false }),
        }),
      };
      confirmations.value.push(component);
    });
  };

  return {
    confirmations,
    setConfirmation,
    closeConfirmation,
  };
});
