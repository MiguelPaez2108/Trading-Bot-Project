"""
Application Settings
Pydantic settings with environment variable support
"""
from functools import lru_cache
from typing import Optional
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # Application
    app_name: str = "trading-system"
    app_version: str = "0.2.0"
    environment: str = Field(default="development", pattern="^(development|staging|production|test)$")
    debug: bool = False
    log_level: str = "INFO"
    
    # Database
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_db: str = "trading_db"
    postgres_user: str = "trading_user"
    postgres_password: str = "trading_password"
    postgres_pool_size: int = 20
    postgres_max_overflow: int = 10
    
    # Redis Cache
    redis_cache_host: str = "localhost"
    redis_cache_port: int = 6379
    redis_cache_db: int = 0
    redis_cache_password: Optional[str] = None
    
    # Redis Streams
    redis_streams_host: str = "localhost"
    redis_streams_port: int = 6380
    redis_streams_db: int = 0
    redis_streams_password: Optional[str] = None
    
    # Trading
    trading_mode: str = Field(default="paper", pattern="^(paper|live)$")
    initial_capital: float = 10000.0
    max_position_size_pct: float = 10.0
    max_total_exposure_pct: float = 50.0
    max_daily_loss_pct: float = 5.0
    max_leverage: float = 3.0
    
    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_workers: int = 4
    api_reload: bool = True
    api_secret_key: str = "change_this_secret_key"
    
    # Monitoring
    prometheus_port: int = 9090
    prometheus_enabled: bool = True
    
    @property
    def database_url(self) -> str:
        """Construct async database URL"""
        return (
            f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )
    
    @property
    def redis_cache_url(self) -> str:
        """Construct Redis cache URL"""
        auth = f":{self.redis_cache_password}@" if self.redis_cache_password else ""
        return f"redis://{auth}{self.redis_cache_host}:{self.redis_cache_port}/{self.redis_cache_db}"
    
    @property
    def redis_streams_url(self) -> str:
        """Construct Redis streams URL"""
        auth = f":{self.redis_streams_password}@" if self.redis_streams_password else ""
        return f"redis://{auth}{self.redis_streams_host}:{self.redis_streams_port}/{self.redis_streams_db}"
    
    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        """Validate log level"""
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if v.upper() not in valid_levels:
            raise ValueError(f"log_level must be one of {valid_levels}")
        return v.upper()


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.
    
    Returns:
        Settings: Application settings
    """
    return Settings()
