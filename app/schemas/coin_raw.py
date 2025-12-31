from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class CoinRaw(BaseModel):
    id: str
    symbol: str
    name: str
    platform_id: Optional[str] = None
    price_usd: Optional[float] = None
    market_cap_usd: Optional[float] = None
    volume_24h_usd: Optional[float] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class CoinRawList(BaseModel):
    coins: List[CoinRaw]
    source: str
    ingested_at: datetime = Field(default_factory=datetime.utcnow)
