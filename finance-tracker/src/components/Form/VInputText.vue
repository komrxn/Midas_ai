<script setup lang="ts">
import type { InputTextProps } from 'primevue';
import type { IEmits, InputFieldProps } from '@/composables/Form/types';
import { InputText } from 'primevue';

import FormLabel from '@/components/Form/FormLabel.vue';
import { useFormField } from '@/composables/Form';

const props = defineProps<InputFieldProps<string, InputTextProps>>();
const emit = defineEmits<IEmits<string>>();

const { val, fieldValid, errorMessage } = useFormField<string, InputTextProps>(props, emit);
</script>

<template>
  <FormLabel :label="props.label" :error-message="!fieldValid ? errorMessage : ''" :loading="loading">
    <InputText v-bind="{ ...props, ...$attrs }" v-model="val" :invalid="!fieldValid" :disabled="loading" />
  </FormLabel>
</template>

<style scoped lang="scss"></style>
