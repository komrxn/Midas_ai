"""
Test AI parsing endpoints.
Note: These tests will make real OpenAI API calls if OPENAI_API_KEY is set.
To skip: pytest -m "not ai"
"""
import pytest
from httpx import AsyncClient
import os


@pytest.mark.ai
@pytest.mark.skipif(not os.getenv("OPENAI_API_KEY"), reason="No OpenAI API key")
@pytest.mark.asyncio
async def test_parse_text_transaction(client: AsyncClient, auth_headers: dict, default_categories):
    """Test parsing transaction from text."""
    response = await client.post(
        "/ai/parse-transaction",
        headers=auth_headers,
        data={"text": "купил бургер за 112000 сум"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["type"] in ["income", "expense"]
    assert float(data["amount"]) > 0
    assert data["currency"] in ["uzs", "usd", "eur", "rub"]
    assert 0 <= data["confidence"] <= 1


@pytest.mark.ai
@pytest.mark.skipif(not os.getenv("OPENAI_API_KEY"), reason="No OpenAI API key")
@pytest.mark.asyncio
async def test_parse_text_with_auto_create(client: AsyncClient, auth_headers: dict, default_categories):
    """Test parsing and auto-creating transaction."""
    response = await client.post(
        "/ai/parse-transaction",
        headers=auth_headers,
        data={
            "text": "зарплата 5000000 сум",
            "auto_create": "true"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    
    # If confidence is high, should auto-create
    if data["confidence"] >= 0.7:
        assert data["auto_created"] == True


@pytest.mark.ai
@pytest.mark.skipif(not os.getenv("OPENAI_API_KEY"), reason="No OpenAI API key")
@pytest.mark.asyncio
async def test_suggest_category(client: AsyncClient, auth_headers: dict, default_categories):
    """Test category suggestion."""
    response = await client.post(
        "/ai/suggest-category",
        headers=auth_headers,
        json={
            "description": "купил продукты в магазине",
            "transaction_type": "expense"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "suggestions" in data
    if data["best_match"]:
        assert 0 <= data["best_match"]["confidence"] <= 1


@pytest.mark.asyncio
async def test_parse_transaction_without_input(client: AsyncClient, auth_headers: dict):
    """Test parsing without providing text/voice/image."""
    response = await client.post(
        "/ai/parse-transaction",
        headers=auth_headers,
        data={}
    )
    
    assert response.status_code == 400
