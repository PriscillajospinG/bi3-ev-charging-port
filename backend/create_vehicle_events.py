# Migration script for vehicle_events table
import asyncio
from sqlalchemy import text
from app.database import engine

async def migrate_vehicle_events():
    print("Migrating DB schema for Vehicle Events...")
    async with engine.begin() as conn:
        try:
            # Create table locally via raw SQL to ensure it exists for now
            # In production, use Alembic. 
            # We use IF NOT EXISTS to be safe.
            await conn.execute(text("""
                CREATE TABLE IF NOT EXISTS vehicle_events (
                    id SERIAL PRIMARY KEY,
                    timestamp TIMESTAMPTZ,
                    video_source VARCHAR,
                    class_name VARCHAR,
                    confidence FLOAT,
                    event_type VARCHAR
                );
            """))
            print("Created 'vehicle_events' table.")
            
            # Create index on timestamp
            await conn.execute(text("CREATE INDEX IF NOT EXISTS idx_vehicle_timestamp ON vehicle_events (timestamp DESC);"))
            print("Created index on timestamp.")
            
        except Exception as e:
            print(f"Migration error: {e}")

if __name__ == "__main__":
    asyncio.run(migrate_vehicle_events())
