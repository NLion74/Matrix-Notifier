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
print(f"{home_server}", f"{bot_name}", f"{bot_pass}", f"{url}")


async def main():
    client = AsyncClient(f"{home_server}", f"{bot_name}")
    print(await client.login(f"{bot_pass}"))

    while True:
        await sync.sync(url, client)
        await sleep(5)


try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("Exited")
