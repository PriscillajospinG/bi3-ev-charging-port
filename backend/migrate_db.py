# Simple migration script to add missing column
import asyncio
from sqlalchemy import text
from app.database import engine

async def migrate():
    print("Migrating DB schema...")
    async with engine.begin() as conn:
        try:
            await conn.execute(text("ALTER TABLE model_predictions ADD COLUMN IF NOT EXISTS source_file VARCHAR"))
            print("Added 'source_file' column.")
        except Exception as e:
            print(f"Migration error (might already exist): {e}")

if __name__ == "__main__":
    asyncio.run(migrate())
