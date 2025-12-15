import type { ComputedRef, InjectionKey, Ref } from 'vue';

export type FormRule<V> = (value: V) => string | boolean;

export const IS_VALIDATED: InjectionKey<Ref<boolean>> = Symbol('isValidated');
export const ADD_FORM_VALIDATION_RULE: InjectionKey<(id: string, value: ComputedRef<boolean>) => () => boolean> = Symbol('addValidationToForm');

export interface IFormField<V extends string | number> {
  modelValue: V

  label?: string
  rules?: Array<FormRule<V>>
  loading?: boolean
}

export type InputFieldProps<V extends string | number, P> = IFormField<V> & /* @vue-ignore */ P;
export type InputMaskProps<T extends string, P> = InputFieldProps<T, P> & { mask: string, unmask?: boolean };

export interface IEmits<T> {
  (e: 'update:modelValue', value: T): void
}
