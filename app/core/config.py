from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    app_name: str = "Kasparro Crypto Backend"
    version: str = "1.0.0"
    
    # Database
    database_url: str = "sqlite+aiosqlite:///./app.db"
    echo_db_queries: bool = False
    
    # APIs
    coingecko_api_url: str = "https://api.coingecko.com/api/v3"
    coinpaprika_api_url: str = "https://api.coinpaprika.com/v1"
    
    # Limits
    max_csv_rows: int = 10000
    max_ingestion_batch: int = 1000

    class Config:
        env_file = ".env"

settings = Settings()
