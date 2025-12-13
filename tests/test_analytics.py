"""
Test analytics endpoints.
"""
import pytest
from httpx import AsyncClient
from decimal import Decimal


@pytest.mark.asyncio
async def test_get_balance(client: AsyncClient, auth_headers: dict, default_categories):
    """Test balance calculation."""
    food_cat = next(cat for cat in default_categories if cat.slug == "food")
    salary_cat = next(cat for cat in default_categories if cat.slug == "salary")
    
    # Create transactions
    await client.post(
        "/transactions",
        headers=auth_headers,
        json={"type": "income", "amount": "1000000", "currency": "uzs", "category_id": str(salary_cat.id)}
    )
    
    await client.post(
        "/transactions",
        headers=auth_headers,
        json={"type": "expense", "amount": "300000", "currency": "uzs", "category_id": str(food_cat.id)}
    )
    
    # Get balance
    response = await client.get("/analytics/balance?period=all", headers=auth_headers)
    
    assert response.status_code == 200
    data = response.json()
    assert Decimal(data["total_income"]) == Decimal("1000000")
    assert Decimal(data["total_expense"]) == Decimal("300000")
    assert Decimal(data["balance"]) == Decimal("700000")


@pytest.mark.asyncio
async def test_category_breakdown(client: AsyncClient, auth_headers: dict, default_categories):
    """Test category breakdown for pie chart."""
    food_cat = next(cat for cat in default_categories if cat.slug == "food")
    transport_cat = next(cat for cat in default_categories if cat.slug == "transport")
    
    # Create expenses
    await client.post(
        "/transactions",
        headers=auth_headers,
        json={"type": "expense", "amount": "100000", "currency": "uzs", "category_id": str(food_cat.id)}
    )
    
    await client.post(
        "/transactions",
        headers=auth_headers,
        json={"type": "expense", "amount": "50000", "currency": "uzs", "category_id": str(transport_cat.id)}
    )
    
    # Get breakdown
    response = await client.get("/analytics/categories?period=all&type=expense", headers=auth_headers)
    
    assert response.status_code == 200
    data = response.json()
    assert Decimal(data["total"]) == Decimal("150000")
    assert len(data["categories"]) == 2
    
    # Check percentages
    food_item = next(cat for cat in data["categories"] if cat["category_slug"] == "food")
    assert food_item["percentage"] == pytest.approx(66.7, rel=0.1)


@pytest.mark.asyncio
async def test_trends(client: AsyncClient, auth_headers: dict, default_categories):
    """Test time-series trends."""
    food_cat = next(cat for cat in default_categories if cat.slug == "food")
    
    # Create transaction
    await client.post(
        "/transactions",
        headers=auth_headers,
        json={"type": "expense", "amount": "100000", "currency": "uzs", "category_id": str(food_cat.id)}
    )
    
    # Get trends
    response = await client.get("/analytics/trends?period=month&granularity=day", headers=auth_headers)
    
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert data["granularity"] == "day"
    assert len(data["data"]) > 0


@pytest.mark.asyncio
async def test_analytics_summary(client: AsyncClient, auth_headers: dict, default_categories):
    """Test analytics summary endpoint."""
    food_cat = next(cat for cat in default_categories if cat.slug == "food")
    salary_cat = next(cat for cat in default_categories if cat.slug == "salary")
    
    # Create transactions
    await client.post(
        "/transactions",
        headers=auth_headers,
        json={"type": "income", "amount": "500000", "currency": "uzs", "category_id": str(salary_cat.id)}
    )
    
    await client.post(
        "/transactions",
        headers=auth_headers,
        json={"type": "expense", "amount": "100000", "currency": "uzs", "category_id": str(food_cat.id)}
    )
    
    # Get summary
    response = await client.get("/analytics/summary", headers=auth_headers)
    
    assert response.status_code == 200
    data = response.json()
    assert "balance" in data
    assert "category_breakdown" in data
    assert "trends" in data
