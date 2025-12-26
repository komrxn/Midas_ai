# Baraka Ai API Documentation for Frontend Developers

**Version:** 2.0.0  
**Base URL:** `http://localhost:8000` (development) | `https://your-domain.com` (production)  
**Documentation:** http://localhost:8000/docs (Swagger UI)

---

## Table of Contents

1. [Authentication](#authentication)
2. [Transactions](#transactions)
3. [Categories](#categories)
4. [Analytics](#analytics)
5. [Debts](#debts)
6. [Limits](#limits)
7. [AI Parsing](#ai-parsing)
8. [Error Handling](#error-handling)
9. [Data Models](#data-models)

---

## Authentication

### Register User
**POST** `/auth/register`

```typescript
// Request
{
  "username": "string",
  "email": "user@example.com",
  "password": "string"
}

// Response (201)
{
  "id": "uuid",
  "username": "string",
  "email": "user@example.com",
  "default_currency": "uzs",
  "created_at": "2025-12-13T10:00:00Z"
}
```

### Login
**POST** `/auth/login`

```typescript
// Request
{
  "username": "string",
  "password": "string"
}

// Response (200)
{
  "access_token": "eyJhbGc...",
  "token_type": "bearer"
}
```

### Get Current User
**GET** `/auth/me`

**Headers:** `Authorization: Bearer <token>`

```typescript
// Response (200)
{
  "id": "uuid",
  "username": "string",
  "email": "user@example.com",
  "default_currency": "uzs",
  "created_at": "2025-12-13T10:00:00Z"
}
```

---

## Transactions

### Create Transaction
**POST** `/transactions`

**Headers:** `Authorization: Bearer <token>`

```typescript
// Request
{
  "type": "expense" | "income",
  "amount": 1500.50,
  "category_id": "uuid",
  "description": "Coffee with friends",
  "transaction_date": "2025-12-13T10:00:00Z" // optional, defaults to now
}

// Response (201)
{
  "id": "uuid",
  "user_id": "uuid",
  "category_id": "uuid",
  "type": "expense",
  "amount": "1500.50",
  "currency": "uzs",
  "description": "Coffee with friends",
  "transaction_date": "2025-12-13T10:00:00Z",
  "created_at": "2025-12-13T10:00:00Z",
  "updated_at": "2025-12-13T10:00:00Z"
}
```

### List Transactions
**GET** `/transactions`

**Headers:** `Authorization: Bearer <token>`

**Query Parameters:**
- `type`: `expense` | `income` (optional)
- `category_id`: Filter by category UUID (optional)
- `start_date`: Filter from date (ISO format, optional)
- `end_date`: Filter to date (ISO format, optional)
- `skip`: Pagination offset (default: 0)
- `limit`: Page size (default: 100, max: 100)

```typescript
// Response (200)
[
  {
    "id": "uuid",
    "type": "expense",
    "amount": "1500.50",
    "category_id": "uuid",
    "description": "Coffee",
    "transaction_date": "2025-12-13T10:00:00Z",
    ...
  }
]
```

### Get Transaction
**GET** `/transactions/{transaction_id}`

### Update Transaction
**PUT** `/transactions/{transaction_id}`

### Delete Transaction
**DELETE** `/transactions/{transaction_id}`

**Response:** 204 No Content

---

## Categories

### List Categories
**GET** `/categories`

**Headers:** `Authorization: Bearer <token>`

```typescript
// Response (200)
[
  {
    "id": "uuid",
    "user_id": "uuid" | null, // null for default categories
    "name": "Питание",
    "slug": "food",
    "type": "expense" | "income" | "debt",
    "icon": "🍔",
    "color": "#E74C3C",
    "is_default": true,
    "created_at": "2025-12-13T10:00:00Z"
  }
]
```

### Create Category
**POST** `/categories`

```typescript
// Request
{
  "name": "Кофе",
  "slug": "coffee",
  "type": "expense",
  "icon": "☕",
  "color": "#8B4513"
}
```

### Update Category
**PUT** `/categories/{category_id}`

**Note:** Cannot update default categories

### Delete Category
**DELETE** `/categories/{category_id}`

**Note:** Cannot delete default categories

---

## Analytics

### Get Balance
**GET** `/analytics/balance`

**Headers:** `Authorization: Bearer <token>`

**Query Parameters:**
- `start_date`: From date (ISO format, optional)
- `end_date`: To date (ISO format, optional)

```typescript
// Response (200)
{
  "total_income": "50000.00",
  "total_expense": "35000.00",
  "balance": "15000.00",
  "income_count": 5,
  "expense_count": 42
}
```

### Category Breakdown
**GET** `/analytics/category-breakdown`

**Query Parameters:**
- `type`: `expense` | `income` (default: expense)
- `start_date`: From date (optional)
- `end_date`: To date (optional)

```typescript
// Response (200)
{
  "categories": [
    {
      "category_id": "uuid",
      "category_name": "Питание",
      "total": "12500.00",
      "percentage": 35.7,
      "transaction_count": 15
    }
  ],
  "total": "35000.00"
}
```

### Trends
**GET** `/analytics/trends`

**Query Parameters:**
- `period`: `daily` | `weekly` | `monthly` (default: monthly)
- `start_date`: From date (optional)
- `end_date`: To date (optional)

```typescript
// Response (200)
{
  "trends": [
    {
      "period": "2025-12",
      "income": "50000.00",
      "expense": "35000.00", 
      "balance": "15000.00"
    }
  ]
}
```

### Summary
**GET** `/analytics/summary`

**Headers:** `Authorization: Bearer <token>`

```typescript
// Response (200)
{
  "current_balance": "15000.00",
  "this_month_income": "50000.00",
  "this_month_expense": "35000.00",
  "top_expense_category": {
    "name": "Питание",
    "amount": "12500.00"
  },
  "recent_transactions": [],
  "trends": []
}
```

---

## Debts

### Create Debt
**POST** `/debts`

**Headers:** `Authorization: Bearer <token>`

```typescript
// Request
{
  "type": "i_owe" | "owe_me",
  "person_name": "John Doe",
  "amount": 5000.00,
  "currency": "uzs",
  "description": "Borrowed for rent",
  "due_date": "2025-12-31" // optional
}

// Response (201)
{
  "id": "uuid",
  "user_id": "uuid",
  "type": "i_owe",
  "person_name": "John Doe",
  "amount": "5000.00",
  "currency": "uzs",
  "description": "Borrowed for rent",
  "status": "open", // open | overdue | settled
  "due_date": "2025-12-31",
  "settled_at": null,
  "created_at": "2025-12-13T10:00:00Z",
  "updated_at": "2025-12-13T10:00:00Z"
}
```

### List Debts
**GET** `/debts`

**Headers:** `Authorization: Bearer <token>`

**Query Parameters:**
- `type`: `i_owe` | `owe_me` (optional)
- `status`: `open` | `overdue` | `settled` (optional)

```typescript
// Response (200)
[
  {
    "id": "uuid",
    "type": "i_owe",
    "person_name": "John Doe",
    "amount": "5000.00",
    "status": "open",
    ...
  }
]
```

### Get Debt Balance
**GET** `/debts/balance`

**Headers:** `Authorization: Bearer <token>`

```typescript
// Response (200)
{
  "i_owe_total": "5000.00",
  "owe_me_total": "3000.00",
  "i_owe_count": 2,
  "owe_me_count": 1
}
```

### Get Debt
**GET** `/debts/{debt_id}`

### Update Debt
**PUT** `/debts/{debt_id}`

```typescript
// Request
{
  "person_name": "John Updated",
  "amount": 6000.00,
  "description": "Updated description",
  "status": "open" | "overdue" | "settled",
  "due_date": "2025-12-31",
  "settled_at": "2025-12-13T10:00:00Z" // if settling manually
}
```

### Mark Debt as Paid
**POST** `/debts/{debt_id}/mark-paid`

**Headers:** `Authorization: Bearer <token>`

```typescript
// Response (200)
{
  "id": "uuid",
  "status": "settled",
  "settled_at": "2025-12-13T10:00:00Z",
  ...
}
```

### Delete Debt
**DELETE** `/debts/{debt_id}`

**Response:** 204 No Content

---

## Limits

### Create Limit
**POST** `/limits`

**Headers:** `Authorization: Bearer <token>`

```typescript
// Request
{
  "category_id": "uuid",
  "amount": 50000.00,
  "period_start": "2025-12-01",
  "period_end": "2025-12-31"
}

// Response (201)
{
  "id": "uuid",
  "user_id": "uuid",
  "category_id": "uuid",
  "category_name": "Питание",
  "amount": "50000.00",
  "period_start": "2025-12-01",
  "period_end": "2025-12-31",
  "spent": "12500.00",
  "remaining": "37500.00",
  "percentage": 25.0,
  "is_exceeded": false,
  "created_at": "2025-12-13T10:00:00Z",
  "updated_at": "2025-12-13T10:00:00Z"
}
```

### List Limits
**GET** `/limits`

**Headers:** `Authorization: Bearer <token>`

**Query Parameters:**
- `period_start`: Filter by period start (optional)
- `period_end`: Filter by period end (optional)

```typescript
// Response (200)
[
  {
    "id": "uuid",
    "category_id": "uuid",
    "category_name": "Питание",
    "amount": "50000.00",
    "spent": "12500.00",
    "remaining": "37500.00",
    "percentage": 25.0,
    "is_exceeded": false,
    ...
  }
]
```

### Get Current Month Limits
**GET** `/limits/current`

**Headers:** `Authorization: Bearer <token>`

```typescript
// Response (200)
{
  "total_limits": 3,
  "total_budget": "150000.00",
  "total_spent": "45000.00",
  "exceeded_count": 0,
  "limits": [
    {
      "id": "uuid",
      "category_name": "Питание",
      "amount": "50000.00",
      "spent": "12500.00",
      "percentage": 25.0,
      ...
    }
  ]
}
```

### Get Limit
**GET** `/limits/{limit_id}`

### Update Limit
**PUT** `/limits/{limit_id}`

```typescript
// Request
{
  "amount": 60000.00,
  "period_start": "2025-12-01",
  "period_end": "2025-12-31"
}
```

### Delete Limit
**DELETE** `/limits/{limit_id}`

**Response:** 204 No Content

---

## AI Parsing

### Parse Transaction
**POST** `/ai/parse-transaction`

**Headers:** `Authorization: Bearer <token>`

**Query Parameters:**
- `input_type`: `text` | `voice` | `image` (required)

#### Text Parsing
```typescript
// Request
{
  "text": "Купил кофе за 350 рублей"
}

// Response (200)
{
  "type": "expense",
  "amount": 350.00,
  "description": "Купил кофе",
  "suggested_category": {
    "id": "uuid",
    "name": "Питание"
  },
  "confidence": 0.95
}
```

#### Voice Parsing
```typescript
// Request (multipart/form-data)
{
  "file": <audio file>
}
```

#### Image Parsing
```typescript
// Request (multipart/form-data)
{
  "file": <image file>
}
```

### Suggest Category
**POST** `/ai/suggest-category`

**Headers:** `Authorization: Bearer <token>`

```typescript
// Request
{
  "description": "кофе латте в старбакс"
}

// Response (200)
{
  "category_id": "uuid",
  "category_name": "Питание",
  "confidence": 0.92
}
```

---

## Error Handling

All endpoints return standard HTTP status codes:

### Success Codes
- `200 OK` - Success
- `201 Created` - Resource created
- `204 No Content` - Success with no response body

### Error Codes
- `400 Bad Request` - Invalid request data
- `401 Unauthorized` - Missing or invalid auth token
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Resource not found
- `422 Unprocessable Entity` - Validation error
- `500 Internal Server Error` - Server error

### Error Response Format
```typescript
{
  "detail": "Error message"
}
```

### Validation Error Format
```typescript
{
  "detail": [
    {
      "loc": ["body", "amount"],
      "msg": "ensure this value is greater than 0",
      "type": "value_error"
    }
  ]
}
```

---

## Data Models

### UUID Format
All IDs are UUID v4 strings:
```
"1969091e-e36a-4160-8e61-3f0863427449"
```

### Date Format
All dates use ISO 8601 format:
```
"2025-12-13T10:00:00Z"  // Full datetime
"2025-12-13"            // Date only
```

### Decimal Format
All monetary values are returned as strings to preserve precision:
```json
{
  "amount": "1500.50"
}
```

Convert to number for display:
```typescript
const amount = parseFloat(transaction.amount);
```

### Currency
Default currency: `"uzs"`

---

## Rate Limiting

No rate limiting currently implemented, but recommended client-side throttling:
- Max 100 requests/minute per user
- Batch operations when possible

---

## CORS

Allowed origins (configured in `.env`):
```
CORS_ORIGINS=http://localhost:3000,http://localhost:5173,http://localhost:8080
```

---

## WebSocket Support

Not currently implemented. Consider for future real-time updates.

---

## Best Practices

### Authentication
```typescript
// Store token securely
localStorage.setItem('token', response.access_token);

// Include in all requests
const headers = {
  'Authorization': `Bearer ${localStorage.getItem('token')}`,
  'Content-Type': 'application/json'
};
```

### Pagination
```typescript
// Fetch transactions with pagination
const fetchTransactions = async (page = 0, pageSize = 20) => {
  const response = await fetch(
    `/transactions?skip=${page * pageSize}&limit=${pageSize}`,
    { headers }
  );
  return response.json();
};
```

### Error Handling
```typescript
try {
  const response = await fetch('/transactions', { 
    method: 'POST',
    headers,
    body: JSON.stringify(data)
  });
  
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail);
  }
  
  return await response.json();
} catch (error) {
  console.error('API Error:', error);
  // Show user-friendly error message
}
```

---

## Example: Complete Transaction Flow

```typescript
// 1. Login
const loginResponse = await fetch('http://localhost:8000/auth/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ username: 'user', password: 'pass' })
});
const { access_token } = await loginResponse.json();

// 2. Get categories
const categoriesResponse = await fetch('http://localhost:8000/categories', {
  headers: { 'Authorization': `Bearer ${access_token}` }
});
const categories = await categoriesResponse.json();

// 3. Create transaction
const transactionResponse = await fetch('http://localhost:8000/transactions', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${access_token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    type: 'expense',
    amount: 500,
    category_id: categories[0].id,
    description: 'Coffee'
  })
});
const transaction = await transactionResponse.json();

// 4. Get analytics
const analyticsResponse = await fetch('http://localhost:8000/analytics/summary', {
  headers: { 'Authorization': `Bearer ${access_token}` }
});
const summary = await analyticsResponse.json();
```

---

## Support

- **Swagger UI:** http://localhost:8000/docs
- **OpenAPI JSON:** http://localhost:8000/openapi.json
- **Health Check:** http://localhost:8000/health

---

**Generated:** 2025-12-13  
**API Version:** 2.0.0
