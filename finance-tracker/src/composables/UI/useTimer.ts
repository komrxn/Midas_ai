import { useLocalStorage } from '@vueuse/core';
import { computed, onBeforeMount, onBeforeUnmount, ref } from 'vue';

export const useTimer = () => {
  let intervalId: NodeJS.Timeout;

  const timerEndTimeStamp = useLocalStorage<number>('timer', 0);
  const currentTimeStamp = ref<number>(Date.now());

  const isTimerActive = computed<boolean>(() => {
    return !!timerEndTimeStamp.value && timerEndTimeStamp.value > currentTimeStamp.value;
  });

  const time = computed<string>(() => {
    if (!isTimerActive.value) return '00:00';
    const delta = (timerEndTimeStamp.value - currentTimeStamp.value) / 1000;
    const minutes = Math.floor(delta / 60);
    const seconds = Math.floor(delta % 60);
    return `${minutes < 10 ? 0 : ''}${minutes}:${seconds < 10 ? 0 : ''}${seconds}`;
  });

  const resetInterval = () => {
    timerEndTimeStamp.value = 0;
    if (intervalId) clearInterval(intervalId);
  };

  const startInterval = () => {
    if (!isTimerActive.value) return;
    intervalId = setInterval(() => {
      currentTimeStamp.value = Date.now();
      if (!isTimerActive.value) resetInterval();
    }, 1000);
  };

  onBeforeUnmount(() => {
    if (intervalId) clearInterval(intervalId);
  });

  onBeforeMount(() => {
    startInterval();
  });

  const start = (minutes: number) => {
    currentTimeStamp.value = Date.now();
    timerEndTimeStamp.value = Date.now() + minutes * 60 * 1000;
    startInterval();
  };

  return { start, time, isTimerActive };
};
