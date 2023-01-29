# Matrix-Notifier
A Matrix Bot inspired by gotify and ntfy though it has way less features.

Currently it supports titles and content server side but the bot is only using the content and just ignoring the title.

## Setup

The easiest way of installing would be to use docker, however if for any reason that is not an option you can also install it from source.

Before starting you may wanna create a bot account on the homeserver of your liking.

### Install with Docker

Make sure you have docker.io, docker-compose and git installed, before continuing.

First of all you should clone the repository using git like this: ```git clone https://github.com/NLion74/Matrix-Notifier```.

Afterwards move into the docker directory and copy the example.env to .env, where you should adjust the roomid as well setting up the botcreds. These being the values: botuser, botpass and homeserver. 

When you're done adjusting the environment variables to your liking, you may wanna start the docker-compose by running ```docker-compose up -d```.

#### Disclaimer

When deleting the messages.db database of the server you will have to also delete ids.json. Otherwise the bot will not send messages where the id is saved within the ids.json file.

### Install from source

To start just change the host and port in server/main.py to which the websocket will bind.

The bot consists of two core components, these being the bot and the server.
To setup the server just change the host and port to your liking. After that just start the main.py in the server directory and you should be good to go.

To setup the bot you'll have to create a file called roomid.txt in the saved folders, it should look just like this:
```
├── bot
│   ├── saved
│   │   └── roomid.txt
│   ├── Dockerfile
│   ├── main.py
│   ├── sender.py
│   └── sync.py
├── docker
│   ├── docker-compose.yml
│   └── example.env
├── server
│   ├── Dockerfile
│   ├── main.py
│   ├── parser.py
│   ├── responder.py
│   ├── saver.py
│   └── server.py
├── LICENSE
└── README.md
```

If you ran either the server or bot before this, there may be additional files but don't let that confuse you. After that you should put the room id of the room you want messages getting sent to in the text file raw, so it looks like this:
```[some_random_id]:[your.home.server]```.

Afterwards just change the host, port and scheme to wherever the server is reachable, as well as changing the Bot Creds to your the ones of your bot and you should be good to start the main.py of the bot. 

#### Disclaimer

When deleting the Database of the server you will have to also delete ids.json in the bot/saved folder. Otherwise the bot will not send messages where the id is saved within the ids.json file.

Also you should be aware that the server only stores the last 100 messages sent to it. If you wanna increase that number edit the saver.py and change the SQL LIMIT on line 41.

## General Information

The bot and server are to completely independent components meaning that you could theoretically take the server and create another client for it, like on discord. You can request all messages from the server using a GET request. It will return them in a JSON Array.

## Usage

The Syntax is inspired by ntfy as you may notice if you've ever used ntfy before.

Use ```curl -d "[Message_Body]" [host]:[port]``` to send a message.

You can also add title like this ```curl -H "Title: [Title_Body]" -d "[Message_Body]" [host]:[port]```.

There are various aliases to set titles including: ```X-Title(Case Sensitive) - Title(Case Insensitive), t(Case Insensitive)```.

## Contact
If there are any questions regarding this project, feel free to contact me over any platform listed on https://nlion.nl/.
