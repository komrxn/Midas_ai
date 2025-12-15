import { ref } from 'vue';

export const useToggle = (initialValue?: boolean) => {
  const show = ref<boolean>(initialValue || false);

  const open = () => {
    show.value = true;
  };

  const close = () => {
    show.value = false;
  };

  const toggle = () => {
    show.value = !show.value;
  };

  return { show, open, close, toggle };
};
