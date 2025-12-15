<template>
  <div class="telegram-required">
    <div class="telegram-required__content">
      <div class="telegram-required__icon">
        🤖
      </div>
      
      <h1 class="telegram-required__title">
        Midas AI Accountant
      </h1>
      
      <p class="telegram-required__message">
        Для доступа пройдите авторизацию через Telegram бота
      </p>
      
      <a 
        :href="`https://t.me/${botUsername}`" 
        target="_blank"
        class="telegram-required__button"
      >
        <span class="telegram-required__button-icon">📱</span>
        Открыть бота {{ botUsername }}
      </a>
      
      <div class="telegram-required__hint">
        После авторизации в боте откройте веб-приложение
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// You can customize this based on your actual bot username
const botUsername = import.meta.env.VITE_BOT_USERNAME || 'MidasBot';
</script>

<style scoped lang="scss">
.telegram-required {
  position: fixed;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  font-family: var(--font-family);
  
  &__content {
    max-width: 400px;
    padding: 3rem 2rem;
    text-align: center;
    background: rgba(255, 255, 255, 0.95);
    border-radius: 24px;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
    animation: fadeIn 0.5s ease-out;
  }
  
  &__icon {
    font-size: 4rem;
    margin-bottom: 1.5rem;
    animation: bounce 2s infinite;
  }
  
  &__title {
    font-size: 1.75rem;
    font-weight: 700;
    color: #2d3748;
    margin-bottom: 1rem;
  }
  
  &__message {
    font-size: 1.125rem;
    color: #4a5568;
    margin-bottom: 2rem;
    line-height: 1.6;
  }
  
   &__button {
    display: inline-flex;
    align-items: center;
    gap: 0.75rem;
    padding: 1rem 2rem;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    text-decoration: none;
    border-radius: 12px;
    font-weight: 600;
    font-size: 1rem;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    
    &:hover {
      transform: translateY(-2px);
      box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    &:active {
      transform: translateY(0);
    }
    
    &-icon {
      font-size: 1.25rem;
    }
  }
  
  &__hint {
    margin-top: 1.5rem;
    font-size: 0.875rem;
    color: #718096;
    font-style: italic;
  }
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes bounce {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
}
</style>
