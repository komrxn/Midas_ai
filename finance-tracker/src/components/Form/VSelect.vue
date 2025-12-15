<script setup lang="ts">
import type { SelectProps } from 'primevue';
import type { IEmits, InputFieldProps } from '@/composables/Form/types';
import { Select } from 'primevue';

import FormLabel from '@/components/Form/FormLabel.vue';
import { useFormField } from '@/composables/Form';

const props = defineProps<InputFieldProps<string | number, SelectProps> & { modelValue?: string | number }>();
const emit = defineEmits<IEmits<string | number>>();

const { val, fieldValid, errorMessage } = useFormField<string | number, SelectProps>(props, emit);
</script>

<template>
  <FormLabel :label="props.label" :error-message="!fieldValid ? errorMessage : ''" :loading="loading">
    <Select v-bind="{ ...props, ...$attrs }" :model-value="val" :invalid="!fieldValid" :disabled="loading"
      @update:model-value="val = $event" />
  </FormLabel>
</template>

<style scoped lang="scss"></style>
