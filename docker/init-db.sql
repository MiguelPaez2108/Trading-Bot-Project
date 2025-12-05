-- ============================================================================
-- TimescaleDB Initialization Script
-- ============================================================================
-- This script runs automatically when the database is first created

-- Enable TimescaleDB extension
CREATE EXTENSION IF NOT EXISTS timescaledb;

-- Create application user with limited permissions (if not exists)
DO
$$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'trading_app') THEN
        CREATE ROLE trading_app WITH LOGIN PASSWORD 'app_password_change_me';
    END IF;
END
$$;

-- Create read-only user for backups and analytics
DO
$$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'trading_readonly') THEN
        CREATE ROLE trading_readonly WITH LOGIN PASSWORD 'readonly_password_change_me';
    END IF;
END
$$;

-- Grant necessary permissions
GRANT CONNECT ON DATABASE trading_db TO trading_app;
GRANT CONNECT ON DATABASE trading_db TO trading_readonly;

-- Create schemas
CREATE SCHEMA IF NOT EXISTS market_data;
CREATE SCHEMA IF NOT EXISTS trading;
CREATE SCHEMA IF NOT EXISTS analytics;

-- Grant schema permissions
GRANT USAGE ON SCHEMA market_data TO trading_app, trading_readonly;
GRANT USAGE ON SCHEMA trading TO trading_app, trading_readonly;
GRANT USAGE ON SCHEMA analytics TO trading_app, trading_readonly;

GRANT CREATE ON SCHEMA market_data TO trading_app;
GRANT CREATE ON SCHEMA trading TO trading_app;
GRANT CREATE ON SCHEMA analytics TO trading_app;

-- ============================================================================
-- Market Data Tables
-- ============================================================================

