"""Analytics router for dashboard data."""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, case, extract
from datetime import datetime, timedelta

from ..database import get_db
from ..models.user import User
from .auth import get_current_admin

router = APIRouter()


@router.get("/stats")
async def get_dashboard_stats(
    db: AsyncSession = Depends(get_db),
    admin = Depends(get_current_admin)
):
    """Get overview stats for dashboard cards."""
    # Total users
    total_users = await db.execute(select(func.count(User.id)))
    total_users = total_users.scalar_one()
    
    # Active subscriptions (not free)
    active_subs = await db.execute(
        select(func.count(User.id)).where(User.subscription_type != "free")
    )
    active_subs = active_subs.scalar_one()
    
    # Subscription breakdown
    subs_breakdown = await db.execute(
        select(
            User.subscription_type,
            func.count(User.id)
        ).group_by(User.subscription_type)
    )
    breakdown = {row[0]: row[1] for row in subs_breakdown.fetchall()}
    
    # New users this month
    month_start = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    new_this_month = await db.execute(
        select(func.count(User.id)).where(User.created_at >= month_start)
    )
    new_this_month = new_this_month.scalar_one()
    
    return {
        "total_users": total_users,
        "active_subscriptions": active_subs,
        "new_users_this_month": new_this_month,
        "subscription_breakdown": breakdown
    }


@router.get("/user-growth")
async def get_user_growth(
    days: int = 30,
    db: AsyncSession = Depends(get_db),
    admin = Depends(get_current_admin)
):
    """Get user registration data for growth chart."""
    start_date = datetime.now() - timedelta(days=days)
    
    # Group by date
    result = await db.execute(
        select(
            func.date(User.created_at).label("date"),
            func.count(User.id).label("count")
        )
        .where(User.created_at >= start_date)
        .group_by(func.date(User.created_at))
        .order_by(func.date(User.created_at))
    )
    
    data = result.fetchall()
    
    # Build cumulative data
    dates = []
    counts = []
    cumulative = 0
    
    # Get total before start_date
    pre_count = await db.execute(
        select(func.count(User.id)).where(User.created_at < start_date)
    )
    cumulative = pre_count.scalar_one() or 0
    
    for row in data:
        dates.append(row.date.strftime("%Y-%m-%d"))
        cumulative += row.count
        counts.append(cumulative)
    
    return {
        "labels": dates,
        "data": counts,
        "daily_new": [row.count for row in data]
    }


@router.get("/subscription-growth")
async def get_subscription_growth(
    days: int = 30,
    db: AsyncSession = Depends(get_db),
    admin = Depends(get_current_admin)
):
    """Get subscription tier data over time."""
    # For this, we'll show current breakdown per date by checking subscription_ends_at
    # Simpler approach: show current subscription distribution
    
    result = await db.execute(
        select(
            User.subscription_type,
            func.count(User.id)
        ).group_by(User.subscription_type)
    )
    
    breakdown = {row[0]: row[1] for row in result.fetchall()}
    
    return {
        "plus": breakdown.get("plus", 0),
        "pro": breakdown.get("pro", 0), 
        "premium": breakdown.get("premium", 0),
        "trial": breakdown.get("trial", 0),
        "free": breakdown.get("free", 0)
    }


@router.get("/bot-usage")
async def get_bot_usage(
    days: int = 30,
    db: AsyncSession = Depends(get_db),
    admin = Depends(get_current_admin)
):
    """Get bot usage statistics."""
    # Since we track voice_usage_count and photo_usage_count on users,
    # we'll aggregate those
    
    result = await db.execute(
        select(
            func.sum(User.voice_usage_count).label("total_voice"),
            func.sum(User.photo_usage_count).label("total_photo"),
            func.sum(User.text_usage_count).label("total_text"),
            func.sum(User.voice_usage_daily).label("voice_today"),
            func.sum(User.image_usage_daily).label("images_today"),
            func.sum(User.text_usage_daily).label("text_today")
        )
    )
    
    row = result.fetchone()
    
    # Active users (used bot in last 7 days based on updated_at)
    week_ago = datetime.now() - timedelta(days=7)
    active_result = await db.execute(
        select(func.count(User.id)).where(User.updated_at >= week_ago)
    )
    active_users = active_result.scalar_one()
    
    return {
        "total_voice_requests": row.total_voice or 0,
        "total_photo_requests": row.total_photo or 0,
        "total_text_requests": row.total_text or 0,
        "voice_today": row.voice_today or 0,
        "images_today": row.images_today or 0,
        "text_today": row.text_today or 0,
        "active_users_7d": active_users
    }
