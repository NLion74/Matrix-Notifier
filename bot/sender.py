import os
import json
from dataclasses import dataclass


@dataclass
class Message:
    id: int
    title: str
    content: str


async def send(msg, client):
    if not os.path.exists("./saved"):
        os.mkdir("./saved")

    if os.path.exists("./saved/roomids.json"):
        with open("./saved/roomids.json", "r") as f:
            roomids = json.load(f)
            f.close()
    else:
        roomids = []

    msg = Message(id=msg[0], title=msg[1], content=msg[2])
    for roomid in roomids:
        await client.room_send(room_id=roomid, message_type="m.room.message", content={"msgtype": "m.text", "body": f"{msg.content}"})
        print(f"Message sent")