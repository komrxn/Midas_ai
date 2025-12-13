# AI Accountant API - Test Guide

## 🧪 Running Tests

### Quick Start

```bash
# Install test dependencies
pip install -r requirements.txt

# Create test database
createdb accountant_test_db

# Run all tests
python scripts/run_tests.py

# Or directly with pytest
pytest tests/ -v
```

### Test Options

```bash
# Skip AI tests (no OpenAI API calls)
python scripts/run_tests.py --skip-ai

# Verbose output
python scripts/run_tests.py --verbose

# Run specific test file
pytest tests/test_auth.py -v

# Run specific test
pytest tests/test_auth.py::test_register_user -v

# Run only AI tests
pytest tests/ -m ai -v
```

## 📊 Test Coverage

### Test Files

| File | Tests | Coverage |
|------|-------|----------|
| `test_auth.py` | 6 | Authentication endpoints |
| `test_transactions.py` | 7 | Transaction CRUD operations |
| `test_categories.py` | 8 | Category management |
| `test_analytics.py` | 4 | Analytics & reports |
| `test_ai.py` | 4 | AI parsing (requires OpenAI key) |

**Total: 29 tests** covering all major API functionality

### What's Tested

✅ **Authentication**
- User registration
- Login with JWT tokens
- Protected endpoint access
- Invalid credentials handling

✅ **Transactions**
- Create, read, update, delete
- Filtering by type, category, date
- Pagination
- Validation

✅ **Categories**
- List default categories
- Create custom categories
- Update/delete custom categories
- Protection of default categories
- Prevent deletion if used

✅ **Analytics**
- Balance calculation
- Category breakdown (pie chart data)
- Time-series trends
- Combined dashboard summary

✅ **AI Parsing**
- Text transaction parsing
- Auto-categorization
- Category suggestions
- Confidence scoring

## 🔧 Test Database

Tests use a separate database: `accountant_test_db`

**Setup:**
```bash
# Create test database
createdb accountant_test_db

# Tables are auto-created/dropped for each test
# No manual schema setup needed!
```

**Isolation:**
- Each test gets a fresh database
- Tests don't interfere with each other
- Real database (`accountant_db`) is never touched

## 📝 Writing New Tests

### Example Test

```python
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_my_endpoint(client: AsyncClient, auth_headers: dict):
    """Test description."""
    response = await client.get("/my-endpoint", headers=auth_headers)
    
    assert response.status_code == 200
    assert response.json()["key"] == "value"
```

### Available Fixtures

- `client` - Async HTTP client
- `auth_headers` - Authenticated request headers
- `db_session` - Database session
- `test_user` - Pre-created test user
- `default_categories` - Default categories

## 🚨 Important Notes

### AI Tests

AI tests make **real OpenAI API calls** and may:
- Cost money (minimal, ~$0.01 per test run)
- Be flaky if OpenAI is down
- Require `OPENAI_API_KEY` in environment

**Skip AI tests** if you don't have an API key:
```bash
pytest tests/ -m "not ai"
```

### Test Database Cleanup

Test database is automatically cleaned before each test. No manual cleanup needed.

### CI/CD Integration

For automated testing:
```yaml
# Example GitHub Actions
- name: Run tests
  env:
    DATABASE_URL: postgresql://postgres:postgres@localhost/accountant_test_db
  run: |
    createdb accountant_test_db
    pytest tests/ -m "not ai" -v
```

## 📈 Coverage Report

Generate HTML coverage report:
```bash
pytest tests/ --cov=api --cov-report=html
open htmlcov/index.html
```

## 🐛 Debugging Failed Tests

```bash
# Run with full traceback
pytest tests/ -v --tb=long

# Stop on first failure
pytest tests/ -x

# Run last failed tests
pytest tests/ --lf

# Drop into debugger on failure
pytest tests/ --pdb
```

## ✅ Expected Output

```
tests/test_auth.py::test_register_user PASSED                   [ 16%]
tests/test_auth.py::test_login PASSED                           [ 33%]
tests/test_transactions.py::test_create_transaction PASSED      [ 50%]
...

===================== 29 passed in 5.43s =========================
```

All tests should pass with a fresh database!
