import { ref, watch } from 'vue';

export const useFetchStates = () => {
  const error = ref<boolean>(false);
  const loading = ref<boolean>(false);

  const posting = ref<boolean>(false);
  const posted = ref<boolean>(false);

  const deleting = ref<boolean>(false);
  const deleted = ref<boolean>(false);

  watch(posted, async (value) => {
    if (!value) return;
    await new Promise(resolve => setTimeout(resolve, 1500));
    posted.value = false;
  });

  watch(deleted, async (value) => {
    if (!value) return;
    await new Promise(resolve => setTimeout(resolve, 1500));
    deleted.value = false;
  });

  return {
    error,
    loading,

    posting,
    posted,

    deleting,
    deleted,
  };
};
