"""
Sample data generator for demo user.
Creates realistic transaction data for the last 3 months.
"""
import random
from datetime import datetime,  timedelta
from decimal import Decimal
from uuid import UUID

# Category mapping (slug -> name, typical amounts in UZS)
EXPENSE_CATEGORIES = {
    "food": ("Питание", 50000, 200000, [
        "Супермаркет", "Кафе", "Ресторан", "Бургер", "Пицца", 
        "Доставка еды", "Кофе", "Продукты Atto", "Макдональдс"
    ]),
    "transport": ("Транспорт", 10000, 50000, [
        "Такси", "Яндекс.Такси", "Метро", "Автобус", "Парковка", "Бензин"
    ]),
    "entertainment": ("Развлечения", 30000, 150000, [
        "Кино", "Боулинг", "Караоке", "Концерт", "Игры", "Подписка Netflix"
    ]),
    "shopping": ("Покупки", 100000, 500000, [
        "Одежда", "Обувь", "Электроника", "Маркетплейс", "Техника"
    ]),
    "services": ("Услуги", 50000, 120000, [
        "Барбер", "Парикмахерская", "Салон красоты", "Мастер"
    ]),
    "health": ("Здоровье", 30000, 100000, [
        "Аптека", "Врач", "Стоматолог", "Анализы", "Лекарства"
    ]),
    "bills": ("Счета", 50000, 150000, [
        "Интернет", "Мобильная связь", "Коммунальные услуги", "Электричество"
    ]),
    "other": ("Прочее", 20000, 80000, [
        "Разное", "Прочее", "Другое"
    ]),
}

INCOME_CATEGORIES = {
    "salary": ("Зарплата", 3000000, 5000000, ["Зарплата", "Аванс"]),
    "freelance": ("Подработка", 500000, 2000000, ["Фриланс", "Подработка"]),
}


def generate_sample_data_sql(username: str = "demo", email: str = "demo@example.com", password_hash: str = "$2b$12$demo_hash") -> str:
    """
    Generate SQL INSERT statements for sample data.
    
    Args:
        username: Sample user username
        email: Sample user email
        password_hash: Pre-hashed password (use get_password_hash("demo123"))
    
    Returns:
        SQL string with INSERT statements
    """
    
    sql_lines = [
        "-- ============================================================================",
        "-- SAMPLE DATA FOR DEMO USER",
        "-- ============================================================================",
        "",
        "-- Create demo user",
        "DO $$",
        "DECLARE",
        "    demo_user_id UUID := uuid_generate_v4();",
        "    cat_food UUID;",
        "    cat_transport UUID;",
        "    cat_entertainment UUID;",
        "    cat_shopping UUID;",
        "    cat_services UUID;",
        "    cat_health UUID;",
        "    cat_bills UUID;",
        "    cat_other UUID;",
        "    cat_salary UUID;",
        "    cat_freelance UUID;",
        "BEGIN",
        "",
        f"    -- Insert demo user",
        f"    INSERT INTO users (id, username, email, hashed_password, default_currency)",
        f"    VALUES (demo_user_id, '{username}', '{email}', '{password_hash}', 'uzs')",
        f"    ON CONFLICT (username) DO NOTHING;",
        "",
        "    -- Get category IDs",
        "    SELECT id INTO cat_food FROM categories WHERE slug = 'food' AND is_default = TRUE LIMIT 1;",
        "    SELECT id INTO cat_transport FROM categories WHERE slug = 'transport' AND is_default = TRUE LIMIT 1;",
        "    SELECT id INTO cat_entertainment FROM categories WHERE slug = 'entertainment' AND is_default = TRUE LIMIT 1;",
        "    SELECT id INTO cat_shopping FROM categories WHERE slug = 'shopping' AND is_default = TRUE LIMIT 1;",
        "    SELECT id INTO cat_services FROM categories WHERE slug = 'services' AND is_default = TRUE LIMIT 1;",
        "    SELECT id INTO cat_health FROM categories WHERE slug = 'health' AND is_default = TRUE LIMIT 1;",
        "    SELECT id INTO cat_bills FROM categories WHERE slug = 'bills' AND is_default = TRUE LIMIT 1;",
        "    SELECT id INTO cat_other FROM categories WHERE slug = 'other' AND is_default = TRUE LIMIT 1;",
        "    SELECT id INTO cat_salary FROM categories WHERE slug = 'salary' AND is_default = TRUE LIMIT 1;",
        "    SELECT id INTO cat_freelance FROM categories WHERE slug = 'freelance' AND is_default = TRUE LIMIT 1;",
        "",
        "    -- Insert transactions for last 3 months",
    ]
    
    # Generate transactions for last 3 months
    end_date = datetime.now()
    start_date = end_date - timedelta(days=90)
    
    current_date = start_date
    
    while current_date <= end_date:
        day_of_month = current_date.day
        day_of_week = current_date.weekday()
        
        # Salary on 1st and 15th
        if day_of_month in [1, 15]:
            amount = random.randint(3000000, 5000000)
            description = "Зарплата" if day_of_month == 1 else "Аванс"
            sql_lines.append(
                f"    INSERT INTO transactions (user_id, category_id, type, amount, currency, description, transaction_date) "
                f"VALUES (demo_user_id, cat_salary, 'income', {amount}, 'uzs', '{description}', '{current_date.strftime('%Y-%m-%d %H:%M:%S')}');"
            )
        
        # Expenses (more on weekends)
        num_transactions = random.randint(3, 5) if day_of_week >= 5 else random.randint(1, 3)
        
        for _ in range(num_transactions):
            # Random category
            category_slug = random.choice(list(EXPENSE_CATEGORIES.keys()))
            cat_name, min_amt, max_amt, descriptions = EXPENSE_CATEGORIES[category_slug]
            
            amount = random.randint(min_amt, max_amt)
            description = random.choice(descriptions)
            
            # Random time during the day
            random_hour = random.randint(8, 22)
            random_minute = random.randint(0, 59)
            tx_time = current_date.replace(hour=random_hour, minute=random_minute)
            
            cat_var = f"cat_{category_slug}"
            
            sql_lines.append(
                f"    INSERT INTO transactions (user_id, category_id, type, amount, currency, description, transaction_date) "
                f"VALUES (demo_user_id, {cat_var}, 'expense', {amount}, 'uzs', '{description}', '{tx_time.strftime('%Y-%m-%d %H:%M:%S')}');"
            )
        
        current_date += timedelta(days=1)
    
    sql_lines.extend([
        "",
        "    RAISE NOTICE 'Sample data created for user: %', demo_user_id;",
        "END $$;",
        "",
        "-- ============================================================================",
        "-- END SAMPLE DATA",
        "-- ============================================================================",
    ])
    
    return "\n".join(sql_lines)


if __name__ == "__main__":
    # Generate and print SQL
    # Note: In production, use proper password hashing
    from passlib.context import CryptContext
    
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    password_hash = pwd_context.hash("demo123")
    
    sql = generate_sample_data_sql(
        username="demo",
        email="demo@example.com",
        password_hash=password_hash
    )
    
    # Write to file
    with open("sample_data.sql", "w", encoding="utf-8") as f:
        f.write(sql)
    
    print("✅ Sample data SQL generated: sample_data.sql")
    print("📊 Run with: psql -U postgres -d accountant_db -f sample_data.sql")
