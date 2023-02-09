import os

# Port the server will use
port = '5505'

# How many entries should be kept in the database
limit = 100

# Where data will persist for the server
datadir_server = "./data"


# Do Not Touch
# If docker is used it will use the environment values
docker = os.environ.get('docker', False)
if docker:
    port = os.environ.get('port', False)
    limit = os.environ.get('sqlimit', False)
    datadir_server = "/data"