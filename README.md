# Matrix-Notifier
A Matrix Bot inspired by gotify and ntfy though it has way less features.

Currently it supports titles and content server side but the bot is only using the content and just ignoring the title.

## Setup

To start just change the host and port in server/main.py to which the websocket will bind

The bot consists of two core components, these being the bot and the server.
To setup the server just change the host and port to your liking. After that just start the main.py in the server directory and you should be good to go

To setup the bot you'll have to create a file called roomids.json in the saved folders, it should look just like this:
```
├── bot
│   ├── saved
│   │   └── roomids.json
│   ├── main.py
│   ├── sender.py
│   └── sync.py
├── server
│   ├── main.py
│   ├── parser.py
│   ├── responder.py
│   ├── saver.py
│   └── server.py
├── LICENSE
└── README.md
```

If you ran either the server or bot before this, there may be additional files but don't let that confuse you. After that you should put the room ids of the rooms you want messages getting sent to in a JSON Array. It should look like this. ```["room_id_here", "room_id_here"]```

Afterwards just change the host, port and scheme to wherever the server is reachable, as well as changing the Bot Creds to your the ones of your bot and you should be good to start the main.py of the bot.

### Disclaimer

When deleting the Database of the server you will have to also delete ids.json in the bot/saved folder. Otherwise the bot will not send messages where the id is saved within the ids.json file.

## Usage

The Syntax is inspired by ntfy as you may notice if you've ever used ntfy before.

Use ```curl -d "[Message_Body]" [host]:[port]``` to send a message.

You can also add title like this ```curl -H "Title: [Title_Body]" -d "[Message_Body]" [host]:[port]```

There are various aliases to set titles including: ```X-Title(Case Sensitive) - Title(Case Insensitive), t(Case Insensitive)```
