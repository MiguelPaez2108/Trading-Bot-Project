"""
Settings management using Pydantic Settings.

Loads configuration from environment variables and config files.
"""
from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class DatabaseSettings(BaseSettings):
    """Database configuration."""
    
    host: str = Field(default="localhost", description="Database host")
    port: int = Field(default=5432, description="Database port")
    name: str = Field(default="trading", description="Database name")
    user: str = Field(default="trader", description="Database user")
    password: str = Field(default="password", description="Database password")
    pool_size: int = Field(default=20, description="Connection pool size")
    max_overflow: int = Field(default=10, description="Max pool overflow")
    pool_timeout: int = Field(default=30, description="Pool timeout in seconds")
    echo: bool = Field(default=False, description="Echo SQL queries")
    
    model_config = SettingsConfigDict(env_prefix="DB_")


class RedisSettings(BaseSettings):
    """Redis configuration."""
    
    host: str = Field(default="localhost", description="Redis host")
    port: int = Field(default=6379, description="Redis port")
    db: int = Field(default=0, description="Redis database number")
    password: Optional[str] = Field(default=None, description="Redis password")
    max_connections: int = Field(default=50, description="Max connections in pool")
    socket_timeout: int = Field(default=5, description="Socket timeout in seconds")
    socket_connect_timeout: int = Field(default=5, description="Connection timeout")
    decode_responses: bool = Field(default=True, description="Decode responses to strings")
    
    model_config = SettingsConfigDict(env_prefix="REDIS_")


class ExchangeSettings(BaseSettings):
    """Exchange API configuration."""
    
    binance_api_key: str = Field(default="", description="Binance API key")
    binance_secret_key: str = Field(default="", description="Binance secret key")
    binance_testnet: bool = Field(default=True, description="Use Binance testnet")
    
    hyperliquid_api_key: str = Field(default="", description="HyperLiquid API key")
    hyperliquid_secret_key: str = Field(default="", description="HyperLiquid secret key")
    
    rate_limit_requests_per_minute: int = Field(default=1200, description="Rate limit")
    
    model_config = SettingsConfigDict(env_prefix="EXCHANGE_")


class RiskSettings(BaseSettings):
    """Risk management configuration."""
    
    max_position_size_usd: float = Field(default=1000.0, description="Max position size in USD")
    max_positions: int = Field(default=3, description="Max concurrent positions")
    max_leverage: float = Field(default=3.0, description="Max leverage")
    max_daily_loss_pct: float = Field(default=0.05, description="Max daily loss %")
    require_stop_loss: bool = Field(default=True, description="Require stop loss on all orders")
    require_take_profit: bool = Field(default=True, description="Require take profit")
    max_correlation: float = Field(default=0.7, description="Max correlation between positions")
    
    model_config = SettingsConfigDict(env_prefix="RISK_")


class Settings(BaseSettings):
    """Main application settings."""
    
    # Environment
    environment: str = Field(default="development", description="Environment name")
    debug: bool = Field(default=False, description="Debug mode")
    
    # Mode
    mode: str = Field(default="paper", description="Trading mode: paper or live")
    
    # Logging
    log_level: str = Field(default="INFO", description="Logging level")
    log_format: str = Field(default="json", description="Log format: json or text")
    
    # Sub-configurations
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)
    redis: RedisSettings = Field(default_factory=RedisSettings)
    exchange: ExchangeSettings = Field(default_factory=ExchangeSettings)
    risk: RiskSettings = Field(default_factory=RiskSettings)
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        env_nested_delimiter="__"
    )


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.
    
    Returns:
        Settings instance loaded from environment
    """
    return Settings()
