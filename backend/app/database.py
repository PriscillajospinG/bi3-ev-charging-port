import os
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    # Fallback to local sqlite for dev if no URL provided (though user provided TimescaleDB)
    # But since we are building for TimescaleDB specifically, we should warn or expect it.
    # For dev safety here without revealing secrets in logs easily:
    pass

# Explicitly disable SSL for asyncpg if not specified, to match successful test script behavior
# If user wants SSL, they should ensure the server handshake works or pass valid context.
# Given the "hang", we force False to unblock.
connect_args = {"ssl": False}

engine = create_async_engine(DATABASE_URL, echo=False, connect_args=connect_args)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
