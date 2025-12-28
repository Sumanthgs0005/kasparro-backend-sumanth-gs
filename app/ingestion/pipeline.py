from typing import List
from app.ingestion.base import BaseIngestor
from app.ingestion.csv_ingestor import CSVIngestor
from app.schemas.coin_raw import CoinRaw

class IngestionPipeline:
    @staticmethod
    async def run_all_ingestors(limit: int = 100) -> List[CoinRaw]:
        """Run all ingestors and aggregate results."""
        all_coins = []
        
        # CSV pipeline
        csv_ingestor = CSVIngestor("data/coins_source.csv")
        csv_coins = await csv_ingestor.ingest(limit)
        all_coins.extend(csv_coins)
        
        return all_coins
