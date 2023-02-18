import json
import logging
from markdown import markdown

logger = logging.getLogger(__name__)


async def send(msg, client):
    roomids = msg['Channels']
    roomids = json.loads(roomids)

    if str(msg['Markdown']) == "true":
        markdown_enabled = True
    else:
        markdown_enabled = False

    if markdown_enabled:
        if not msg['Title'] == "":
            content = {"msgtype": "m.text",
                       "body": f"{msg['Title']}\n{msg['Content']}",
                       "format": "org.matrix.custom.html",
                       "formatted_body": markdown(f"{msg['Title']}:\n{msg['Content']}", extensions=['nl2br'])}
        else:
            content = {"msgtype": "m.text",
                       "body": f"{msg['Content']}",
                       "format": "org.matrix.custom.html",
                       "formatted_body": markdown(msg['Content'], extensions=['nl2br'])}
    else:
        if not msg['Title'] == "":
            content = {"msgtype": "m.text",
                       "body": f"{msg['Title']}:\n{msg['Content']}"}
        else:
            content = {"msgtype": "m.text",
                       "body": f"{msg['Content']}"}

    if not roomids:
        logger.info("No Channel Id provided")
    else:
        for room in roomids:
            await client.room_send(room_id=room,
                                   message_type="m.room.message",
                                   content=content)
            logger.info(f"Message sent")
