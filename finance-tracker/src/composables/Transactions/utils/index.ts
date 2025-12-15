import type { Transaction, TransactionGroup } from '../types';
import { formatDate, formatDateToAPI } from '@/utils';
import { MONTHS_FULL, DAYS_SHORT } from '@/composables/Categories/data';
import { i18n } from '@/plugins/i18n';

/**
 * Группирует транзакции по дням
 */
export const groupTransactionsByDay = (transactions: Transaction[]): TransactionGroup[] => {
    const t = i18n.global.t;
    const groupsMap = new Map<string, Transaction[]>();

    transactions.forEach(transaction => {
        const date = new Date(transaction.transaction_date);
        // Используем локальное форматирование даты для избежания проблем с часовыми поясами
        const dateKey = formatDateToAPI(date);

        if (!groupsMap.has(dateKey)) {
            groupsMap.set(dateKey, []);
        }
        groupsMap.get(dateKey)!.push(transaction);
    });

    const groups: TransactionGroup[] = Array.from(groupsMap.entries()).map(([date, transactions]) => {
        const transactionDate = new Date(date);
        const today = new Date();
        const yesterday = new Date(today);
        yesterday.setDate(yesterday.getDate() - 1);

        let dateLabel = '';
        if (transactionDate.toDateString() === today.toDateString()) {
            dateLabel = t('common.today');
        } else if (transactionDate.toDateString() === yesterday.toDateString()) {
            dateLabel = t('common.yesterday');
        } else {
            const dayOfWeek = transactionDate.getDay();
            const dayIndex = dayOfWeek === 0 ? 6 : dayOfWeek - 1;
            const dayName = DAYS_SHORT[dayIndex];
            const day = transactionDate.getDate();
            const month = MONTHS_FULL[transactionDate.getMonth()];
            dateLabel = `${dayName}, ${day} ${month}`;
        }

        // Сортируем транзакции внутри группы по времени (новые сверху)
        const sortedTransactions = transactions.sort((a, b) => {
            return new Date(b.transaction_date).getTime() - new Date(a.transaction_date).getTime();
        });

        const totalIncome = sortedTransactions
            .filter(t => t.type === 'income')
            .reduce((sum, t) => sum + parseFloat(t.amount), 0);

        const totalExpense = sortedTransactions
            .filter(t => t.type === 'expense')
            .reduce((sum, t) => sum + parseFloat(t.amount), 0);

        return {
            date: date, // Используем date из деструктуризации [date, transactions]
            dateLabel,
            transactions: sortedTransactions,
            totalIncome,
            totalExpense,
        };
    });

    // Сортируем группы по дате (новые сверху)
    return groups.sort((a, b) => {
        return new Date(b.date).getTime() - new Date(a.date).getTime();
    });
};

/**
 * Форматирует время из ISO строки в формат HH:MM
 */
export const formatTime = (dateString: string): string => {
    const date = new Date(dateString);
    return date.toLocaleTimeString('ru-RU', {
        hour: '2-digit',
        minute: '2-digit',
    });
};
