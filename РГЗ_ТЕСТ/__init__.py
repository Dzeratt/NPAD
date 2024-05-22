import asyncio
from main import main, conn

async def run():
    try:
        await main()
    finally:
        conn.close()

asyncio.run(run())
