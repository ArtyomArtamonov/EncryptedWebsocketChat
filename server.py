import websockets
import asyncio
import copy
import json

from modules.formats import Message


class Server:
    clients = set()

    async def register(self, websocket):
        if len(self.clients) >= 2:
            await websocket.send('Clients limit is 2 per server. You will not receive any messages')
            return
        self.clients.add(websocket)
        pass

    async def unregister(self, websocket):
        print('Client disconnected')
        self.clients.remove(websocket)
        message = json.dumps(vars(Message('System', 1)))
        await self.send_to_clients(message=message)

    async def send_to_clients(self, message, websocket=None):
        if self.clients:
            new_clients = copy.copy(self.clients)
            if websocket is not None:
                new_clients.remove(websocket)
            print(message)
            try:
                await asyncio.wait([client.send(message) for client in new_clients])
            except:
                pass

    async def handler(self, websocket, path):
        print('New client')
        await self.register(websocket)
        try:
            await self.distribute(websocket)
        finally:
            await self.unregister(websocket)

    async def distribute(self, websocket):
        async for message in websocket:
            await self.send_to_clients(message, websocket)


if __name__ == '__main__':
    address = input('Enter IP address: ')
    port = input('port: ')
    server = Server()
    start_server = websockets.serve(server.handler, address, int(port))
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
