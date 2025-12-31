from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_session
from app.services.etl_service import ETLService
from app.ingestion.csv_ingestor import CSVIngestor
from app.schemas.etl_run import ETLRunsCreate
import tempfile
import os

router = APIRouter()

@router.post("/ingest/csv")
async def ingest_csv(
    file: UploadFile = File(...),
    session: AsyncSession = Depends(get_session)
):
    if not file.filename.endswith('.csv'):
        raise HTTPException(400, "Only CSV files allowed")
    
    with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name
    
    try:
        ingestor = CSVIngestor(tmp_path)
        coins = await ingestor.ingest()
        
        run = ETLRunsCreate(source=ingestor.get_source_name(), total_records=len(coins))
        etl_run = await ETLService.create_run(session, run)
        
        return {"run_id": etl_run.id, "coins_ingested": len(coins)}
    finally:
        os.unlink(tmp_path)
