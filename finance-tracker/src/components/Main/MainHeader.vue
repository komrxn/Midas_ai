<template>
    <div class="main-header">
        <div class="main-header__content">
            <div class="main-header__content-avatar">
                {{ firstLetter }}
            </div>
            <div class="main-header__content-info">
                <h1>
                    {{ t('main.greeting', { username: userData?.name || t('main.user') }) }}
                </h1>
                <p>{{ t('main.smartTracker') }}</p>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue';
import { storeToRefs } from 'pinia';
import { useI18n } from 'vue-i18n';
import { useUserStore } from '@/store/userStore';

const { t } = useI18n();

const userStore = useUserStore();
const { user: userData } = storeToRefs(userStore);
const { loadUser } = userStore;

const firstLetter = computed(() => {
    if (userData.value?.name) {
        return userData.value.name.charAt(0).toUpperCase();
    }
    return '?';
});

onMounted(async () => {
    try {
        await loadUser();
    } catch (error) {
        console.error('Failed to load user data:', error);
    }
});

</script>

<style scoped lang="scss">
.main-header {
    display: flex;
    align-items: center;
    justify-content: space-between;

    &__content {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 1rem;

    }

    &__content-avatar {
        width: 4rem;
        height: 4rem;
        border-radius: 50%;
        background: var(--primary-500);
        color: var(--white);
        display: flex;
        align-items: center;
        justify-content: center;
        font: var(--font-18-b);
        font-weight: 600;
    }

    &__content-info {
        display: flex;
        flex-direction: column;
        gap: 0.4rem;

        h1 {
            font: var(--font-18-b);
        }

        p {
            font: var(--font-14-r);
        }
    }

}
</style>