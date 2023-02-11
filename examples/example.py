import requests

# This assummes that the server is reachable on localhost with the port 5505
matrix_notifier_url = 'http://127.0.0.1:5505'

# The id of the room where you want your messages to be sent to.
# Note that you'll have to manually accept the room invite. Also Room Encryption is currently not supported.
# To obtain the room id of a room under element, just right-click the room, and then you can find then under Advanced,
# there is the "Internal room ID", just copy that, and you have successfully obtained the room_id and can paste it here.
room_id = ""

try:
    # You have to encode the data in utf-8 if you're using utf-8
    # It also works without encoding it, but I recommend always encoding it with utf-8 when possible
    res = requests.post(matrix_notifier_url, headers={"Channel": ""}, data="Hello, I am working.".encode("utf-8"))
    if res.status_code == 401:
        print("The auth_secret seems to be invalid")
except requests.exceptions.RequestException:
    print("The Server seems to be down")