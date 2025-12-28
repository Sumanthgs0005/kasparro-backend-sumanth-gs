import pandas as pd
from pathlib import Path
from typing import List
from app.schemas.coin_raw import CoinRaw
from app.ingestion.base import BaseIngestor
from datetime import datetime

class CSVIngestor(BaseIngestor):
    def __init__(self, filepath: str):
        self.filepath = Path(filepath)
    
    async def ingest(self, limit: int = 1000) -> List[CoinRaw]:
        if not self.filepath.exists():
            raise FileNotFoundError(f"CSV file not found: {self.filepath}")
        
        df = pd.read_csv(self.filepath)
        df = df.head(limit)
        
        coins = []
        for _, row in df.iterrows():
            coin = CoinRaw(
                id=str(row.get('id', row.get('symbol', 'unknown'))),
                symbol=str(row.get('symbol', 'unknown')).upper(),
                name=str(row.get('name', 'Unknown')),
                price_usd=float(row.get('price_usd', 0)) if pd.notna(row.get('price_usd')) else None,
                market_cap_usd=float(row.get('market_cap_usd', 0)) if pd.notna(row.get('market_cap_usd')) else None,
                volume_24h_usd=float(row.get('volume_24h_usd', 0)) if pd.notna(row.get('volume_24h_usd')) else None
            )
            coins.append(coin)
        
        return coins
    
    def get_source_name(self) -> str:
        return f"csv:{self.filepath.name}"
