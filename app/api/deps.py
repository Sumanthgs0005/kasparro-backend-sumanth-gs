from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_session
from app.core.config import settings

async def get_db(session: AsyncSession = Depends(get_session)):
    try:
        yield session
    finally:
        await session.close()
