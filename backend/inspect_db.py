
import asyncio
import os
import pandas as pd
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# SSL Trick for this specific cloud instance
# We know from previous debugging that we need to force ssl=False logic or manipulate the string
# The current efficient fix used in database.py is connect_args={"ssl": False}

async def inspect():
    if not DATABASE_URL:
        print("ERROR: DATABASE_URL not found in .env")
        return

    print(f"Connecting to: {DATABASE_URL.split('@')[1]}") # Hide password for safety
    
    try:
        # Create Engine with the SSL Fix
        engine = create_async_engine(DATABASE_URL, echo=False, connect_args={"ssl": False})
        
        async with engine.connect() as conn:
            print("\n--- Checking 'ev_events' Table ---")
            
            # Count
            result = await conn.execute(text("SELECT count(*) FROM ev_events"))
            count = result.scalar()
            print(f"Total Rows: {count}")
            
            # First 5 rows
            print("\n--- First 5 Rows ---")
            result = await conn.execute(text("SELECT * FROM ev_events ORDER BY timestamp DESC LIMIT 5"))
            rows = result.fetchall()
            
            # Print nicely
            if rows:
                # Get column names
                keys = result.keys()
                df = pd.DataFrame(rows, columns=keys)
                print(df.to_string())
            else:
                print("Table is empty.")

    except Exception as e:
        print(f"\n❌ Connection Failed: {e}")
    finally:
        await engine.dispose()

if __name__ == "__main__":
    asyncio.run(inspect())
