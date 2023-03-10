import logging
from markdown import markdown
import emoji
import json

from nio import (RoomSendResponse,
                 ErrorResponse,)

logger = logging.getLogger(__name__)


async def fetch_content(msg, markdown_enabled):
    if msg['Tags'] or msg['Title'] != "":
        emojis = await convert_emojis(msg['Tags'])
        if markdown_enabled:
            content = {"msgtype": "m.text",
                       "body": f"{emojis}{msg['Title']}:\n{msg['Content']}",
                       "format": "org.matrix.custom.html",
                       "formatted_body": f"{emojis}{msg['Title']}:\n{markdown(msg['Content'], extensions=['nl2br'])}"}
        else:
            content = {"msgtype": "m.text",
                       "body": f"{emojis}{msg['Title']}:\n{msg['Content']}"}

    else:
        if markdown_enabled:
            content = {"msgtype": "m.text",
                       "body": f"{msg['Content']}",
                       "format": "org.matrix.custom.html",
                       "formatted_body": f"{markdown(msg['Content'], extensions=['nl2br'])}"}
        else:
            content = {"msgtype": "m.text",
                       "body": f"{msg['Content']}"}

    return content


async def convert_emojis(tags):
    emoji_dict_alias = emoji.get_aliases_unicode_dict()
    emoji_list = []
    for tag in tags:
        if f":{tag}:" in emoji_dict_alias:
            emoji_list.append(emoji.emojize(f":{tag}:", language="alias"))
        else:
            continue
    emojis = ''.join(emoji_list)
    return emojis


async def send(msg, client):
    if str(msg['Markdown']) == "true":
        markdown_enabled = True
    else:
        markdown_enabled = False

    content = await fetch_content(msg=msg, markdown_enabled=markdown_enabled)

    if not msg['Channels']:
        logger.info("No Channel Id provided")
    else:
        for room in msg['Channels']:
            try:
                res = await client.room_send(room_id=room,
                                             message_type="m.room.message",
                                             content=content,
                                             ignore_unverified_devices=True,)
                logger.info(f"Message with id {msg['Id']} has been sent succesfully.")
                if isinstance(res, ErrorResponse):
                    raise Exception(res)
                return True
            except Exception as err:
                logger.exception(err)
                return False
