"""Seed default categories for the application."""
import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from api.database import async_session_maker
from api.models.category import Category
from sqlalchemy import select


DEFAULT_CATEGORIES = [
    # Расходы
    {"name": "Еда", "slug": "food", "type": "expense", "icon": "🍔", "color": "#FF6B6B"},
    {"name": "Транспорт", "slug": "transport", "type": "expense", "icon": "🚗", "color": "#4ECDC4"},
    {"name": "Жильё", "slug": "housing", "type": "expense", "icon": "🏠", "color": "#95E1D3"},
    {"name": "Развлечения", "slug": "entertainment", "type": "expense", "icon": "🎮", "color": "#F38181"},
    {"name": "Здоровье", "slug": "health", "type": "expense", "icon": "💊", "color": "#AA96DA"},
    {"name": "Образование", "slug": "education", "type": "expense", "icon": "📚", "color": "#FCBAD3"},
    {"name": "Одежда", "slug": "clothing", "type": "expense", "icon": "👔", "color": "#A8D8EA"},
    {"name": "Связь", "slug": "communication", "type": "expense", "icon": "📱", "color": "#FFD93D"},
    {"name": "Подарки", "slug": "gifts", "type": "expense", "icon": "🎁", "color": "#6BCB77"},
    {"name": "Спорт", "slug": "sports", "type": "expense", "icon": "⚽", "color": "#4D96FF"},
    {"name": "Красота", "slug": "beauty", "type": "expense", "icon": "💄", "color": "#FDA7DF"},
    {"name": "Путешествия", "slug": "travel", "type": "expense", "icon": "✈️", "color": "#F6A5C0"},
    {"name": "Кафе/Рестораны", "slug": "cafes", "type": "expense", "icon": "☕", "color": "#F3D250"},
    {"name": "Продукты", "slug": "groceries", "type": "expense", "icon": "🛒", "color": "#90CCF4"},
    {"name": "Такси", "slug": "taxi", "type": "expense", "icon": "🚕", "color": "#F78888"},
    {"name": "Коммуналка", "slug": "utilities", "type": "expense", "icon": "💡", "color": "#5EAAA8"},
    {"name": "Другое", "slug": "other_expense", "type": "expense", "icon": "💰", "color": "#B8B5FF"},
    
    # Доходы
    {"name": "Зарплата", "slug": "salary", "type": "income", "icon": "💵", "color": "#26de81"},
    {"name": "Фриланс", "slug": "freelance", "type": "income", "icon": "💻", "color": "#45aaf2"},
    {"name": "Инвестиции", "slug": "investments", "type": "income", "icon": "📈", "color": "#a55eea"},
    {"name": "Подарок", "slug": "gift_income", "type": "income", "icon": "🎁", "color": "#fd79a8"},
    {"name": "Другое", "slug": "other_income", "type": "income", "icon": "💸", "color": "#00b894"},
    
    # Долги
    {"name": "Заняли", "slug": "borrowed", "type": "debt_out", "icon": "💸", "color": "#ee5a6f"},
    {"name": "Дали взаймы", "slug": "lent", "type": "debt_in", "icon": "🤝", "color": "#20bf6b"},
    {"name": "Вернули мне", "slug": "returned_to_me", "type": "income", "icon": "💰", "color": "#4b7bec"},
    {"name": "Я вернул", "slug": "i_returned", "type": "expense", "icon": "💵", "color": "#fa8231"},
]


async def seed_categories():
    """Seed default categories into database."""
    async with async_session_maker() as session:
        # Check if categories already exist
        result = await session.execute(select(Category))
        existing = result.scalars().all()
        
        if len(existing) > 5:
            print(f"⚠️ Categories already exist ({len(existing)} found). Skipping seed.")
            return
        
        print(f"📦 Seeding {len(DEFAULT_CATEGORIES)} default categories...")
        
        for cat_data in DEFAULT_CATEGORIES:
            # Check if category with this slug exists
            result = await session.execute(
                select(Category).where(Category.slug == cat_data["slug"])
            )
            existing_cat = result.scalar_one_or_none()
            
            if not existing_cat:
                category = Category(**cat_data)
                session.add(category)
                print(f"  ✅ Added: {cat_data['name']} ({cat_data['type']})")
        
        await session.commit()
        print("✅ Categories seeded successfully!")


if __name__ == "__main__":
    asyncio.run(seed_categories())
