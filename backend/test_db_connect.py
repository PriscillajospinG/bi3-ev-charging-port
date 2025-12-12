
import asyncio
import os
import asyncpg
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
print(f"Testing connection to: {DATABASE_URL}")

async def test_connection():
    try:
        # Use simpler connection arg first
        engine = create_async_engine(DATABASE_URL, echo=True, connect_args={"ssl": "require"})
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT 1"))
            print("Connection Successful! Result:", result.scalar())
    except Exception as e:
        print(f"Connection Failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_connection())
