<script setup lang="ts">
import type { MaskaDetail } from 'maska';
import type { InputTextProps } from 'primevue';
import type { IEmits, InputMaskProps } from '@/composables/Form/types';
import { vMaska } from 'maska/vue';

import { InputText } from 'primevue';
import FormLabel from '@/components/Form/FormLabel.vue';
import { useFormField } from '@/composables/Form';

const props = defineProps<InputMaskProps<string, InputTextProps>>();
const emit = defineEmits<IEmits<string>>();

const { val, isMaskFieldCorrect, fieldValid, errorMessage } = useFormField<string, InputTextProps>(props, emit);

const maska = {
  mask: props.mask,
  eager: true,
  tokens: {
    A: { pattern: /[A-Z]/, transform: (chr: string) => chr.toUpperCase() },
  },
};

const maskInputHandler = (event: CustomEvent<MaskaDetail>) => {
  val.value = props.unmask ? event.detail.unmasked : event.detail.masked;
  isMaskFieldCorrect.value = event.detail.completed;
};
</script>

<template>
  <FormLabel :label="props.label" :error-message="!fieldValid ? errorMessage : ''" :loading="loading">
    <InputText
      v-maska="maska"
      v-bind="{ ...props, ...$attrs }"
      :invalid="!fieldValid"
      :disabled="loading"
      @maska="maskInputHandler"
    />
  </FormLabel>
</template>

<style scoped lang="scss"></style>
