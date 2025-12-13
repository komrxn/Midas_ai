-- AI Accountant Database Schema
-- PostgreSQL 14+
-- Production-ready schema for multi-user expense tracking

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================================================
-- USERS TABLE
-- ============================================================================
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    default_currency VARCHAR(3) DEFAULT 'uzs' NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT NOW() NOT NULL
);

CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_email ON users(email);

-- ============================================================================
-- CATEGORIES TABLE
-- ============================================================================
CREATE TABLE IF NOT EXISTS categories (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    slug VARCHAR(100) NOT NULL,
    type VARCHAR(20) NOT NULL CHECK (type IN ('expense', 'income', 'debt')),
    icon VARCHAR(50),
    color VARCHAR(20),
    is_default BOOLEAN DEFAULT FALSE NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL
);

CREATE INDEX idx_categories_user_id ON categories(user_id);
CREATE INDEX idx_categories_slug ON categories(slug);
CREATE INDEX idx_categories_type ON categories(type);

-- ============================================================================
-- TRANSACTIONS TABLE
-- ============================================================================
CREATE TABLE IF NOT EXISTS transactions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    category_id UUID REFERENCES categories(id) ON DELETE SET NULL,
    type VARCHAR(20) NOT NULL CHECK (type IN ('income', 'expense')),
    amount NUMERIC(18, 2) NOT NULL CHECK (amount > 0),
    currency VARCHAR(3) DEFAULT 'uzs' NOT NULL,
    description VARCHAR(500),
    ai_parsed_data JSONB,
    ai_confidence NUMERIC(3, 2),
    transaction_date TIMESTAMPTZ DEFAULT NOW() NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT NOW() NOT NULL
);

CREATE INDEX idx_transactions_user_id ON transactions(user_id);
CREATE INDEX idx_transactions_category_id ON transactions(category_id);
CREATE INDEX idx_transactions_type ON transactions(type);
CREATE INDEX idx_transactions_date ON transactions(transaction_date);
CREATE INDEX idx_transactions_user_date ON transactions(user_id, transaction_date DESC);
CREATE INDEX idx_transactions_user_type_date ON transactions(user_id, type, transaction_date DESC);

-- ============================================================================
-- DEBTS TABLE
-- ============================================================================
CREATE TABLE IF NOT EXISTS debts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    type VARCHAR(20) NOT NULL CHECK (type IN ('i_owe', 'owe_me')),
    person_name VARCHAR(200) NOT NULL,
    amount NUMERIC(18, 2) NOT NULL CHECK (amount > 0),
    currency VARCHAR(3) DEFAULT 'uzs' NOT NULL,
    description VARCHAR(500),
    status VARCHAR(20) DEFAULT 'open' NOT NULL CHECK (status IN ('open', 'overdue', 'settled')),
    due_date DATE,
    settled_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT NOW() NOT NULL
);

CREATE INDEX idx_debts_user_id ON debts(user_id);
CREATE INDEX idx_debts_status ON debts(status);
CREATE INDEX idx_debts_type ON debts(type);

-- ============================================================================
-- LIMITS TABLE  
-- ============================================================================
CREATE TABLE IF NOT EXISTS limits (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    category_id UUID NOT NULL REFERENCES categories(id) ON DELETE CASCADE,
    amount NUMERIC(18, 2) NOT NULL CHECK (amount > 0),
    period_start DATE NOT NULL,
    period_end DATE NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT NOW() NOT NULL,
    UNIQUE(user_id, category_id, period_start)
);

CREATE INDEX idx_limits_user_id ON limits(user_id);
CREATE INDEX idx_limits_period ON limits(user_id, period_start, period_end);
CREATE INDEX idx_limits_category ON limits(category_id);

-- ============================================================================
-- TRIGGERS FOR UPDATED_AT
-- ============================================================================
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_transactions_updated_at BEFORE UPDATE ON transactions
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_categories_updated_at BEFORE UPDATE ON categories
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_debts_updated_at BEFORE UPDATE ON debts
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_limits_updated_at BEFORE UPDATE ON limits
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ============================================================================
-- DEFAULT CATEGORIES (System-wide)
-- ============================================================================
INSERT INTO categories (id, user_id, name, slug, type, icon, color, is_default) VALUES
-- Expense categories
(uuid_generate_v4(), NULL, 'Питание', 'food', 'expense', '🍔', '#E74C3C', TRUE),
(uuid_generate_v4(), NULL, 'Транспорт', 'transport', 'expense', '🚕', '#3498DB', TRUE),
(uuid_generate_v4(), NULL, 'Развлечения', 'entertainment', 'expense', '🎮', '#9B59B6', TRUE),
(uuid_generate_v4(), NULL, 'Покупки', 'shopping', 'expense', '🛍️', '#2ECC71', TRUE),
(uuid_generate_v4(), NULL, 'Услуги', 'services', 'expense', '💇', '#1ABC9C', TRUE),
(uuid_generate_v4(), NULL, 'Здоровье', 'health', 'expense', '💊', '#E91E63', TRUE),
(uuid_generate_v4(), NULL, 'Образование', 'education', 'expense', '📚', '#FF9800', TRUE),
(uuid_generate_v4(), NULL, 'Жильё', 'housing', 'expense', '🏠', '#795548', TRUE),
(uuid_generate_v4(), NULL, 'Счета', 'bills', 'expense', '💳', '#607D8B', TRUE),
(uuid_generate_v4(), NULL, 'Прочее', 'other', 'expense', '📦', '#95A5A6', TRUE),

-- Income categories
(uuid_generate_v4(), NULL, 'Зарплата', 'salary', 'income', '💰', '#27AE60', TRUE),
(uuid_generate_v4(), NULL, 'Подработка', 'freelance', 'income', '💼', '#16A085', TRUE),
(uuid_generate_v4(), NULL, 'Возврат', 'refund', 'income', '↩️', '#2ECC71', TRUE),
(uuid_generate_v4(), NULL, 'Прочее', 'other_income', 'income', '💵', '#27AE60', TRUE)
ON CONFLICT DO NOTHING;
