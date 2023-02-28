import requests

# This assummes that the server is reachable on localhost with the port 5505
matrix_notifier_url = 'http://127.0.0.1:5505'

# This should be set to the amount of messages that should be returned from the server
limit = 250

try:
    res = requests.get(f"{matrix_notifier_url}?limit={limit}")
    if res.status_code == 401:
        print("The auth_secret seems to be invalid")
    else:
        # This should be a json array of the last however many messages you set in the limit
        print(res.text)
except requests.exceptions.RequestException:
    print("The Server seems to be down")
