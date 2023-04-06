import asyncio
from nio import (InviteMemberEvent,
                 RoomMessageText,
                 MegolmEvent,)
import logging
from time import time

import sync
import config as configfile
from Callbacks import Callbacks
import bot
from exit_handler import Exit
import config

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(message)s',
                    datefmt='%m-%d %H:%M',)

logger = logging.getLogger()

if config.coverage:
    from coverage import Coverage
    coveragedatafile = ".coverage-bot-" + str(int(time()))
    cov = Coverage(data_file=f"{config.datadir_bot}/coverage/{coveragedatafile}")
    cov.erase()
    cov.start()
else:
    cov = ""

exit_handler = Exit(cov)


async def main():
    url = f"{configfile.server_url}/messages"

    client = await bot.login()

    callbacks = Callbacks(client)
    client.add_event_callback(callbacks.invite, (InviteMemberEvent,))
    client.add_event_callback(callbacks.message, (RoomMessageText,))
    client.add_event_callback(callbacks.decryption_failure, (MegolmEvent,))

    await client.sync(full_state=True)

    if client.should_upload_keys:
        await client.keys_upload()

    if client.should_query_keys:
        await client.keys_query()

    if client.should_claim_keys:
        await client.keys_claim()

    f1 = asyncio.get_event_loop().create_task(bot.sync_forever(client=client, timeout=30000, full_state=False,))
    f2 = asyncio.get_event_loop().create_task(sync.sync_forever(url, client))

    await asyncio.wait([f1, f2])


try:
    asyncio.run(main())
except KeyboardInterrupt:
    logger.error("Received keyboard interrupt.")
    quit(0)
