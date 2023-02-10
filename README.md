# Matrix-Notifier
A Matrix Bot inspired by gotify and ntfy though it has way less features.

Currently it supports titles and content server side but the bot is only using the content and just ignoring the title.

Currently this bot does not support room accepting meaning that you'll have to manually log into the bot and accept the room you wanna send your messages to.

## Setup

The easiest way of installing would be to use docker, however if for any reason that is not an option you can also install it from source.

Before starting you may wanna create a bot account on the homeserver of your liking.

If you're ever having trouble with the database just use the example-database.db provided.

### Requirements

If youre using the docker-compose.yml you will need to have docker and docker-compose as well as curl installed, and when using the dev-docker-compose.yml you will also need git. building from source you will need python3 matrix-nio and requests installed.

Building from source is not recommended however if you decide to do so anyways you will need python3, matrix-nio and requests installed.

### Install with Docker

There are two docker-compose.yml files provided, the docker-compose.yml and the dev-docker-compose.yml. The docker-compose.yml is whats recommended and also the most stable, using the image from dockerhub and the other one building from the git repository.

If you're using the default docker-compose follow the instructions below:
```
# Create a directory for your docker-compose and move into it
mkdir ./matrix-notifier && cd ./matrix-notifier

# Clone the docker-compose.yml and example.env
curl -O https://raw.githubusercontent.com/NLion74/Matrix-Notifier/main/docker/docker-compose.yml
curl -O https://raw.githubusercontent.com/NLion74/Matrix-Notifier/main/docker/example.env

# Copy the example.env to .env
cp example.env .env

# Customize the .env file and when youre done start the docker-compose
docker-compose up -d
```

If you're using the dev docker-compose follow these instructions below:
```
# Clone the repository
git clone https://github.com/NLion74/Matrix-Notifier

# Move into the repository's docker folder
cd ./Matrix-Notifier/docker

# Copy the example.env to .env
cp example.env .env

# Customize the .env file and when youre done start the docker-compose
docker-compose up -d
```

Now everything should be up and running and you can now.

### Install from source

Building from source is not recommended but if you decide to do so anyways heres a guide.

To configure, edit the server/config.py and the bot/config.py. Important values to set before starting are The Bot Creds bot/config.py.

Afterwards just start the server/app.py and bot/main.py.

## Usage

The Syntax is inspired by ntfy as you may notice if you've ever used ntfy before.

Use ```curl -H "Channel: [Room_Id]" -d "[Message_Body]" [host]:[port]``` to send a message. It is required to use the channel header as you need to provide the server with a room_id to send the message to.

Here's a list of headers together with their provided aliases and a description of what these headers are used for:
```
# Required for sending messages. Used to tell the server which room ids to send messages to. Can be used repeatedly.
X-Channel(Case Sensitive) - Channel(Case Insensitive), c(Case Insensitive)

# Sets the title of the message. Cannot be used repeatedly
X-Title(Case Sensitive) - Title(Case Insensitive), t(Case Insensitive)

# Used for api authentication
X-Authorization(Case Sensitive) - Authorization(Case Insensitive), auth(Case Insensitive)
```

### Disclamer

Note that if you're room id contains a "," the server will break. I don't know if room ids with "," in them exist but if they do this will be an issue that you should be aware of.

## Contact
If there are any questions regarding this project, feel free to contact me over any platform listed on https://nlion.nl/.
