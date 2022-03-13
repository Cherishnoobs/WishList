import asyncio
from asyncio import tasks
from asyncio.log import logger

from model.log import get_logger
from model.crawer import Crawer

logger = get_logger('Main')

async def main():
    steamid = [76561198323399563]
    token = '71a7d4524266563df456abdede7f7145683d649e'

    c = Crawer(steamids=steamid, token=token)

    tasks = [
        asyncio.create_task(c.start())
    ]
    await asyncio.wait(tasks)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
