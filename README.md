# Matrix-Notifier
A Matrix Bot inspired by gotify and ntfy though it has way less features.

Currently it supports titles and content server side but the bot is only using the content and just ignoring the title.

## Setup

The easiest way of installing would be to use docker, however if for any reason that is not an option you can also install it from source.

Before starting you may wanna create a bot account on the homeserver of your liking.

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

Afterwards move into the docker directory and copy the example.env to .env, where you should adjust the roomid as well setting up the botcreds. These being the values: botuser, botpass and homeserver. 

When you're done adjusting the environment variables to your liking, you may wanna start the docker-compose by running ```docker-compose up -d```.

#### Disclaimer

When deleting the messages.db database of the server you will have to also delete ids.json. Otherwise the bot will not send messages where the id is saved within the ids.json file.

### Install from source

Building from source is not recommended but if you decide to do so anyways heres a guide.

To configure, edit the server/config.py and the bot/config.py. Important values to set before starting are The Bot Creds and room_id in bot/config.py.

Afterwards just start the server/main.py and bot/main.py.

#### Disclaimer

When deleting the Database of the server you will have to also delete ids.json in the bot/saved folder. Otherwise the bot will not send messages where the id is saved within the ids.json file.

## General Information

The bot and server are to completely independent components meaning that you could theoretically take the server and create another client for it, like on discord. You can request all messages from the server using a GET request. It will return them in a JSON Array.

## Usage

The Syntax is inspired by ntfy as you may notice if you've ever used ntfy before.

Use ```curl -d "[Message_Body]" [host]:[port]``` to send a message.

You can also add title like this ```curl -H "Title: [Title_Body]" -d "[Message_Body]" [host]:[port]```.

There are various aliases to set titles including: ```X-Title(Case Sensitive) - Title(Case Insensitive), t(Case Insensitive)```.

## Contact
If there are any questions regarding this project, feel free to contact me over any platform listed on https://nlion.nl/.
