import json
import re
import codecs


def decode(content):
    for match in re.findall(r"\\x[a-f0-9][a-f0-9]", content):
        print(match[2::])
        s = chr(int(match[2::], 16))
        content = content.replace(match, s)

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
