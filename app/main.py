import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.db import db
from app.core.config import settings
from app.core.logging_config import setup_logging
from app.api import routes_health, routes_data, routes_stats
from app.ingestion.pipeline import IngestionPipeline

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

# Startup and shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("🚀 Starting Kasparro Backend...")
    try:
        await db.init_db()
        logger.info("✅ Database initialized")
    except Exception as e:
        logger.warning(f"Database init warning: {e}")
    
    # Optional: Run ETL on startup
    try:
        logger.info("🔄 Running initial ETL pipeline...")
        async with db.session_factory() as session:
            records = await IngestionPipeline.run_all_ingestors(session, limit=50)
            logger.info(f"✅ ETL pipeline completed: {records} normalized records inserted")
    except Exception as e:
        logger.warning(f"⚠️ Initial ETL failed (non-critical): {e}")
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down Kasparro Backend...")
    try:
        await db.close()
        logger.info("✅ Database closed")
    except Exception as e:
        logger.warning(f"Database close warning: {e}")

# Create FastAPI app
app = FastAPI(
    title="Kasparro Crypto Backend",
    description="Production-grade ETL & API for crypto data aggregation",
    version=settings.version,
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(routes_health.router, prefix="/health", tags=["health"])
app.include_router(routes_data.router, prefix="/data", tags=["data"])
app.include_router(routes_stats.router, prefix="/stats", tags=["stats"])

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint - returns API information"""
    return {
        "message": "Kasparro Backend - Crypto Data ETL API",
        "version": settings.version,
        "status": "operational",
        "endpoints": {
            "health": "/health/",
            "data": "/data/coins",
            "stats": "/stats/",
            "docs": "/docs",
            "redoc": "/redoc",
        }
    }
