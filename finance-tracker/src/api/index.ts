import type { AxiosError } from 'axios';
import { useCookies } from '@vueuse/integrations/useCookies';
import axios from 'axios';
import { useToastStore } from '@/store/toastsStore.ts';

const $axios = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://95.111.250.65:8001',
});

const fetchToken = async (): Promise<{ success: boolean }> => {
  const response = await fetch('/token');
  return await response.json() as { success: boolean };
};

$axios.interceptors.request.use(
  (config) => {
    if (config.loading) config.loading.value = true;

    const { get: getToken } = useCookies();
    if (getToken('token')) {
      config.headers.Authorization = `Bearer ${getToken('token')}`;
    }
    return config;
  },
);

$axios.interceptors.response.use(
  (response) => {
    if (response.data.error && typeof response.data.error === 'string') {
      const $toast = useToastStore();
      $toast.error(response.data.error);
    }

    if (response.config.loading) response.config.loading.value = false;

    return response;
  },

  async (error: AxiosError) => {
    if (error.status === 401) {
      const result = await fetchToken();
      if (result.success && error.config) return $axios.request(error.config);
    }

    if (error) {
      const message = error.response?.data && typeof error.response.data === 'string' ? error.response.data : error.message;
      const $toast = useToastStore();
      $toast.error(message);
    }

    if (error?.response?.config.loading) error.response.config.loading.value = false;

    return { error };
  },
);

export default $axios;
