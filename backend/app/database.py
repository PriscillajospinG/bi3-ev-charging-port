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

# Explicitly require SSL for TimescaleDB
# asyncpg with SQLAlchemy sometimes needs an SSLContext object for "require",
# or we can pass it via the query string if the driver supports it.
# However, for many cloud providers, a simple context with verify_mode=CERT_NONE (if using self-signed or system CA) works best.
import ssl
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

connect_args = {"ssl": ctx}

# Create engine with connect_args
engine = create_async_engine(DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://"), echo=False, connect_args=connect_args)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
