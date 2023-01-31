import asyncio
from nio import AsyncClient, AsyncClientConfig, LoginResponse, InviteMemberEvent
from asyncio import sleep
import os
import json

import sync

docker = os.environ.get('docker', False)
if docker:
    config_file = "/data/credentials.json"
    store_path = "/data/store"
else:
    config_file = "./saved/credentials.json"
    store_path = "./saved/store"


def write_details_to_disk(resp: LoginResponse, home_server) -> None:
    with open(config_file, "w") as f:
        json.dump(
            {
                "home_server": home_server,
                "user_id": resp.user_id,
                "device_id": resp.device_id,
                "access_token": resp.access_token,
            },
            f,
        )


async def login(home_server, bot_name, bot_pass, device_name) -> AsyncClient:
    bot_config = AsyncClientConfig(
        store_sync_tokens=True,
    )

    if not os.path.exists(config_file):

        if not (home_server.startswith("https://") or home_server.startswith("http://")):
            home_server = "https://" + home_server

        if not os.path.exists(store_path):
            os.mkdir(store_path)

        client = AsyncClient(
            home_server,
            bot_name,
            store_path=store_path,
            config=bot_config,
        )

        resp = await client.login(password=bot_pass, device_name=device_name)

        if isinstance(resp, LoginResponse):
            write_details_to_disk(resp, home_server)
        else:
            print(f'homeserver = "{home_server}"; user = "{bot_name}"')
            print(f"Failed to log in: {resp}")
            quit(1)

        print("Logged in via password")

    else:
        with open(config_file, "r") as f:
            config = json.load(f)
            client = AsyncClient(
                config["home_server"],
                config["user_id"],
                device_id=config["device_id"],
                store_path=store_path,
                config=bot_config,
            )

            client.restore_login(
                user_id=config["user_id"],
                device_id=config["device_id"],
                access_token=config["access_token"],
            )
        print("Logged in via access token")

        if client.should_upload_keys:
            await client.keys_upload()

    return client


async def main():
    # Server
    host = "127.0.0.1"
    port = "5505"
    scheme = "http://"

    # Bot Creds
    bot_name = "@bot_user:home.server"
    bot_pass = "bot_pass"
    home_server = "https://home.server"
    device_name = "matrix-nio"

    docker = os.environ.get('docker', False)
    if docker:
        host = os.environ.get('host', False)
        port = os.environ.get('port', False)
        bot_name = os.environ.get('botuser', False)
        bot_pass = os.environ.get('botpass', False)
        home_server = os.environ.get('homeserver', False)
        device_name = os.environ.get('devicename', False)

    url = f"{scheme}{host}:{port}"

    docker = os.environ.get('docker', False)
    if docker:
        sync_interval = os.environ.get('sync_interval', False)
    else:
        sync_interval = 5

    client = await login(home_server, bot_name, bot_pass, device_name)

    while True:
        await sync.sync(url, client)
        await sleep(int(sync_interval))


try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("Received keyboard interrupt.")
    quit(0)
