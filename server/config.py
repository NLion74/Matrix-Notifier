import os

# Port the server will use
port = '5505'

# Where data will persist for the server
datadir_server = "./data"

authorization = False
auth_secret = ""


# Do Not Touch
# If docker is used it will use the environment values
docker = os.environ.get('docker', False)
if docker:
    port = os.environ.get('port', False)
    datadir_server = "/data"
    authorization = os.environ.get('authorization', False)
    auth_secret = os.environ.get('auth_secret', False)

if str(authorization).lower() == "true" or authorization == True:
    authorization = True
else:
    authorization = False
