import json


async def send(msg, client):
    roomid = msg['Channels']
    roomid = json.loads(roomid)

    if not roomid:
        print("No Channel Id provided")
    else:
        for room in roomid:
            await client.room_send(room_id=room, message_type="m.room.message", content={"msgtype": "m.text", "body": f"{msg['Content']}"})
            print(f"Message sent")
