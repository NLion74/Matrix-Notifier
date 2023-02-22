from nio import (AsyncClient,
                 AsyncClientConfig,
                 LoginResponse,
                 JoinedMembersError,
                 JoinedMembersResponse,)
from aiohttp import (ClientConnectionError,
                     ServerDisconnectedError)
from asyncio import sleep
import os
import json
import logging

import config as configfile

logger = logging.getLogger()

data_dir = configfile.datadir_bot
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


async def login() -> AsyncClient:
    bot_name = configfile.bot_name
    bot_pass = configfile.bot_pass
    home_server = configfile.home_server
    device_name = configfile.device_name

    bot_config = AsyncClientConfig(
        store_sync_tokens=True,
        #encryption_enabled=True,
    )

    if not os.path.exists(config_file):

        if not (home_server.startswith("https://") or home_server.startswith("http://")):
            home_server = "https://" + home_server

        if not os.path.exists(store_path):
            os.mkdir(store_path)

        client = AsyncClient(
            homeserver=home_server,
            user=bot_name,
            store_path=store_path,
            config=bot_config,
        )

        resp = await client.login(password=bot_pass, device_name=device_name)

        if isinstance(resp, LoginResponse):
            await write_details_to_disk(resp, home_server)
            message = "Logged in via password."
        else:
            logger.error(f'homeserver = "{home_server}"; user = "{bot_name}"')
            logger.error(f"Failed to log in: {resp}")
            logger.error(f"Trying to register...")

            resp = await client.register(username=bot_name, password=bot_pass, device_name=device_name)
            message = "Registered using specified credentials."

            if not isinstance(resp, LoginResponse):
                logger.critical(f'homeserver = "{home_server}"; user = "{bot_name}"')
                logger.critical(f"Failed to register: {resp}")
                quit(1)

        logger.info(message)

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
        logger.info("Logged in via access token")

    return client


async def sync_forever(client: AsyncClient, timeout, full_state):
    while True:
        try:
            logger.info("Resyncing with matrix")
            for room_id in client.rooms.keys():
                members = await client.joined_members(room_id=room_id)
                if len(members.members) < 2:
                    await client.room_leave(room_id)
            await client.sync(timeout=timeout, full_state=full_state,)
        except (ClientConnectionError, ServerDisconnectedError):
            logger.warning("Unable to connect to homeserver, retrying in 15s...")
            await sleep(15)
        finally:
            await client.close()
