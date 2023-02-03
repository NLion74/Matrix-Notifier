import json

import config


def decode(content):
    content = content.replace("\\xf6", "ö")
    content = content.replace("\\xe4", "ä")
    content = content.replace("\\xfc", "ü")
    content = content.replace("\\xdf", "ß")
    content = content.replace("\\xdc", "Ü")
    content = content.replace("\\xd6", "Ö")
    content = content.replace("\\xc4", "Ä")
    content = content.replace("\\x80", "€")
    content = content.replace("\\xa7", "§")
    content = content.replace("\\xa9", "©")

    return content


async def send(msg, client):
    roomid = msg['Channel']
    roomid = json.loads(roomid)

    if not roomid:
        print("No Channel Id provided")
    else:
        for room in roomid:
            await client.room_send(room_id=room, message_type="m.room.message", content={"msgtype": "m.text", "body": f"{decode(msg['Content'])}"})
            print(f"Message sent")
