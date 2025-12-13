from decimal import Decimal
from typing import Optional
from pydantic import BaseModel


class BalanceResponse(BaseModel):
    """Overall balance response."""
    balance: Decimal
    total_income: Decimal
    total_expense: Decimal
    currency: str = "uzs"
    period_label: str


class CategoryBreakdownItem(BaseModel):
    """Single category in breakdown."""
    category_id: Optional[str]
    category_name: str
    category_slug: str
    amount: Decimal
    percentage: float
    transaction_count: int
    color: Optional[str] = None


class CategoryBreakdownResponse(BaseModel):
    """Category breakdown for pie chart."""
    categories: list[CategoryBreakdownItem]
    total: Decimal
    currency: str = "uzs"


class TimeSeriesDataPoint(BaseModel):
    """Single point in time series."""
    date: str  # YYYY-MM-DD or YYYY-MM or YYYY
    income: Decimal
    expense: Decimal
    balance: Decimal


class TimeSeriesResponse(BaseModel):
    """Time series data for charts."""
    data: list[TimeSeriesDataPoint]
    granularity: str  # day, week, month, year
    currency: str = "uzs"


class TrendMetric(BaseModel):
    """Trend metrics with percentage change."""
    current_value: Decimal
    previous_value: Decimal
    change_percentage: float
    is_up: bool


class AnalyticsSummaryResponse(BaseModel):
    """Combined analytics summary."""
    balance: BalanceResponse
    category_breakdown: CategoryBreakdownResponse
    trends: Optional[TimeSeriesResponse] = None
    income_trend: Optional[TrendMetric] = None
    expense_trend: Optional[TrendMetric] = None
