import asyncio
import random

async def human_delay():

    delay = random.uniform(1.0, 3.5)

    await asyncio.sleep(delay)
