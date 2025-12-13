"""
Test category endpoints.
"""
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_list_categories(client: AsyncClient, auth_headers: dict, default_categories):
    """Test listing categories."""
    response = await client.get("/categories", headers=auth_headers)
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 3  # At least our 3 default categories


@pytest.mark.asyncio
async def test_filter_categories_by_type(client: AsyncClient, auth_headers: dict, default_categories):
    """Test filtering categories by type."""
    # Get expense categories
    response = await client.get("/categories?type=expense", headers=auth_headers)
    
    assert response.status_code == 200
    data = response.json()
    assert all(cat["type"] == "expense" for cat in data)


@pytest.mark.asyncio
async def test_create_custom_category(client: AsyncClient, auth_headers: dict):
    """Test creating a custom category."""
    response = await client.post(
        "/categories",
        headers=auth_headers,
        json={
            "name": "Подписки",
            "slug": "subscriptions",
            "type": "expense",
            "icon": "📱",
            "color": "#FF5722"
        }
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Подписки"
    assert data["slug"] == "subscriptions"
    assert data["is_default"] == False


@pytest.mark.asyncio
async def test_create_duplicate_category_slug(client: AsyncClient, auth_headers: dict, default_categories):
    """Test creating category with duplicate slug."""
    response = await client.post(
        "/categories",
        headers=auth_headers,
        json={
            "name": "Another Food",
            "slug": "food",  # Already exists
            "type": "expense"
        }
    )
    
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_update_custom_category(client: AsyncClient, auth_headers: dict):
    """Test updating a custom category."""
    # Create custom category
    create_response = await client.post(
        "/categories",
        headers=auth_headers,
        json={"name": "Test", "slug": "test_cat", "type": "expense"}
    )
    
    cat_id = create_response.json()["id"]
    
    # Update
    response = await client.patch(
        f"/categories/{cat_id}",
        headers=auth_headers,
        json={"name": "Updated Test", "icon": "🎯"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Test"
    assert data["icon"] == "🎯"


@pytest.mark.asyncio
async def test_cannot_update_default_category(client: AsyncClient, auth_headers: dict, default_categories):
    """Test that default categories cannot be updated."""
    food_cat = next(cat for cat in default_categories if cat.slug == "food")
    
    response = await client.patch(
        f"/categories/{food_cat.id}",
        headers=auth_headers,
        json={"name": "Modified Food"}
    )
    
    assert response.status_code == 404  # Can't find/modify default category


@pytest.mark.asyncio
async def test_delete_custom_category(client: AsyncClient, auth_headers: dict):
    """Test deleting a custom category."""
    # Create custom category
    create_response = await client.post(
        "/categories",
        headers=auth_headers,
        json={"name": "Temporary", "slug": "temp", "type": "expense"}
    )
    
    cat_id = create_response.json()["id"]
    
    # Delete
    response = await client.delete(f"/categories/{cat_id}", headers=auth_headers)
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_cannot_delete_category_with_transactions(client: AsyncClient, auth_headers: dict, default_categories):
    """Test that categories with transactions cannot be deleted."""
    # Create custom category
    create_response = await client.post(
        "/categories",
        headers=auth_headers,
        json={"name": "WithTx", "slug": "withtx", "type": "expense"}
    )
    
    cat_id = create_response.json()["id"]
    
    # Create transaction with this category
    await client.post(
        "/transactions",
        headers=auth_headers,
        json={"type": "expense", "amount": "1000", "currency": "uzs", "category_id": cat_id}
    )
    
    # Try to delete
    response = await client.delete(f"/categories/{cat_id}", headers=auth_headers)
    assert response.status_code == 400
