export const layoutMiddleware = async (route: any) => {
  try {
    const layout = route.meta.layout;
    const layoutComponent = await import(`../layouts/${layout}.vue`);
    route.meta.layoutComponent = layoutComponent.default;
  }
  catch (error) {
    if (error) {
      const layout = 'Default';
      const layoutComponent = await import(`../layouts/${layout}.vue`);
      route.meta.layoutComponent = layoutComponent.default;
    }
  }
};
