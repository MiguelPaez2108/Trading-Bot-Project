-- Trading System Database Schema
-- TimescaleDB (PostgreSQL extension for time-series data)

-- Enable TimescaleDB extension
CREATE EXTENSION IF NOT EXISTS timescaledb;

-- ============================================================================
-- CANDLES TABLE (Hypertable for OHLCV data)
-- ============================================================================
CREATE TABLE candles (
    time TIMESTAMPTZ NOT NULL,
    symbol TEXT NOT NULL,
    timeframe TEXT NOT NULL,
    open DECIMAL(20, 8) NOT NULL,
    high DECIMAL(20, 8) NOT NULL,
    low DECIMAL(20, 8) NOT NULL,
    close DECIMAL(20, 8) NOT NULL,
    volume DECIMAL(20, 8) NOT NULL,
    quote_volume DECIMAL(20, 8),
    trades_count INTEGER,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Convert to hypertable (partitioned by time)
SELECT create_hypertable('candles', 'time', if_not_exists => TRUE);

-- Create indexes for fast queries
CREATE INDEX idx_candles_symbol_time ON candles (symbol, time DESC);
CREATE INDEX idx_candles_timeframe ON candles (timeframe, time DESC);

-- Create continuous aggregates for higher timeframes
CREATE MATERIALIZED VIEW candles_15m
WITH (timescaledb.continuous) AS
SELECT
    time_bucket('15 minutes', time) AS time,
    symbol,
    '15m' as timeframe,
    FIRST(open, time) as open,
    MAX(high) as high,
    MIN(low) as low,
    LAST(close, time) as close,
    SUM(volume) as volume,
    SUM(quote_volume) as quote_volume,
    SUM(trades_count) as trades_count
FROM candles
WHERE timeframe = '1m'
GROUP BY time_bucket('15 minutes', time), symbol;

CREATE MATERIALIZED VIEW candles_1h
WITH (timescaledb.continuous) AS
SELECT
    time_bucket('1 hour', time) AS time,
    symbol,
    '1h' as timeframe,
    FIRST(open, time) as open,
    MAX(high) as high,
    MIN(low) as low,
    LAST(close, time) as close,
    SUM(volume) as volume,
    SUM(quote_volume) as quote_volume,
    SUM(trades_count) as trades_count
FROM candles
WHERE timeframe = '1m'
GROUP BY time_bucket('1 hour', time), symbol;

CREATE MATERIALIZED VIEW candles_4h
WITH (timescaledb.continuous) AS
SELECT
    time_bucket('4 hours', time) AS time,
    symbol,
    '4h' as timeframe,
    FIRST(open, time) as open,
    MAX(high) as high,
    MIN(low) as low,
    LAST(close, time) as close,
    SUM(volume) as volume,
    SUM(quote_volume) as quote_volume,
    SUM(trades_count) as trades_count
FROM candles
WHERE timeframe = '1m'
GROUP BY time_bucket('4 hours', time), symbol;

CREATE MATERIALIZED VIEW candles_1d
WITH (timescaledb.continuous) AS
SELECT
    time_bucket('1 day', time) AS time,
    symbol,
    '1d' as timeframe,
    FIRST(open, time) as open,
    MAX(high) as high,
    MIN(low) as low,
    LAST(close, time) as close,
    SUM(volume) as volume,
    SUM(quote_volume) as quote_volume,
    SUM(trades_count) as trades_count
FROM candles
WHERE timeframe = '1m'
GROUP BY time_bucket('1 day', time), symbol;

-- Add refresh policies (update every 5 minutes)
SELECT add_continuous_aggregate_policy('candles_15m',
    start_offset => INTERVAL '1 day',
    end_offset => INTERVAL '5 minutes',
    schedule_interval => INTERVAL '5 minutes');

SELECT add_continuous_aggregate_policy('candles_1h',
    start_offset => INTERVAL '7 days',
    end_offset => INTERVAL '5 minutes',
    schedule_interval => INTERVAL '5 minutes');

SELECT add_continuous_aggregate_policy('candles_4h',
    start_offset => INTERVAL '30 days',
    end_offset => INTERVAL '5 minutes',
    schedule_interval => INTERVAL '5 minutes');

SELECT add_continuous_aggregate_policy('candles_1d',
    start_offset => INTERVAL '365 days',
    end_offset => INTERVAL '5 minutes',
    schedule_interval => INTERVAL '5 minutes');

-- ============================================================================
-- ORDERS TABLE
-- ============================================================================
CREATE TABLE orders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    exchange_order_id TEXT UNIQUE,
    symbol TEXT NOT NULL,
    side TEXT NOT NULL CHECK (side IN ('BUY', 'SELL')),
    order_type TEXT NOT NULL CHECK (order_type IN ('MARKET', 'LIMIT', 'STOP_LOSS', 'TAKE_PROFIT', 'OCO')),
    status TEXT NOT NULL CHECK (status IN ('PENDING', 'OPEN', 'PARTIALLY_FILLED', 'FILLED', 'CANCELLED', 'REJECTED', 'EXPIRED')),
    price DECIMAL(20, 8),
    stop_price DECIMAL(20, 8),
    size DECIMAL(20, 8) NOT NULL,
    filled_size DECIMAL(20, 8) DEFAULT 0,
    average_fill_price DECIMAL(20, 8),
    commission DECIMAL(20, 8),
    commission_asset TEXT,
    time_in_force TEXT DEFAULT 'GTC',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    filled_at TIMESTAMPTZ,
    metadata JSONB
);

