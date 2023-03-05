import requests
import json

# This assummes that the server is reachable on localhost with the port 5505
matrix_notifier_url = 'http://127.0.0.1:5505'

# The id of the room where you want your messages to be sent to.
# Note that you'll have to manually accept the room invite. Also Room Encryption is currently not supported.
# To obtain the room id of a room under element, just right-click the room, and then you can find then under Advanced,
# there is the "Internal room ID", just copy that, and you have successfully obtained the room_id and can paste it here.
room_id = "!IuYrvSwpWqfPXsFqJL:nlion.nl"

message = "Test Message"
title = "Test Title"

message_array = {"message": message, "title": title, "channel": room_id}

try:
    res = requests.post(matrix_notifier_url, data=json.dumps(message_array))
    if res.status_code == 401:
        print("The auth_secret seems to be invalid")
except requests.exceptions.RequestException:
    print("The Server seems to be down")