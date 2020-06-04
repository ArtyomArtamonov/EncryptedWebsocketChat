# EncryptedWebsocketChat

## What is this?
This is a simple python client and server, that allows 2 clients to send messages to each other using [WebSocket protocol](https://en.wikipedia.org/wiki/WebSocket). 
Every message is encrypted using [RSA cryptosystem](https://en.wikipedia.org/wiki/RSA_(cryptosystem))

## Requirements
You will need some libraries to successfuly run application

For client.py:
```bash
pip install websocket-client
pip install clint
pip install rsa
```
For server.py:
```bash
pip install websockets
pip install asyncio
```

## Usage

Run server.py

```bash
python server.py
```

Run client.py

```bash
python client.py
```

After two clients connected, all messages will become encrypted

## TODO:

- Better UI
