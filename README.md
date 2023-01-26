# Matrix-Notifier
A Matrix Bot inspired by gotify and ntfy though it has way less features

Currently it supports titles and message content

## Setup

To start just change the host and port in server/main.py to which the websocket will bind

## Usage

The Syntax is inspired by ntfy as you may notice if you've ever used ntfy before

Use ```curl -d "[Message_Body]" [host]:[port]``` to send a message.

You can also add title like this ```curl -H "Title: [Title_Body]" -d "[Message_Body]" [host]:[port]```
All aliases for Title are: ```X-Title(Case Sensitive) - Title(Case Insensitive), t(Case Insensitive)```
