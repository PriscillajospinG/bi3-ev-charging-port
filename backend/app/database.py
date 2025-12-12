import os
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

# Get DATABASE_URL and clean it (stop at first newline or extra content)
raw_db_url = os.getenv("DATABASE_URL", "")
# Extract just the first line if there are multiple
DATABASE_URL = raw_db_url.split('\n')[0].split('OPEN_CHARGE')[0].strip() if raw_db_url else None

USE_SQLITE = False
connect_args = {}

if DATABASE_URL and DATABASE_URL.startswith("postgresql"):
    # PostgreSQL/TimescaleDB mode
    import ssl
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    connect_args = {"ssl": ctx}
    engine_url = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")
else:
    # Fallback to SQLite for dev/testing
    USE_SQLITE = True
    engine_url = "sqlite+aiosqlite:///./ev_charging.db"
    connect_args = {"check_same_thread": False}
    print("⚠️  Using SQLite fallback database for development")

# Create engine with connect_args
engine = create_async_engine(engine_url, echo=False, connect_args=connect_args)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

