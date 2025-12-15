<template>
    <div class="main-quick-input">
        <div class="main-quick-input__card">
            <h5 class="main-quick-input__title">{{ t('main.quickInput') }}</h5>
            <div class="main-quick-input__buttons">
                <Button :icon="microphoneIcon" severity="primary" text fluid :label="t('main.voiceInput')"
                    class="main-quick-input__button" @click="handleVoiceInput" />
                <Button :icon="cameraIcon" severity="primary" text fluid :label="t('main.photoInput')"
                    class="main-quick-input__button" @click="handlePhotoInput" />
            </div>
            <InputText v-model="quickInputText" :placeholder="t('main.writeExpenses')" class="main-quick-input__field"
                @keyup.enter="handleTextInput" fluid />
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useI18n } from 'vue-i18n';
import { Button, InputText } from 'primevue';
import { microphone, camera } from '@/assets/icons';

const { t } = useI18n();

const quickInputText = ref('');
const microphoneIcon = microphone;
const cameraIcon = camera;

const handleVoiceInput = () => {
    // TODO: Реализовать голосовой ввод
    console.log('Голосовой ввод');
};

const handlePhotoInput = () => {
    // TODO: Реализовать фото ввод
    console.log('Фото ввод');
};

const handleTextInput = () => {
    if (quickInputText.value.trim()) {
        // TODO: Обработать текстовый ввод
        console.log('Текстовый ввод:', quickInputText.value);
        quickInputText.value = '';
    }
};
</script>

<style scoped lang="scss">
.main-quick-input {
    padding: 2rem 0 0 0;

    &__card {
        padding: 2rem 1.6rem;
        border-radius: 1.6rem;
        background: var(--gold-card-bg);
        border: 1px solid var(--gold-border);
        box-shadow: var(--gold-shadow);
        position: relative;
        overflow: hidden;
        transition: all 0.3s ease;

        &::before {
            content: '';
            position: absolute;
            top: 0;
            right: 0;
            width: 60%;
            height: 100%;
            background: var(--gold-card-radial);
            pointer-events: none;
        }

        &:hover {
            border-color: var(--gold-border-hover);
            box-shadow: var(--gold-shadow-hover);
            transform: translateY(-2px);
        }

        @include media-max($mobile) {
            padding: 1.6rem 1.2rem;
        }
    }

    &__title {
        color: var(--text-color-secondary);
        font: var(--font-14-r);
        margin-bottom: 1.2rem;
        position: relative;
        z-index: 1;
    }

    &__buttons {
        display: flex;
        align-items: center;
        gap: 1rem;
        position: relative;
        z-index: 1;
        margin: 0 0 1.2rem 0;

        @include media-max($mobile) {
            gap: 0.8rem;
        }
    }

    &__button {
        --p-button-padding-y: 1rem;
        font: var(--font-14-b);

        @include media-max($small) {
            font: var(--font-12-b) !important;
        }
    }

    &__field {
        flex: 1;
        min-width: 0;
        padding: 1.2rem 1.6rem;
        border-color: var(--gold-border);
        font: var(--font-14-r);
        border-radius: 0.8rem;
        transition: all 0.3s ease;
    }
}
</style>
