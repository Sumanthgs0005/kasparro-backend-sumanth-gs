from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_session
from app.services.stats_service import StatsService
from app.services.coin_service import CoinService
from app.schemas.coin_normalized import CoinNormalized

router = APIRouter()

@router.get("/stats")
async def get_stats(session: AsyncSession = Depends(get_session)):
    return await StatsService.get_stats(session)

@router.get("/coins", response_model=list[CoinNormalized])
async def list_coins(limit: int = 50, session: AsyncSession = Depends(get_session)):
    return await CoinService.get_normalized_coins(session, limit)
