# Matrix-Notifier

[![Bot Pulls](https://img.shields.io/docker/pulls/nlion/matrix-notifier-bot?label=bot%20pulls&style=flat-square)](https://hub.docker.com/repository/docker/nlion/matrix-notifier-bot)
[![Server Pulls](https://img.shields.io/docker/pulls/nlion/matrix-notifier-server?label=server%20pulls&style=flat-square)](https://hub.docker.com/repository/docker/nlion/matrix-notifier-server)
[![Version](https://img.shields.io/github/v/tag/NLion74/Matrix-Notifier?label=version&style=flat-square)](https://github.com/NLion74/Matrix-Notifier)

API for sending messages over the [Matrix](https://matrix.org) protocol, built with [matrix-nio](https://github.com/poljar/matrix-nio).

## Features

- Sending messages via POST
- Web UI to send messages
- Webhooks
- Pushing messages as json
- Docker support
- Authentication support
- Sending encrypted messages
- UTF-8 support
- Markdown support for messages
- Tag support to embed emojis in the title by using their short codes
- Title support

## Table of contents
> Note: Matrix-Notifier probably contains a lot of bugs.
> If you encounter a bug, please consider opening an issue.

- [Setup](#setup)
  - [Dependencies](#dependencies)
  - [Docker installation](#installation-via-docker--recommended-)
  - [From source installation](#from-source-installation)
- [Usage](#usage)
  - [Sending messages](#sending-messages)
  - [Options](#options)
  - [Getting messages](#getting-messages-from-the-server)
- [Disclaimer](#disclaimer)
- [Issues](#issues)
- [Contact](#contact)

## Setup
 
The easiest way of installing would be to use docker, however if for any reason that is not an option you can also install it from source.

Before starting, you may want to create a bot account on the homeserver of your liking. Or if your home_server supports registration without email adress and captcha, it will just create an account using the specified credentials. 

If you're ever having trouble with the database just use the example-database.db provided under examples/example-database.

### Dependencies

#### Install via docker

- [Docker](https://www.docker.com/)
- [Docker Compose](https://github.com/docker/compose)

#### Install from source

- [Python3](https://www.python.org/)
- [Python3-pip](https://pypi.org/project/pip/)

### Installation via Docker (recommended)

There are two docker-compose.yml files provided, the docker-compose.yml and the dev-docker-compose.yml. The docker-compose.yml is what's recommended and also the most stable, using the image from dockerhub and the other one building from the git repository.

If you're using the default docker-compose follow the instructions below:

```
# Create a directory for your docker-compose and move into it
mkdir ./matrix-notifier && cd ./matrix-notifier

# Clone the docker-compose.yml and example.env
curl -O https://raw.githubusercontent.com/NLion74/Matrix-Notifier/main/docker/docker-compose.yml
curl -O https://raw.githubusercontent.com/NLion74/Matrix-Notifier/main/docker/example.env

# Copy the example.env to .env
cp example.env .env

# Customize the .env file and when you're done start the docker-compose
docker-compose up -d
```

If you're using the dev-docker-compose follow these instructions below:

```
# Clone the repository
git clone https://github.com/NLion74/Matrix-Notifier

# Move into the repository's docker folder
cd ./Matrix-Notifier/docker

# Copy the example.env to .env
cp example.env .env

# Customize the .env file and when you're done start the docker-compose
docker-compose up -d
```

Now everything should be up and running, and you can now move to the [Usage Section](#Usage).

### From source Installation

```
# Clone the repository
git clone https://github.com/NLion74/Matrix-Notifier

# Move into the repository's server folder
cd ./Matrix-Notifier/server

# Installing the dependencies
pip3 install -r requirements.txt

# Edit the config.py and start the server
python3 app.py

# Move into the repository's bot folder
cd ../bot

# Installing the dependencies
pip3 install -r requirements.txt

# Edit the config.py and start the bot
python3 main.py
```

Now if all the dependencies are installed the server and bot should be up and running. You can now move on to the [Usage Section](#Usage).

## Usage

Before moving on to sending messages you should create a room with the bot in it and copy the room id.

To obtain the room id of a room on [Element](https://element.io/) right-click the room, then click on Settings. The room id can then be found in advanced section under Internal room ID.

### Sending messages

Messages can either be sent via HTTP POST request and by using the Web UI or even via HTTP GET request by using Webhooks.

#### POST

Here's an example showing how you can send messages via POST request:

```
curl \
  -H "Channel: !liLFnvuVbMtrtbOYMS:matrix.org" \
  -H "Title: Server Failure"
  -H "Tags: exclamation, computer"
  -d "Your server went down!" \
  127.0.0.1:5505
```

And on ios with element installed that would result in a notifcation like this:

![notification.png](assets/images/notifications.png)

#### Web UI

Alternatively you could use the Web UI to send messages, which looks like this:

![webui.png](assets/images/webui.png)

After you've seen how to send messages via POST this should be rather self-explanatory.

#### Webhooks

An alternative to using POST would be to send messages via webhook which supports both GET and POST requests.

To use webhooks, simply make a request to the ```/webhook``` route and use queries to provide options just like you would normally.

if you don't specify a message it will default to "webhook triggered".

```
curl "127.0.0.1:5505/webhook?channel=!liLFnvuVbMtrtbOYMS:matrix.org&title=Server+Failure&tags=exclamation,computer&message=Your+server+went+down!"
```

Which would result in a notification like this.

![notification.png](assets/images/notifications.png)

#### Push as json

You can also push messages via json. This feature supports both POST and GET http requests.

To push messages as json, you have to make a request to the ```/json``` the body has to be a json dictionary.

Specifying a message is required.

```
curl 127.0.0.1:5505/json \
  -d '{
    "channel": "!liLFnvuVbMtrtbOYMS:matrix.org",
    "title": "Server Failure",
    "tags": "exclamation, computer",
    "message": "Your server went down!"
  }'
```

This would result in a notification like this:

![notification.png](assets/images/notifications.png)

### Options

In this section we will be going through every single option, explain what they do and how to use them. At the end of the section you'll find a summary of all options.

#### Channel

This option is always required, and is used for the bot to identify the rooms. The value has to be the room id of the room you want your messages getting sent to.

To obtain the room id of a room on [Element](https://element.io/) right-click the room, then click on Settings. The room id can then be found in advanced section under Internal room ID.

#### Authorization

This option is required for authentication if enabled.

```
curl -H "Channel: !liLFnvuVbMtrtbOYMS:matrix.org" -H "Authorization: super_secure_secret" -d "This message requires authentication"
```

![authorization_example.png](assets/images/authorization_example.png)

#### Message title

The title will be a line on top of the message with a ":" at the end of the title.
Setting a title is optional.

```
curl -H "Channel: !liLFnvuVbMtrtbOYMS:matrix.org" -H "X-Title: My amazing title" -d "Titles are just so amazing" 127.0.0.1:5505
curl -H "Channel: !liLFnvuVbMtrtbOYMS:matrix.org" -H "Title: My amazing title" -d "Titles are just so amazing" 127.0.0.1:5505
curl -H "Channel: !liLFnvuVbMtrtbOYMS:matrix.org" -H "t: My amazing title" -d "Titles are just so amazing" 127.0.0.1:5505
```

![title_example.png](assets/images/title_example.png)

#### Message tags

The tags will be a line on top of the message with a ":" at the end of the tags. To send multiple tags just split them with "," between them. With this you could tag specific server to identify them.
Setting tags is optional.

A list of emojis can be found here: https://www.webfx.com/tools/emoji-cheat-sheet/

```
curl -H "Channel: !liLFnvuVbMtrtbOYMS:matrix.org" -H "X-Tags: computer_disk, exclamation" -d "Drive failure detected" 127.0.0.1:5505
curl -H "Channel: !liLFnvuVbMtrtbOYMS:matrix.org" -H "Tags: computer_disk, exclamation" -d "Drive failure detected" 127.0.0.1:5505
curl -H "Channel: !liLFnvuVbMtrtbOYMS:matrix.org" -H "ta: computer_disk, exclamation" -d "Drive failure detected" 127.0.0.1:5505
```

![tags_example.png](assets/images/tags_example.png)

#### Markdown messages

This option enables the use of markdown. Setting markdown is optional. Default is set to false.
Markdown can only be used in the message body not for the headers.

A guide on how to use markdown can be found here: https://www.markdownguide.org/basic-syntax/.

```
curl -H "Channel: !liLFnvuVbMtrtbOYMS:matrix.org" -H "X-Markdown: true" -d "_italic text_" 127.0.0.1:5505
curl -H "Channel: !liLFnvuVbMtrtbOYMS:matrix.org" -H "Markdown: true" -d "_italic text_" 127.0.0.1:5505
curl -H "Channel: !liLFnvuVbMtrtbOYMS:matrix.org" -H "m: true" -d "_italic text_" 127.0.0.1:5505
```

![markdown_example.png](assets/images/markdown_example.png)

#### Markdown messages

This option is used as a query when requesting messages from the server via HTTP GET request.
Default is set to 100.

```
curl 127.0.0.1:5505/messages?limit=250
```

#### List of all options

```
# Required for sending messages. Used to tell the server which room ids to send messages to. Can be used repeatedly.
X-Channel(Case Sensitive) - Channel(Case Insensitive), c(Case Insensitive)

# Used for api authentication. Cannot be used repeatedly.
X-Authorization(Case Sensitive) - Authorization(Case Insensitive), auth(Case Insensitive)

# Sets the title of the message. Cannot be used repeatedly.
X-Title(Case Sensitive) - Title(Case Insensitive), t(Case Insensitive)

# Used to put emojis into the title without actually typing them out.
# Useful if wherever you want to send emojis from doesnt support utf-8.
# Emoji codes can be found here: https://www.webfx.com/tools/emoji-cheat-sheet/
X-Tags(Case Sensitive) - Tags(Case Insensitive), Tag(Case Insensitive), ta(Case Insensitive)

# Used to enable and disable markdown. Default is set to false. Cannot be used repeatedly.
X-Markdown(Case Sensitive) - Markdown(Case Insensitive), m(Case Insensitive)

# Used to manipulate how many messages the server should return when requesting messages via HTTP GET.
X-Limit(Case Sensitive) - Limit(Case Insensitive), l(Case Insensitive)
```

If you need more examples take a look into the examples directory.

### Getting messages from the server

#### GET

If you want to get the messages from the server you can do that via HTTP GET request.

```
curl 127.0.0.1:5505/messages
```

This will return the last 100 messages in json format by default. You can however increase the limit by adding a query like this:

```
curl 127.0.0.1:5505/messages?limit=250
```

You can also reference specific messages by their id.

```
curl 127.0.0.1:5505/messages/10
```

Now if you want to reference multiple messages by their id you can seperate by them with a ",".

```
curl 127.0.0.1:5505/messages/10,12,99
```

if authorization is enabled you will have to also add an authorization query.

### Disclaimer

**This is an experimental project. It could break at any time and should not be considered production ready.**

Note that if your room id contains a "," the server will break. I don't know if room ids with "," in them exist but if they do this will be an issue that you should be aware of.

## Issues

Matrix-Notifier probably contains a lot of bugs. So if you encounter a bug, please consider opening an issue or contacting me directly. For the latter take a look at the [Contact Section](#Contact).

## Contact
If there are any questions regarding this project, feel free to contact me over any platform listed on https://nlion.nl/.
