from abc import ABC, abstractmethod
from typing import List, Dict, Any
from app.schemas.coin_raw import CoinRaw

class BaseIngestor(ABC):
    @abstractmethod
    async def ingest(self, limit: int = 100) -> List[CoinRaw]:
        """Ingest raw coin data from source."""
        pass
    
    @abstractmethod
    def get_source_name(self) -> str:
        """Return source name for tracking."""
        pass
