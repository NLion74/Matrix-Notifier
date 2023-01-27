import asyncio
from nio import AsyncClient, MatrixRoom, RoomMessageText
from asyncio import sleep

import sync

# Server
host = "127.0.0.1"
port = "5505"
url = f"{host}:{port}"
scheme = "http://"

# Bot Creds
bot_name = "@bot_user:home.server"
bot_pass = "bot_pass"
home_server = "https://home.server"


async def main():
    client = AsyncClient(f"{home_server}", f"{bot_name}")
    print(await client.login(f"{bot_pass}"))

    while True:
        await sync.sync(scheme, url, client)
        await sleep(5)


try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("Exited")
