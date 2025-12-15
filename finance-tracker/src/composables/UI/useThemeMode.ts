import { useLocalStorage, usePreferredDark } from '@vueuse/core';
import { computed } from 'vue';

type ThemeMode = 'light' | 'dark';

export const useThemeMode = () => {
  const isDarkPreferable = usePreferredDark();
  const themeMode = useLocalStorage<ThemeMode>('theme', isDarkPreferable.value ? 'dark' : 'light');

  const modes: ThemeMode[] = ['light', 'dark'];

  const setTheme = () => {
    document.documentElement.classList.remove('app-dark');
    if (themeMode.value === 'dark') {
      document.documentElement.classList.add('app-dark');
    }
    else {
      document.documentElement.classList.remove('app-dark');
    }
  };

  const modeModel = computed<ThemeMode>({
    get() {
      return themeMode.value;
    },
    set(value) {
      themeMode.value = value;
      setTheme();
    },
  });

  const isDark = computed(() => themeMode.value === 'dark');

  return {
    modes,
    isDark,
    modeModel,
    setTheme,
  };
};
