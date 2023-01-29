import os
from dataclasses import dataclass


@dataclass
class Message:
    id: int
    title: str
    content: str


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
    docker = os.environ.get('docker', False)
    if docker:
        roomid = os.environ.get('roomid', False)
    else:
        if not os.path.exists("./saved"):
            os.mkdir("./saved")
        if os.path.exists("./saved/roomid.txt"):
            with open("./saved/roomid.txt", "r") as f:
                roomid = f.read()
                f.close()
        else:
            roomid = ""

    msg = Message(id=msg[0], title=decode(msg[1]), content=decode(msg[2]))
    await client.room_send(room_id=roomid, message_type="m.room.message", content={"msgtype": "m.text", "body": f"{msg.content}"})
    print(f"Message sent")
