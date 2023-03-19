# Ignore this section
import os
import logging
logger = logging.getLogger(__name__)


# Port the server will use
port = '5505'

# Where data will persist for the server
datadir_server = "./data"

authorization = False
# Cant contain any &'s or +'s
auth_secret = ""

# How long the server should keep messages in hours
message_preserve_time = 72
# How often the purge job should be run in minutes
message_purge_interval = 30

# Do Not Touch
# If docker is used it will use the environment values
docker = os.environ.get('docker', False)
if docker:
    port = os.environ.get('SERVER_PORT', False)
    datadir_server = "/data"
    authorization = os.environ.get('authorization', False)
    auth_secret = os.environ.get('auth_secret', False)
    message_preserve_time = os.environ.get('message_preserve_time', False)
    message_purge_interval = os.environ.get('message_purge_interval', False)

if str(authorization).lower() == "true" or authorization == True:
    authorization = True
    if auth_secret.__contains__("&") or auth_secret.__contains__("+"):
        logger.error("auth_secret contains invalid character")
        quit(1)
else:
    authorization = False
if not type(message_preserve_time) == type(1):
    try:
        message_preserve = int(message_preserve_time)
    except ValueError:
        logger.error("Wrong message_preserve format")
        quit(1)
if not type(message_purge_interval) == type(1):
    try:
        message_purge_interval = int(message_purge_interval)
    except ValueError:
        logger.error("Wrong message_purge_interval format")
        quit(1)
