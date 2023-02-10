import os

# Set this to wherever the bot will be able to access the server
# Example: You have a server running the matrix-notifier-bot with the ip 1.2.3.4 and the port set to 5505.
# If the matrix-notifier-server is running on the same server as the bot it will be able to reach the
# matrix-notifier-server on http://127.0.0.1:5505, but if it's running on a different server it won't be able to
# reach the matrix-notifier-server on localhost therefore you will have to set the server_url to http://1.2.3.4:5505
server_url = "http://127.0.0.1:5505"

# Bot Creds
bot_name = ''
bot_pass = ''
home_server = ''
device_name = 'matrix-nio'

# How many often the bot sync's with the server in seconds
sync_interval = 5

# Where data will persist for the bot
datadir_bot = "./data"

authorization = False
auth_secret = ""


# Do Not Touch
# If docker is used it will use the environment values
docker = os.environ.get('docker', False)
if docker:
    server_url = f"http://{os.environ.get('host', False)}:{os.environ.get('port', False)}"
    bot_name = os.environ.get('botuser', False)
    bot_pass = os.environ.get('botpass', False)
    home_server = os.environ.get('homeserver', False)
    device_name = os.environ.get('devicename', False)
    sync_interval = os.environ.get('sync_interval', False)
    datadir_bot = "/data"
    authorization = os.environ.get('authorization', False)
    auth_secret = os.environ.get('auth_secret', False)