/**
 * Форматирование чисел и дат
 */

import type { Period } from '@/composables/Analytics/useAnalytics';
import { DAYS_SHORT, MONTHS_SHORT } from '@/composables/Categories/data';

/**
 * Форматирует сумму в строку с разделителями тысяч
 * @param amount - сумма (число или строка)
 * @returns Отформатированная строка
 */
export const formatAmount = (amount: number | string | null | undefined): string => {
    if (amount === null || amount === undefined) {
        return '0';
    }

    const numAmount = typeof amount === 'string' ? parseFloat(amount || '0') : amount;

    if (isNaN(numAmount)) {
        return '0';
    }

    return numAmount.toLocaleString('ru-RU');
};

/**
 * Форматирует сумму с сокращениями (k, M)
 * @param amount - сумма
 * @returns Отформатированная строка с сокращениями
 */
export const formatAmountShort = (amount: number | undefined | null): string => {
    if (amount === undefined || amount === null || isNaN(amount)) {
        return '0';
    }

    if (amount >= 1000000) {
        return `${(amount / 1000000).toFixed(1).replace(/\.0$/, '')}M`;
    }

    if (amount >= 1000) {
        return `${(amount / 1000).toFixed(0)}k`;
    }

    return amount.toLocaleString('ru-RU');
};

/**
 * Форматирует сумму со знаком (+ или -)
 * @param amount - сумма
 * @returns Отформатированная строка со знаком
 */
export const formatAmountWithSign = (amount: number): string => {
    const absAmount = Math.abs(amount);
    const sign = amount < 0 ? '-' : '';

    if (absAmount >= 1000000) {
        const millions = absAmount / 1000000;
        const rounded = millions.toFixed(1);
        return `${sign}${rounded.replace(/\.0$/, '')}M`;
    }

    return `${sign}${absAmount.toLocaleString('ru-RU')}`;
};

/**
 * Форматирует дату в формат ДД.ММ.ГГГГ
 * @param dateString - строка с датой (ISO формат или другой)
 * @returns Отформатированная дата
 */
export const formatDate = (dateString: string | null | undefined): string => {
    if (!dateString) {
        return '';
    }

    const date = new Date(dateString);

    if (isNaN(date.getTime())) {
        return '';
    }

    return date.toLocaleDateString('ru-RU', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric'
    });
};

/**
 * Форматирует дату и время
 * @param dateString - строка с датой
 * @returns Отформатированная дата и время
 */
export const formatDateTime = (dateString: string | null | undefined): string => {
    if (!dateString) {
        return '';
    }

    const date = new Date(dateString);

    if (isNaN(date.getTime())) {
        return '';
    }

    return date.toLocaleString('ru-RU', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
};

/**
 * Форматирует дату в формат YYYY-MM-DD (без времени)
 * Используется для API запросов, чтобы избежать проблем с часовыми поясами
 * @param date - объект Date или строка с датой
 * @returns Строка в формате YYYY-MM-DD
 */
export const formatDateToAPI = (date: Date | string): string => {
    const dateObj = typeof date === 'string' ? new Date(date) : date;

    if (isNaN(dateObj.getTime())) {
        throw new Error('Invalid date');
    }

    const year = dateObj.getFullYear();
    const month = String(dateObj.getMonth() + 1).padStart(2, '0');
    const day = String(dateObj.getDate()).padStart(2, '0');

    return `${year}-${month}-${day}`;
};

/**
 * Получает дату начала дня в формате YYYY-MM-DD
 * @param date - объект Date (по умолчанию сегодня)
 * @returns Строка в формате YYYY-MM-DD
 */
export const getStartOfDayString = (date: Date = new Date()): string => {
    return formatDateToAPI(date);
};

/**
 * Получает дату конца дня в формате YYYY-MM-DD
 * @param date - объект Date (по умолчанию сегодня)
 * @returns Строка в формате YYYY-MM-DD
 */
export const getEndOfDayString = (date: Date = new Date()): string => {
    return formatDateToAPI(date);
};

/**
 * Преобразует дату в формат datetime для API (YYYY-MM-DDTHH:mm:ss)
 * @param dateString - строка с датой в формате YYYY-MM-DD
 * @param isEndOfDay - если true, устанавливает время 23:59:59, иначе 00:00:00
 * @returns Строка в формате YYYY-MM-DDTHH:mm:ss
 */
export const formatDateToAPIDatetime = (dateString: string, isEndOfDay = false): string => {
    if (!dateString) {
        return '';
    }

    // Если дата уже содержит время, возвращаем как есть
    if (dateString.includes('T')) {
        return dateString;
    }

    // Добавляем время в зависимости от isEndOfDay
    const time = isEndOfDay ? '23:59:59' : '00:00:00';
    return `${dateString}T${time}`;
};

/**
 * Форматирует дату для меток графиков в зависимости от периода
 * @param dateStr - строка с датой в формате "2024-12-14"
 * @param period - период (day, week, month, year)
 * @returns Отформатированная метка для графика
 */
export const formatDateLabel = (dateStr: string, period: Period): string => {
    const date = new Date(dateStr);

    if (isNaN(date.getTime())) {
        return dateStr;
    }

    if (period === 'week') {
        // getDay() возвращает 0 для воскресенья, но нам нужен понедельник как первый день
        const dayIndex = date.getDay() === 0 ? 6 : date.getDay() - 1;
        return DAYS_SHORT[dayIndex];
    }

    if (period === 'year') {
        return MONTHS_SHORT[date.getMonth()];
    }

    if (period === 'month') {
        return date.getDate().toString();
    }

    if (period === 'day') {
        return `${date.getHours()}:00`;
    }

    return dateStr;
};
