# EncryptedWebsocketChat

## Installation
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
Server will be running on localhost:1234

Run client.py

```bash
python client.py
```

After two clients connected, all messages will become encrypted

## TODO:

### Ability to disconnect without lost of handshake
