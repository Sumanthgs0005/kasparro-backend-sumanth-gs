from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models import CoinNormalized
from app.schemas.coin_normalized import CoinNormalized as CoinNormalizedSchema
from typing import List, Tuple
import logging

logger = logging.getLogger(__name__)

class CoinService:
    @staticmethod
    async def get_normalized_coins(
        session: AsyncSession,
        limit: int = 50,
        offset: int = 0,
        source: str | None = None,
        symbol: str | None = None
    ) -> Tuple[List[CoinNormalizedSchema], int]:
        """Get paginated normalized coins with optional filters"""
        query = select(CoinNormalized)

        if source:
            query = query.where(CoinNormalized.source == source)
        if symbol:
            query = query.where(CoinNormalized.symbol == symbol.upper())

        # Get total count
        count_query = select(func.count()).select_from(CoinNormalized)
        if source:
            count_query = count_query.where(CoinNormalized.source == source)
        if symbol:
            count_query = count_query.where(CoinNormalized.symbol == symbol.upper())
        
        total = await session.execute(count_query)
        total_count = total.scalar() or 0

        # Get paginated results
        query = query.order_by(CoinNormalized.updated_at.desc()).offset(offset).limit(limit)
        result = await session.execute(query)
        coins = result.scalars().all()

        return [CoinNormalizedSchema.model_validate(c) for c in coins], total_count

    @staticmethod
    async def get_coin_by_symbol(session: AsyncSession, symbol: str) -> CoinNormalizedSchema | None:
        """Get a single coin by symbol"""
        result = await session.execute(
            select(CoinNormalized).where(CoinNormalized.symbol == symbol.upper()).limit(1)
        )
        coin = result.scalars().first()
        return CoinNormalizedSchema.model_validate(coin) if coin else None

    @staticmethod
    async def get_distinct_sources(session: AsyncSession) -> List[str]:
        """Get all distinct data sources"""
        result = await session.execute(select(CoinNormalized.source).distinct())
        return result.scalars().all()
