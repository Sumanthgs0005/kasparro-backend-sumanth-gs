from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_session
from app.services.stats_service import StatsService

router = APIRouter()

@router.get("/")
async def health_check(session: AsyncSession = Depends(get_session)):
    stats = await StatsService.get_stats(session)
    return {
        "status": "healthy",
        "service": "kasparro-crypto-backend",
        "stats": stats
    }
