from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import db
from app.schemas.etl_run import ETLRunsCreate, ETLRuns
from app.models import ETLRun  # Will create later
from datetime import datetime

class ETLService:
    @classmethod
    async def create_run(cls, session: AsyncSession, run: ETLRunsCreate) -> ETLRuns:
        db_run = ETLRun(**run.dict())
        session.add(db_run)
        await session.commit()
        await session.refresh(db_run)
        return ETLRuns.from_orm(db_run)
    
    @classmethod
    async def update_run_status(cls, session: AsyncSession, run_id: int, status: str, processed: int = 0, error: str = None):
        run = await session.get(ETLRun, run_id)
        if run:
            run.status = status
            run.processed_records = processed
            if error:
                run.error_message = error
            if status == "completed":
                run.completed_at = datetime.utcnow()
            await session.commit()
