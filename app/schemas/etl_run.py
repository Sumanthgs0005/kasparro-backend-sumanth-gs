from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum

class ETLStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

class ETLRunsCreate(BaseModel):
    source: str
    total_records: int
    status: ETLStatus = ETLStatus.PENDING

class ETLRuns(BaseModel):
    id: int
    source: str
    total_records: int
    processed_records: int
    status: ETLStatus
    started_at: datetime
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None
    
    class Config:
        from_attributes = True
