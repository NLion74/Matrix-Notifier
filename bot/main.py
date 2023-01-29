import asyncio
from nio import AsyncClient
from asyncio import sleep
import os

import sync

# Server
host = "127.0.0.1"
port = "5505"
scheme = "http://"

# Bot Creds
bot_name = "@user_name"
bot_pass = "bot_pass"
home_server = "https://home.server"

docker = os.environ.get('docker', False)
if docker:
    host = os.environ.get('host', False)
    port = os.environ.get('port', False)
    bot_name = os.environ.get('botuser', False)
    bot_pass = os.environ.get('botpass', False)
    home_server = os.environ.get('homeserver', False)

url = f"{scheme}{host}:{port}"


async def main():
    docker = os.environ.get('docker', False)
    if docker:
        sync_interval = os.environ.get('sync_interval', False)
    else:
        sync_interval = 5

    client = AsyncClient(f"{home_server}", f"{bot_name}")
    print(await client.login(f"{bot_pass}"))

    while True:
        await sync.sync(url, client)
        await sleep(int(sync_interval))


try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("Exited")