CREATE INDEX idx_orders_symbol ON orders (symbol);
CREATE INDEX idx_orders_status ON orders (status);
CREATE INDEX idx_orders_created_at ON orders (created_at DESC);
CREATE INDEX idx_orders_exchange_id ON orders (exchange_order_id) WHERE exchange_order_id IS NOT NULL;

-- ============================================================================
-- TRADES TABLE
-- ============================================================================
CREATE TABLE trades (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id UUID REFERENCES orders(id),
    exchange_trade_id TEXT,
    symbol TEXT NOT NULL,
    side TEXT NOT NULL CHECK (side IN ('BUY', 'SELL')),
    price DECIMAL(20, 8) NOT NULL,
    size DECIMAL(20, 8) NOT NULL,
    commission DECIMAL(20, 8),
    commission_asset TEXT,
    realized_pnl DECIMAL(20, 8),
    executed_at TIMESTAMPTZ NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    metadata JSONB
);

CREATE INDEX idx_trades_order_id ON trades (order_id);
CREATE INDEX idx_trades_symbol ON trades (symbol);
CREATE INDEX idx_trades_executed_at ON trades (executed_at DESC);

-- ============================================================================
-- POSITIONS TABLE
-- ============================================================================
CREATE TABLE positions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    symbol TEXT NOT NULL,
    side TEXT NOT NULL CHECK (side IN ('LONG', 'SHORT')),
    size DECIMAL(20, 8) NOT NULL,
    entry_price DECIMAL(20, 8) NOT NULL,
    current_price DECIMAL(20, 8),
    stop_loss DECIMAL(20, 8),
    take_profit DECIMAL(20, 8),
    unrealized_pnl DECIMAL(20, 8),
    realized_pnl DECIMAL(20, 8) DEFAULT 0,
    status TEXT NOT NULL CHECK (status IN ('OPEN', 'CLOSED')),
    opened_at TIMESTAMPTZ NOT NULL,
    closed_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    metadata JSONB
);

CREATE INDEX idx_positions_symbol ON positions (symbol);
CREATE INDEX idx_positions_status ON positions (status);
CREATE INDEX idx_positions_opened_at ON positions (opened_at DESC);

-- ============================================================================
-- PORTFOLIO TABLE (Snapshot of portfolio state)
-- ============================================================================
CREATE TABLE portfolio_snapshots (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    timestamp TIMESTAMPTZ NOT NULL,
    total_value DECIMAL(20, 8) NOT NULL,
    available_balance DECIMAL(20, 8) NOT NULL,
    total_unrealized_pnl DECIMAL(20, 8),
    total_realized_pnl DECIMAL(20, 8),
    open_positions_count INTEGER,
    total_exposure DECIMAL(20, 8),
    leverage DECIMAL(10, 4),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    metadata JSONB
);

SELECT create_hypertable('portfolio_snapshots', 'timestamp', if_not_exists => TRUE);
CREATE INDEX idx_portfolio_timestamp ON portfolio_snapshots (timestamp DESC);

