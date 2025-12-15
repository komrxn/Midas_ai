export type RouteNames = 'main' | 'status' | 'limits';

export const RouterEnum: Record<RouteNames, number> = {
  main: 1,
  limits: 2,
  status: 10000,
};
