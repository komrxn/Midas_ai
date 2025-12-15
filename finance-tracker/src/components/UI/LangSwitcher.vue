<script setup lang="ts">
import type { TLangs } from '@/plugins/i18n/models';
import { Select } from 'primevue';
import { computed } from 'vue';
import { useI18n } from 'vue-i18n';
import VIcon from '@/components/UI/VIcon.vue';
import { locales } from '@/plugins/i18n';
import { flagIcons, langNames, setCurrentLocale } from '@/plugins/i18n/models';

const { locale } = useI18n();

const selectedLang = computed(() => {
  return {
    name: langNames[locale.value as TLangs],
    icon: flagIcons[locale.value as TLangs],
  };
});

const lang = computed({
  get() {
    return locale.value;
  },
  set(value: TLangs) {
    setCurrentLocale(value);
    locale.value = value;
    document.documentElement.lang = value;
  },
});
</script>

<template>
  <div class="langs">
    <Select v-model="lang" :options="locales" option-value="value" option-label="name" class="lang-switcher">
      <template #value>
        <div class="select-item">
          <VIcon :icon="selectedLang.icon" class="no-fill icon" />
          {{ selectedLang.name }}
        </div>
      </template>

      <template #option="slotProps">
        <div class="select-item">
          <VIcon :icon="slotProps.option.icon" class="no-fill icon" />
          {{ slotProps.option.name }}
        </div>
      </template>
    </Select>
  </div>
</template>

<style scoped lang="scss">
.lang-switcher {
  --p-select-dropdown-width: 2.6rem;
  --p-select-padding-y: 1rem;
  --p-select-padding-x: .5rem;
  --p-icon-size: 1rem;
  --p-select-background: transparent;
  border: 0 !important;
  box-shadow: none !important;
  width: 100%;

  @include media-max($mobile) {
    --p-select-padding-x: 0;
  }

  :deep(.p-select-dropdown) {
    background: var(--gold-card-bg);
    border: 1px solid var(--gold-border);
    border-radius: 0.8rem;
    box-shadow: var(--gold-shadow);
    color: currentColor;
  }

  :deep(.p-select-trigger) {
    background: var(--card-accent);
    border: 1px solid var(--border-light);
    border-radius: 0.8rem;
    padding: 0.8rem 1.2rem;
    transition: all 0.3s ease;

    &:hover {
      background: var(--card-hover);
      border-color: var(--border-medium);
    }
  }
}

.select-item {
  display: flex;
  gap: 1rem;
  align-items: center;
  width: 100%;
  padding: 0.4rem 0;

  @include media-max($mobile) {
    font-size: 0;
    gap: 0;
    justify-content: center;
  }

  .icon {
    min-width: 2.5rem;
    width: 2.5rem;
    height: 2.5rem;
    flex-shrink: 0;
  }
}
</style>
