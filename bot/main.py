import asyncio
from nio import AsyncClient, MatrixRoom, RoomMessageText
from asyncio import sleep

import sync

host = "127.0.0.1"
port = "5505"
url = f"{host}:{port}"
scheme = "http://"


async def main():
    client = AsyncClient("https://mtx.nlion.nl", "@youtube-downloader:nlion.nl")
    print(await client.login("@Q@G8E8xiAFL&w74"))

    while True:
        await sync.sync(scheme, url, client)
        await sleep(10)


try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("Exited")