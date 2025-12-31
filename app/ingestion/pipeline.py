from typing import List
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from app.ingestion.csv_ingestor import CSVIngestor
from app.ingestion.coinpaprika_ingestor import CoinPaprikaIngestor
from app.ingestion.coingecko_ingestor import CoinGeckoIngestor
from app.schemas.coin_raw import CoinRaw
from app.models import CoinNormalized, ETLRun
from app.services.etl_service import ETLService
import logging
from decimal import Decimal

logger = logging.getLogger(__name__)

class IngestionPipeline:
    """
    Main ETL Pipeline for Kasparro Backend
    
    Flow:
    1. Create ETL Run record (tracking)
    2. Run all ingestors (CSV + API sources)
    3. Collect raw coin data
    4. Normalize data to unified schema
    5. Insert into coins_normalized table
    6. Update ETL Run with status (success/failed)
    7. Clean up old records (optional)
    """

    @staticmethod
    async def run_all_ingestors(
        session: AsyncSession,
        limit: int = 100,
        clear_old_records: bool = False
    ) -> int:
        """
        Run complete ETL pipeline.
        
        Args:
            session: AsyncSession for database operations
            limit: Max records per ingestor
            clear_old_records: Clear normalized data before ingesting (default: False for incremental)
        
        Returns:
            Number of normalized records inserted
        """
        start_time = datetime.utcnow()
        logger.info("=" * 80)
        logger.info("🚀 STARTING ETL PIPELINE")
        logger.info("=" * 80)

        # Step 1: Create ETL Run record
        run = await ETLService.create_run(session, source="multi-source")
        logger.info(f"📋 ETL Run ID: {run.id}")
        
        try:
            # Step 2: Clear old data if requested (for full reload)
            if clear_old_records:
                logger.info("🧹 Clearing old normalized records...")
                await session.execute(delete(CoinNormalized))
                await session.commit()
                logger.info("✅ Old records cleared")

            # Step 3: Collect all raw coins from all sources
            all_coins: List[CoinRaw] = []
            total_raw = 0

            # 3a: CSV Ingestor
            logger.info("\n📄 CSV INGESTION")
            logger.info("-" * 40)
            try:
                csv_ingestor = CSVIngestor("data/coins_source.csv")
                csv_coins = await csv_ingestor.ingest(limit)
                all_coins.extend(csv_coins)
                total_raw += len(csv_coins)
                logger.info(f"✅ CSV: {len(csv_coins)} coins ingested")
            except Exception as e:
                logger.error(f"❌ CSV Ingestor failed: {e}")
                # Don't fail entire pipeline if one source fails
                pass

            # 3b: CoinPaprika Ingestor
            logger.info("\n💰 COINPAPRIKA INGESTION")
            logger.info("-" * 40)
            try:
                paprika_ingestor = CoinPaprikaIngestor()
                paprika_coins = await paprika_ingestor.ingest(limit)
                all_coins.extend(paprika_coins)
                total_raw += len(paprika_coins)
                logger.info(f"✅ CoinPaprika: {len(paprika_coins)} coins ingested")
            except Exception as e:
                logger.error(f"❌ CoinPaprika Ingestor failed: {e}")
                pass

            # 3c: CoinGecko Ingestor
            logger.info("\n🦎 COINGECKO INGESTION")
            logger.info("-" * 40)
            try:
                gecko_ingestor = CoinGeckoIngestor()
                gecko_coins = await gecko_ingestor.ingest(limit)
                all_coins.extend(gecko_coins)
                total_raw += len(gecko_coins)
                logger.info(f"✅ CoinGecko: {len(gecko_coins)} coins ingested")
            except Exception as e:
                logger.error(f"❌ CoinGecko Ingestor failed: {e}")
                pass

            logger.info("\n" + "=" * 40)
            logger.info(f"📊 Total raw records: {total_raw}")
            logger.info("=" * 40)

            # Step 4: Normalize and insert data
            logger.info("\n🔄 NORMALIZATION PHASE")
            logger.info("-" * 40)
            
            normalized_count = 0
            deduplicate_by_symbol = {}  # Track coins by symbol to avoid duplicates

            for coin in all_coins:
                try:
                    symbol_upper = coin.symbol.upper()
                    
                    # Deduplication: Keep the one with price (prioritize non-null prices)
                    if symbol_upper in deduplicate_by_symbol:
                        existing = deduplicate_by_symbol[symbol_upper]
                        if coin.price_usd and not existing.price_usd:
                            deduplicate_by_symbol[symbol_upper] = coin
                        continue
                    else:
                        deduplicate_by_symbol[symbol_upper] = coin

                    # Create normalized record
                    normalized_model = CoinNormalized(
                        coin_id=coin.id.lower(),
                        symbol=symbol_upper,
                        name=coin.name,
                        price_usd=Decimal(str(coin.price_usd)) if coin.price_usd else None,
                        market_cap_usd=Decimal(str(coin.market_cap_usd)) if coin.market_cap_usd else None,
                        volume_24h_usd=Decimal(str(coin.volume_24h_usd)) if coin.volume_24h_usd else None,
                        platform_id=coin.platform_id,
                        source=coin.id.split('_')[0] if '_' in coin.id else "unknown",
                    )
                    session.add(normalized_model)
                    normalized_count += 1

                except Exception as e:
                    logger.warning(f"⚠️  Failed to normalize coin {coin.symbol}: {e}")
                    continue

            # Batch commit
            if normalized_count > 0:
                await session.commit()
                logger.info(f"✅ Normalized and inserted: {normalized_count} records")
            else:
                logger.warning("⚠️  No records normalized")

            # Step 5: Update ETL Run with success
            run.status = "completed"
            run.total_records = total_raw
            run.processed_records = normalized_count
            run.completed_at = datetime.utcnow()
            
            if run.started_at:
                duration = (run.completed_at - run.started_at).total_seconds()
                run.duration_seconds = int(duration)
                logger.info(f"⏱️  Duration: {run.duration_seconds}s")

            await session.commit()

            logger.info("\n" + "=" * 80)
            logger.info(f"✅ ETL PIPELINE COMPLETED SUCCESSFULLY")
            logger.info(f"   Total Raw: {total_raw} | Normalized: {normalized_count}")
            logger.info("=" * 80 + "\n")

            return normalized_count

        except Exception as e:
            # Step 5: Handle failure
            logger.error(f"\n❌ ETL PIPELINE FAILED: {e}", exc_info=True)
            
            run.status = "failed"
            run.error_message = str(e)
            run.completed_at = datetime.utcnow()
            
            if run.started_at:
                duration = (run.completed_at - run.started_at).total_seconds()
                run.duration_seconds = int(duration)

            await session.commit()
            
            logger.info("\n" + "=" * 80)
            logger.info(f"❌ ETL PIPELINE FAILED")
            logger.info(f"   Error: {str(e)}")
            logger.info("=" * 80 + "\n")
            
            raise

    @staticmethod
    async def run_incremental(
        session: AsyncSession,
        limit: int = 50,
        last_n_hours: int = 24
    ) -> int:
        """
        Run incremental ETL (only process new/updated records).
        
        Args:
            session: AsyncSession for database operations
            limit: Max records per ingestor
            last_n_hours: Only keep records updated in last N hours
        
        Returns:
            Number of new normalized records inserted
        """
        logger.info("🔄 Starting INCREMENTAL ETL pipeline")
        
        # Delete records older than last_n_hours
        cutoff_time = datetime.utcnow() - timedelta(hours=last_n_hours)
        deleted_result = await session.execute(
            delete(CoinNormalized).where(CoinNormalized.updated_at < cutoff_time)
        )
        await session.commit()
        logger.info(f"🧹 Removed {deleted_result.rowcount} old records (older than {last_n_hours}h)")
        
        # Run normal ingestion on fresh data
        return await IngestionPipeline.run_all_ingestors(
            session,
            limit=limit,
            clear_old_records=False
        )

    @staticmethod
    async def run_full_reload(
        session: AsyncSession,
        limit: int = 250
    ) -> int:
        """
        Run full reload ETL (clear everything and re-ingest).
        
        Args:
            session: AsyncSession for database operations
            limit: Max records per ingestor (higher for full reload)
        
        Returns:
            Number of normalized records inserted
        """
        logger.info("🔄 Starting FULL RELOAD ETL pipeline")
        
        return await IngestionPipeline.run_all_ingestors(
            session,
            limit=limit,
            clear_old_records=True
        )
