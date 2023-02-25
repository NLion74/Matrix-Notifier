# Ignore this section
import os
import logging
logger = logging.getLogger(__name__)


# Set this to wherever the bot will be able to access the server
# Example: You have a server running the matrix-notifier-bot with the ip 1.2.3.4 and the port set to 5505.
# If the matrix-notifier-server is running on the same server as the bot it will be able to reach the
# matrix-notifier-server on http://127.0.0.1:5505, but if it's running on a different server it won't be able to
# reach the matrix-notifier-server on localhost therefore you will have to set the server_url to http://1.2.3.4:5505
server_url = "http://127.0.0.1:5505"

# Bot Creds
bot_name=""
bot_pass=""
home_server=""
device_name = 'matrix-nio'

# Where data will persist for the bot
datadir_bot = "./data"

authorization = False
# Cant contain any &'s or +'s
auth_secret = "some_random_string"


# Do Not Touch
# If docker is used it will use the environment values
docker = os.environ.get('docker', False)
if docker:
    server_url = f"http://{os.environ.get('SERVER_HOSTNAME', False)}:{os.environ.get('SERVER_PORT', False)}"
    bot_name = os.environ.get('bot_user', False)
    bot_pass = os.environ.get('bot_pass', False)
    home_server = os.environ.get('home_server', False)
    device_name = os.environ.get('device_name', False)
    datadir_bot = "/data"
    authorization = os.environ.get('authorization', False)
    auth_secret = os.environ.get('auth_secret', False)

if str(authorization).lower() == "true" or authorization == True:
    authorization = True
    if auth_secret.__contains__("&") or auth_secret.__contains__("+"):
        logger.critical("auth_secret contains invalid characters. Following a list with prohibited characters:")
        logger.critical("['&', '+']")
        logger.critical("Please make sure your auth_secret does not contain any of the characters listed above and try again.")
        quit(1)
else:
    authorization = False

if str(bot_name) == "" or str(bot_name) == "" or str(bot_pass) == "" or str(home_server) == "" or not bot_name or not bot_pass or not home_server:
    logger.critical("Missing Bot_Credentials.")
    quit(1)
