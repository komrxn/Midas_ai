import type { StatusTypes } from '@/composables/useStatusPage/types';
import { useI18n } from 'vue-i18n';
import { useRouter } from 'vue-router';
import { statusIcons } from '@/composables/useStatusPage/models';

export const useStatusPage = () => {
  const $router = useRouter();
  const { t } = useI18n();
  const pageType = ($router.currentRoute.value.params.type || 'close') as StatusTypes;

  const pageTitle = t(`statuses.${pageType}.title`);
  const pageDescription = t(`statuses.${pageType}.description`);
  const pageIcon = statusIcons[pageType];

  return { pageTitle, pageDescription, pageIcon, pageType };
};
