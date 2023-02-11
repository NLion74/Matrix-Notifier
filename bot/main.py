import asyncio
from nio import AsyncClient, AsyncClientConfig, LoginResponse, InviteMemberEvent, RoomMessageText
from asyncio import sleep
import os
import json

import sync
import config
from Callbacks import Callbacks

data_dir = config.datadir_bot
if not os.path.exists(data_dir):
    os.mkdir(data_dir)
config_file = f"{data_dir}/credentials.json"
store_path = f"{data_dir}/store"


async def write_details_to_disk(resp: LoginResponse, home_server) -> None:
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

        callbacks = Callbacks(client)
        client.add_event_callback(callbacks.invite, (InviteMemberEvent,))
        client.add_event_callback(callbacks.message, (RoomMessageText,))


        resp = await client.login(password=bot_pass, device_name=device_name)

        if isinstance(resp, LoginResponse):
            await write_details_to_disk(resp, home_server)
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

            callbacks = Callbacks(client)
            client.add_event_callback(callbacks.invite, (InviteMemberEvent,))
            client.add_event_callback(callbacks.message, (RoomMessageText,))

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
    # Bot Creds
    bot_name = config.bot_name
    bot_pass = config.bot_pass
    home_server = config.home_server
    device_name = config.device_name

    url = config.server_url

    sync_interval = config.sync_interval

    client = await login(home_server=home_server, bot_name=bot_name, bot_pass=bot_pass, device_name=device_name)

    while True:
        await sync.sync(url, client)
        await client.sync(timeout=30000)
        await sleep(int(sync_interval))


try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("Received keyboard interrupt.")
    quit(0)
