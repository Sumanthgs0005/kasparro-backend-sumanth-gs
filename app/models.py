from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Enum
from sqlalchemy.sql import func
from app.core.db import Base
from enum import Enum as PyEnum

class ETLStatus(str, PyEnum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

class CoinRaw(Base):
    __tablename__ = "coin_raw"
    id = Column(Integer, primary_key=True, index=True)
    coin_id = Column(String, index=True)
    symbol = Column(String, index=True)
    name = Column(String)
    platform_id = Column(String, nullable=True)
    price_usd = Column(Float, nullable=True)
    market_cap_usd = Column(Float, nullable=True)
    volume_24h_usd = Column(Float, nullable=True)
    source = Column(String)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

class CoinNormalized(Base):
    __tablename__ = "coin_normalized"
    id = Column(Integer, primary_key=True, index=True)
    coin_id = Column(String, unique=True, index=True)
    symbol = Column(String, index=True)
    name = Column(String)
    price_usd = Column(Float, nullable=True)
    market_cap_usd = Column(Float, nullable=True)
    volume_24h_usd = Column(Float, nullable=True)
    platform_id = Column(String, nullable=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class ETLRun(Base):
    __tablename__ = "etl_runs"
    id = Column(Integer, primary_key=True, index=True)
    source = Column(String, index=True)
    total_records = Column(Integer)
    processed_records = Column(Integer, default=0)
    status = Column(Enum(ETLStatus), default=ETLStatus.PENDING)
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    error_message = Column(Text, nullable=True)
