from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from decimal import Decimal

class CoinNormalized(BaseModel):
    coin_id: str
    symbol: str
    name: str
    price_usd: Optional[Decimal] = None
    market_cap_usd: Optional[Decimal] = None
    volume_24h_usd: Optional[Decimal] = None
    platform_id: Optional[str] = None
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        from_attributes = True
