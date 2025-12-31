from app.ingestion.base import BaseIngestor
from app.schemas.coin_raw import CoinRaw
import httpx

class CoinPaprikaIngestor(BaseIngestor):  # or CoinGeckoIngestor
    async def ingest(self, limit: int = 100) -> list[CoinRaw]:
        async with httpx.AsyncClient() as client:
            resp = await client.get("https://api.coinpaprika.com/v1/coins", params={"limit": limit})
            # Parse and return CoinRaw list (stub)
            return []
    
    def get_source_name(self) -> str:
        return "coinpaprika"  # or "coingecko"
