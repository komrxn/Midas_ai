// import type { RouteLocationNormalized } from 'vue-router';
// import type { RouteNames } from '@/router/types';
// import { RouterEnum } from '@/router/types';
// import { usePageTransitionStore } from '@/store/pageTransitionStore.ts';

// export const pageTransitionMiddleware = (to: RouteLocationNormalized, from: RouteLocationNormalized) => {
//   const pageTransition = usePageTransitionStore();
//   pageTransition.isBack = (!RouterEnum[to.name as RouteNames] || !RouterEnum[from.name as RouteNames]) ? false : RouterEnum[to.name as RouteNames] < RouterEnum[from.name as RouteNames];
// };
