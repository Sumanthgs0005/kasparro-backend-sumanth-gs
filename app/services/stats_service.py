from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func
from app.models import CoinNormalized, ETLRun

class StatsService:
    @classmethod
    async def get_stats(cls, session: AsyncSession):
        total_coins = await session.execute(select(func.count()).select_from(CoinNormalized))
        recent_etl = await session.execute(
            select(ETLRun).order_by(ETLRun.started_at.desc()).limit(5)
        )
        
        return {
            "total_coins": total_coins.scalar(),
            "recent_runs": [run.__dict__ for run in recent_etl.scalars().all()],
            "ingestion_status": "healthy"
        }
