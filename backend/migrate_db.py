# Simple migration script to add missing column
import asyncio
from sqlalchemy import text
from app.database import engine

async def migrate():
    print("Migrating DB schema...")
    async with engine.begin() as conn:
        try:
            await conn.execute(text("ALTER TABLE model_predictions ADD COLUMN IF NOT EXISTS source_file VARCHAR"))
            print("Added 'source_file' column to model_predictions.")
        except Exception as e:
            print(f"Migration error (model_predictions): {e}")

        try:
            await conn.execute(text("ALTER TABLE recommendations ADD COLUMN IF NOT EXISTS estimated_monthly_revenue VARCHAR"))
            print("Added 'estimated_monthly_revenue' column to recommendations.")
        except Exception as e:
            print(f"Migration error (estimated_monthly_revenue): {e}")

        try:
            await conn.execute(text("ALTER TABLE recommendations ADD COLUMN IF NOT EXISTS key_insights VARCHAR"))
            print("Added 'key_insights' column to recommendations.")
        except Exception as e:
            print(f"Migration error (key_insights): {e}")

if __name__ == "__main__":
    asyncio.run(migrate())
