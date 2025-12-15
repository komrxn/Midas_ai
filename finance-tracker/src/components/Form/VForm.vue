<script setup lang="ts">
import type { ComputedRef } from 'vue';
import { provide } from 'vue';

import { ADD_FORM_VALIDATION_RULE, IS_VALIDATED } from '@/composables/Form/types';
import { useToggle } from '@/composables/UI';

const emit = defineEmits<{
  (e: 'submit-form'): void
}>();

const fieldsStatuses: Map<string, ComputedRef<boolean>> = new Map();
const { show: isValidated, open: setIsValidated, close: resetIsValidated } = useToggle();

const addValidationToForm = (id: string, state: ComputedRef<boolean>): () => boolean => {
  fieldsStatuses.set(id, state);
  return () => fieldsStatuses.delete(id);
};

const isInvalid = () => {
  return [...fieldsStatuses.keys()].some(id => fieldsStatuses.get(id) && !fieldsStatuses.get(id)!.value);
};

provide(IS_VALIDATED, isValidated);
provide(ADD_FORM_VALIDATION_RULE, addValidationToForm);

const submitHandler = () => {
  setIsValidated();
  if (isInvalid()) return;
  emit('submit-form');
  resetIsValidated();
};
</script>

<template>
  <form @submit.prevent="submitHandler">
    <slot />
  </form>
</template>

<style scoped lang="scss">
form {
  width: 100%;
}
</style>
