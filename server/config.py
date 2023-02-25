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


# Do Not Touch
# If docker is used it will use the environment values
docker = os.environ.get('docker', False)
if docker:
    port = os.environ.get('SERVER_PORT', False)
    datadir_server = "/data"
    authorization = os.environ.get('authorization', False)
    auth_secret = os.environ.get('auth_secret', False)

if str(authorization).lower() == "true" or authorization == True:
    authorization = True
    if auth_secret.__contains__("&") or auth_secret.__contains__("+"):
        logger.error("auth_secret contains invalid character")
        quit(1)
else:
    authorization = False
