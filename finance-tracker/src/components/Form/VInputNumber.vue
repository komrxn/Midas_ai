<script setup lang="ts">
import type { InputNumberProps } from 'primevue';
import type { IEmits, InputFieldProps } from '@/composables/Form/types';
import { InputNumber } from 'primevue';
import FormLabel from '@/components/Form/FormLabel.vue';

import { useFormField } from '@/composables/Form';

const props = defineProps<InputFieldProps<number, InputNumberProps>>();
const emit = defineEmits<IEmits<number>>();

const { val, fieldValid, errorMessage } = useFormField<number, InputNumberProps>(props, emit);
</script>

<template>
  <FormLabel :label="props.label" :error-message="!fieldValid ? errorMessage : ''" :loading="loading">
    <InputNumber
      v-bind="{ ...props, ...$attrs }"
      :model-value="val"
      :invalid="!fieldValid"
      :disabled="loading"
      locale="ru-RU"
      @input="$val => val = ($val.value as number)"
    />
  </FormLabel>
</template>

<style scoped lang="scss"></style>
