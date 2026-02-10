import { useUserStore } from '@/store/userStore';

export const subscriptionMiddleware = async () => {
    const userStore = useUserStore();

    try {
        // Всегда принудительно загружаем данные пользователя при каждом переходе
        // чтобы обновить статус подписки
        await userStore.loadUser(true);
    } catch (error) {
        console.error('Failed to load user in subscription middleware:', error);
        // Не блокируем переход, просто логируем ошибку
    }

    return true;
};