-- ============================================================================
-- SIGNALS TABLE (Trading signals generated by strategies)
-- ============================================================================
CREATE TABLE signals (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    strategy_name TEXT NOT NULL,
    symbol TEXT NOT NULL,
    side TEXT NOT NULL CHECK (side IN ('BUY', 'SELL')),
    entry_price DECIMAL(20, 8),
    stop_loss DECIMAL(20, 8),
    take_profit DECIMAL(20, 8),
    confidence DECIMAL(5, 4) CHECK (confidence >= 0 AND confidence <= 1),
    timeframe TEXT,
    generated_at TIMESTAMPTZ NOT NULL,
    executed BOOLEAN DEFAULT FALSE,
    order_id UUID REFERENCES orders(id),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    metadata JSONB
);

SELECT create_hypertable('signals', 'generated_at', if_not_exists => TRUE);
CREATE INDEX idx_signals_symbol ON signals (symbol);
CREATE INDEX idx_signals_strategy ON signals (strategy_name);
CREATE INDEX idx_signals_executed ON signals (executed);

-- ============================================================================
-- BACKTEST RESULTS TABLE
-- ============================================================================
CREATE TABLE backtest_results (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    strategy_name TEXT NOT NULL,
    symbols TEXT[] NOT NULL,
    start_date TIMESTAMPTZ NOT NULL,
    end_date TIMESTAMPTZ NOT NULL,
    initial_capital DECIMAL(20, 8) NOT NULL,
    final_capital DECIMAL(20, 8) NOT NULL,
    total_return DECIMAL(10, 4),
    sharpe_ratio DECIMAL(10, 4),
    sortino_ratio DECIMAL(10, 4),
    max_drawdown DECIMAL(10, 4),
    win_rate DECIMAL(10, 4),
    profit_factor DECIMAL(10, 4),
    total_trades INTEGER,
    winning_trades INTEGER,
    losing_trades INTEGER,
    avg_win DECIMAL(20, 8),
    avg_loss DECIMAL(20, 8),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    parameters JSONB,
    equity_curve JSONB,
    trades JSONB
);

CREATE INDEX idx_backtest_strategy ON backtest_results (strategy_name);
CREATE INDEX idx_backtest_created_at ON backtest_results (created_at DESC);

-- ============================================================================
-- SYSTEM EVENTS TABLE (Audit log)
-- ============================================================================
CREATE TABLE system_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    event_type TEXT NOT NULL,
    severity TEXT NOT NULL CHECK (severity IN ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')),
    message TEXT NOT NULL,
    timestamp TIMESTAMPTZ NOT NULL,
    source TEXT,
    user_id TEXT,
    metadata JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

SELECT create_hypertable('system_events', 'timestamp', if_not_exists => TRUE);
CREATE INDEX idx_events_type ON system_events (event_type);
CREATE INDEX idx_events_severity ON system_events (severity);
CREATE INDEX idx_events_timestamp ON system_events (timestamp DESC);

-- ============================================================================
-- COMPRESSION POLICIES (Save disk space for old data)
-- ============================================================================

-- Compress candles older than 7 days
SELECT add_compression_policy('candles', INTERVAL '7 days');

-- Compress portfolio snapshots older than 30 days
SELECT add_compression_policy('portfolio_snapshots', INTERVAL '30 days');

-- Compress signals older than 30 days
SELECT add_compression_policy('signals', INTERVAL '30 days');

-- Compress system events older than 90 days
SELECT add_compression_policy('system_events', INTERVAL '90 days');

-- ============================================================================
-- RETENTION POLICIES (Delete very old data)
-- ============================================================================

-- Keep candles for 2 years
SELECT add_retention_policy('candles', INTERVAL '730 days');

-- Keep system events for 1 year
SELECT add_retention_policy('system_events', INTERVAL '365 days');

-- ============================================================================
-- FUNCTIONS
-- ============================================================================

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Triggers for updated_at
CREATE TRIGGER update_orders_updated_at BEFORE UPDATE ON orders
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_positions_updated_at BEFORE UPDATE ON positions
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ============================================================================
-- GRANTS (Security)
-- ============================================================================

-- Grant permissions to trader user
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO trader;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO trader;
