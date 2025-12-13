
import asyncio
import os
import pandas as pd
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

async def inspect():
    if not DATABASE_URL:
        print("ERROR: DATABASE_URL not found")
        return
        
    engine = create_async_engine(DATABASE_URL, echo=False, connect_args={"ssl": False})
    
    try:
        async with engine.connect() as conn:
            print("\n--- Checking 'recommendations' Table ---")
            result = await conn.execute(text("SELECT * FROM recommendations LIMIT 10"))
            rows = result.fetchall()
            
            if rows:
                keys = result.keys()
                df = pd.DataFrame(rows, columns=keys)
                print(df[['title', 'priority', 'expected_impact', 'estimated_monthly_revenue']].to_string())
            else:
                print("Table 'recommendations' is empty.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await engine.dispose()

if __name__ == "__main__":
    asyncio.run(inspect())
