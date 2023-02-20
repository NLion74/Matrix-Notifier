import logging
from markdown import markdown
import emoji
import json

from nio import (RoomSendResponse,
                 ErrorResponse,)

logger = logging.getLogger(__name__)


async def fetch_content(msg, tags, markdown_enabled):
    if tags:
        emojis = await convert_emojis(tags)
        if markdown_enabled and not msg['Title'] == "":
            content = {"msgtype": "m.text",
                       "body": f"{emojis}{msg['Title']}:\n{msg['Content']}",
                       "format": "org.matrix.custom.html",
                       "formatted_body": f"{emojis}{msg['Title']}:\n{markdown(msg['Content'], extensions=['nl2br'])}"}
        elif markdown_enabled:
            content = {"msgtype": "m.text",
                       "body": f"{emojis}:\n{msg['Content']}",
                       "format": "org.matrix.custom.html",
                       "formatted_body": f"{emojis}:\n{markdown(msg['Content'], extensions=['nl2br'])}"}
        elif not msg['Title'] == "":
            content = {"msgtype": "m.text",
                       "body": f"{emojis}{msg['Title']}:\n{msg['Content']}"}
        else:
            content = {"msgtype": "m.text",
                       "body": f"{emojis}:\n{msg['Content']}"}

    else:
        if markdown_enabled and not msg['Title'] == "":
            content = {"msgtype": "m.text",
                       "body": f"{msg['Title']}:\n{msg['Content']}",
                       "format": "org.matrix.custom.html",
                       "formatted_body": f"{msg['Title']}:\n{markdown(msg['Content'], extensions=['nl2br'])}"}
        elif markdown_enabled:
            content = {"msgtype": "m.text",
                       "body": f"{msg['Content']}",
                       "format": "org.matrix.custom.html",
                       "formatted_body": markdown(msg['Content'], extensions=['nl2br'])}
        elif not msg['Title'] == "":
            content = {"msgtype": "m.text",
                       "body": f"{msg['Title']}:\n{msg['Content']}"}
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
    roomids = msg['Channels']
    roomids = json.loads(roomids)
    tags = json.loads(msg['Tags'])

    if str(msg['Markdown']) == "true":
        markdown_enabled = True
    else:
        markdown_enabled = False

    content = await fetch_content(msg=msg, tags=tags, markdown_enabled=markdown_enabled)

    if not roomids:
        logger.info("No Channel Id provided")
    else:
        for room in roomids:
            try:
                res = await client.room_send(room_id=room,
                                       message_type="m.room.message",
                                       content=content,
                                       ignore_unverified_devices=True,)

                if isinstance(res, ErrorResponse):
                    raise Exception(res)
                logger.info(f"Message sent")
            except Exception as err:
                logger.error(err)