-- Candles table (OHLCV data)
CREATE TABLE IF NOT EXISTS market_data.candles (
    time TIMESTAMPTZ NOT NULL,
    symbol VARCHAR(20) NOT NULL,
    exchange VARCHAR(20) NOT NULL,
    timeframe VARCHAR(10) NOT NULL,
    open NUMERIC(20, 8) NOT NULL,
    high NUMERIC(20, 8) NOT NULL,
    low NUMERIC(20, 8) NOT NULL,
    close NUMERIC(20, 8) NOT NULL,
    volume NUMERIC(20, 8) NOT NULL,
    quote_volume NUMERIC(20, 8),
    trades_count INTEGER,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Convert to hypertable (time-series optimized)
SELECT create_hypertable(
    'market_data.candles',
    'time',
    if_not_exists => TRUE,
    chunk_time_interval => INTERVAL '1 day'
);

-- Create indexes for efficient queries
CREATE INDEX IF NOT EXISTS idx_candles_symbol_time 
    ON market_data.candles (symbol, time DESC);
CREATE INDEX IF NOT EXISTS idx_candles_symbol_exchange_timeframe 
    ON market_data.candles (symbol, exchange, timeframe, time DESC);

-- Add compression policy (compress data older than 7 days)
SELECT add_compression_policy(
    'market_data.candles',
    INTERVAL '7 days',
    if_not_exists => TRUE
);

-- Add retention policy (keep data for 2 years)
SELECT add_retention_policy(
    'market_data.candles',
    INTERVAL '2 years',
    if_not_exists => TRUE
);

-- Trades table (tick data)
CREATE TABLE IF NOT EXISTS market_data.trades (
    time TIMESTAMPTZ NOT NULL,
    symbol VARCHAR(20) NOT NULL,
    exchange VARCHAR(20) NOT NULL,
    trade_id VARCHAR(50),
    price NUMERIC(20, 8) NOT NULL,
    quantity NUMERIC(20, 8) NOT NULL,
    side VARCHAR(10),
    is_buyer_maker BOOLEAN,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

SELECT create_hypertable(
    'market_data.trades',
    'time',
    if_not_exists => TRUE,
    chunk_time_interval => INTERVAL '1 day'
);

CREATE INDEX IF NOT EXISTS idx_trades_symbol_time 
    ON market_data.trades (symbol, time DESC);

-- ============================================================================
-- Trading Tables
-- ============================================================================

-- Orders table
CREATE TABLE IF NOT EXISTS trading.orders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    symbol VARCHAR(20) NOT NULL,
    exchange VARCHAR(20) NOT NULL,
    side VARCHAR(10) NOT NULL,
    type VARCHAR(20) NOT NULL,
    status VARCHAR(20) NOT NULL,
    quantity NUMERIC(20, 8) NOT NULL,
    price NUMERIC(20, 8),
    stop_price NUMERIC(20, 8),
    filled_quantity NUMERIC(20, 8) DEFAULT 0,
    average_fill_price NUMERIC(20, 8),
    commission NUMERIC(20, 8) DEFAULT 0,
    commission_asset VARCHAR(10),
    exchange_order_id VARCHAR(100),
    client_order_id VARCHAR(100),
    strategy_id VARCHAR(50),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    filled_at TIMESTAMPTZ,
    CONSTRAINT chk_filled_quantity CHECK (filled_quantity <= quantity)
);

CREATE INDEX IF NOT EXISTS idx_orders_symbol_created 
    ON trading.orders (symbol, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_orders_status_exchange 
    ON trading.orders (status, exchange);
CREATE INDEX IF NOT EXISTS idx_orders_strategy 
    ON trading.orders (strategy_id, created_at DESC);

-- Positions table
CREATE TABLE IF NOT EXISTS trading.positions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    symbol VARCHAR(20) NOT NULL,
    exchange VARCHAR(20) NOT NULL,
    side VARCHAR(10) NOT NULL,
    entry_price NUMERIC(20, 8) NOT NULL,
    quantity NUMERIC(20, 8) NOT NULL,
    current_price NUMERIC(20, 8),
    realized_pnl NUMERIC(20, 8) DEFAULT 0,
    unrealized_pnl NUMERIC(20, 8) DEFAULT 0,
    total_fees NUMERIC(20, 8) DEFAULT 0,
    strategy_id VARCHAR(50),
    opened_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    closed_at TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS idx_positions_symbol_exchange 
    ON trading.positions (symbol, exchange, closed_at);
CREATE INDEX IF NOT EXISTS idx_positions_strategy 
    ON trading.positions (strategy_id);

-- Balances table
CREATE TABLE IF NOT EXISTS trading.balances (
    exchange VARCHAR(20) NOT NULL,
    currency VARCHAR(10) NOT NULL,
    free NUMERIC(20, 8) NOT NULL DEFAULT 0,
    locked NUMERIC(20, 8) NOT NULL DEFAULT 0,
    total NUMERIC(20, 8) NOT NULL DEFAULT 0,
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    PRIMARY KEY (exchange, currency)
);

-- ============================================================================
-- Analytics Tables
-- ============================================================================

-- Strategy performance metrics
CREATE TABLE IF NOT EXISTS analytics.strategy_metrics (
    time TIMESTAMPTZ NOT NULL,
    strategy_id VARCHAR(50) NOT NULL,
    total_trades INTEGER DEFAULT 0,
    winning_trades INTEGER DEFAULT 0,
    losing_trades INTEGER DEFAULT 0,
    total_pnl NUMERIC(20, 8) DEFAULT 0,
    win_rate NUMERIC(5, 2),
    sharpe_ratio NUMERIC(10, 4),
    max_drawdown NUMERIC(10, 4),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

SELECT create_hypertable(
    'analytics.strategy_metrics',
    'time',
    if_not_exists => TRUE,
    chunk_time_interval => INTERVAL '1 day'
);

-- ============================================================================
-- Grant table permissions
-- ============================================================================

-- Grant full access to trading_app
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA market_data TO trading_app;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA trading TO trading_app;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA analytics TO trading_app;

-- Grant read-only access to trading_readonly
GRANT SELECT ON ALL TABLES IN SCHEMA market_data TO trading_readonly;
GRANT SELECT ON ALL TABLES IN SCHEMA trading TO trading_readonly;
GRANT SELECT ON ALL TABLES IN SCHEMA analytics TO trading_readonly;

-- Grant sequence permissions
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA market_data TO trading_app;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA trading TO trading_app;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA analytics TO trading_app;

-- ============================================================================
-- Continuous Aggregates (for performance)
-- ============================================================================

-- Hourly candles aggregated from minute candles
CREATE MATERIALIZED VIEW IF NOT EXISTS market_data.candles_1h
WITH (timescaledb.continuous) AS
SELECT
    time_bucket('1 hour', time) AS time,
    symbol,
    exchange,
    '1h' as timeframe,
    FIRST(open, time) as open,
    MAX(high) as high,
    MIN(low) as low,
    LAST(close, time) as close,
    SUM(volume) as volume
FROM market_data.candles
WHERE timeframe = '1m'
GROUP BY time_bucket('1 hour', time), symbol, exchange
WITH NO DATA;

-- Add refresh policy
SELECT add_continuous_aggregate_policy(
    'market_data.candles_1h',
    start_offset => INTERVAL '3 hours',
    end_offset => INTERVAL '1 hour',
    schedule_interval => INTERVAL '1 hour',
    if_not_exists => TRUE
);

-- ============================================================================
-- Utility Functions
-- ============================================================================

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Add triggers for updated_at
CREATE TRIGGER update_orders_updated_at BEFORE UPDATE ON trading.orders
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_positions_updated_at BEFORE UPDATE ON trading.positions
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_balances_updated_at BEFORE UPDATE ON trading.balances
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ============================================================================
-- Initialization Complete
-- ============================================================================

-- Log initialization
DO $$
BEGIN
    RAISE NOTICE 'TimescaleDB initialization completed successfully';
    RAISE NOTICE 'Created schemas: market_data, trading, analytics';
    RAISE NOTICE 'Created hypertables: candles, trades, strategy_metrics';
    RAISE NOTICE 'Configured compression and retention policies';
END $$;
