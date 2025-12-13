"""
Test transaction endpoints.
"""
import pytest
from httpx import AsyncClient
from decimal import Decimal


@pytest.mark.asyncio
async def test_create_transaction(client: AsyncClient, auth_headers: dict, default_categories):
    """Test creating a transaction."""
    food_category = next(cat for cat in default_categories if cat.slug == "food")
    
    response = await client.post(
        "/transactions",
        headers=auth_headers,
        json={
            "type": "expense",
            "amount": "50000",
            "currency": "uzs",
            "description": "Lunch at restaurant",
            "category_id": str(food_category.id)
        }
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["type"] == "expense"
    assert Decimal(data["amount"]) == Decimal("50000")
    assert data["description"] == "Lunch at restaurant"


@pytest.mark.asyncio
async def test_list_transactions(client: AsyncClient, auth_headers: dict, default_categories):
    """Test listing transactions."""
    food_category = next(cat for cat in default_categories if cat.slug == "food")
    
    # Create some transactions
    for i in range(3):
        await client.post(
            "/transactions",
            headers=auth_headers,
            json={
                "type": "expense",
                "amount": str(10000 * (i + 1)),
                "currency": "uzs",
                "description": f"Transaction {i}",
                "category_id": str(food_category.id)
            }
        )
    
    # List all
    response = await client.get("/transactions", headers=auth_headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 3
    assert len(data["items"]) == 3


@pytest.mark.asyncio
async def test_filter_transactions_by_type(client: AsyncClient, auth_headers: dict, default_categories):
    """Test filtering transactions by type."""
    food_cat = next(cat for cat in default_categories if cat.slug == "food")
    salary_cat = next(cat for cat in default_categories if cat.slug == "salary")
    
    # Create expenses
    await client.post(
        "/transactions",
        headers=auth_headers,
        json={"type": "expense", "amount": "50000", "currency": "uzs", "category_id": str(food_cat.id)}
    )
    
    # Create income
    await client.post(
        "/transactions",
        headers=auth_headers,
        json={"type": "income", "amount": "500000", "currency": "uzs", "category_id": str(salary_cat.id)}
    )
    
    # Filter by expense
    response = await client.get("/transactions?type=expense", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["total"] == 1
    
    # Filter by income
    response = await client.get("/transactions?type=income", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["total"] == 1


@pytest.mark.asyncio
async def test_get_transaction_by_id(client: AsyncClient, auth_headers: dict, default_categories):
    """Test getting specific transaction."""
    food_category = next(cat for cat in default_categories if cat.slug == "food")
    
    # Create transaction
    create_response = await client.post(
        "/transactions",
        headers=auth_headers,
        json={"type": "expense", "amount": "75000", "currency": "uzs", "category_id": str(food_category.id)}
    )
    
    tx_id = create_response.json()["id"]
    
    # Get by ID
    response = await client.get(f"/transactions/{tx_id}", headers=auth_headers)
    
    assert response.status_code == 200
    assert response.json()["id"] == tx_id


@pytest.mark.asyncio
async def test_update_transaction(client: AsyncClient, auth_headers: dict, default_categories):
    """Test updating a transaction."""
    food_category = next(cat for cat in default_categories if cat.slug == "food")
    
    # Create
    create_response = await client.post(
        "/transactions",
        headers=auth_headers,
        json={"type": "expense", "amount": "100000", "currency": "uzs", "category_id": str(food_category.id)}
    )
    
    tx_id = create_response.json()["id"]
    
    # Update
    response = await client.patch(
        f"/transactions/{tx_id}",
        headers=auth_headers,
        json={"amount": "150000", "description": "Updated description"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert Decimal(data["amount"]) == Decimal("150000")
    assert data["description"] == "Updated description"


@pytest.mark.asyncio
async def test_delete_transaction(client: AsyncClient, auth_headers: dict, default_categories):
    """Test deleting a transaction."""
    food_category = next(cat for cat in default_categories if cat.slug == "food")
    
    # Create
    create_response = await client.post(
        "/transactions",
        headers=auth_headers,
        json={"type": "expense", "amount": "50000", "currency": "uzs", "category_id": str(food_category.id)}
    )
    
    tx_id = create_response.json()["id"]
    
    # Delete
    response = await client.delete(f"/transactions/{tx_id}", headers=auth_headers)
    assert response.status_code == 204
    
    # Verify deleted
    get_response = await client.get(f"/transactions/{tx_id}", headers=auth_headers)
    assert get_response.status_code == 404
