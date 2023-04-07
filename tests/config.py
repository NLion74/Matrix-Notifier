import os

server_url = "http://127.0.0.1:5505"

auth_secret = ""

channel = ""

database_dir = "/data"


# Do Not Touch
# If docker is used it will use the environment values
docker = os.environ.get('docker', False)
if docker:
    database_dir = "/data"
    server_url = f"http://{os.environ.get('SERVER_HOSTNAME', False)}:{os.environ.get('SERVER_PORT', False)}"
    auth_secret = os.environ.get('auth_secret', False)
    channel = os.environ.get('channel', False)
