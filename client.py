import _thread as thread
import json

import ssl
import websocket
from clint.textui import colored, puts

from modules.commands import Commands
from modules.encryption import Encrypter
from modules.formats import Message

DEBUG = False


class Client:
    def __init__(self):
        self.crypto = Encrypter()
        self.current_messages = []

    def handshake(self, key):
        if self.crypto.partner_public is None:
            self.crypto.save_partner_public(key)
            handshake = json.dumps(vars(Message('Handshake', self.crypto.my_public.n)))
            self.send(handshake, False)
            puts(colored.magenta('Partner has been connected. All messages are now encrypted!'))

    def commands(self, command):
        self.command_handler.execute(command)

    def put_user_message(self, message):
        name = message['data']['Name']
        message = message['data']['Message']
        puts(colored.cyan(name + ': ') + message)

    def message_handler(self, message):
        if 'type' in message and message['type'] == 'Handshake':
            self.handshake(message['data'])
        elif 'type' in message and message['type'] == 'Message':
            self.put_user_message(message)
        elif 'type' in message and message['type'] == 'System':
            data = message['data']
            if data == 1:  # 'Partner has disconnected' message from server
                self.crypto.partner_public = None
                puts(colored.magenta('Partner has disconnected. All messages are now unencrypted!'))

    def on_message(self, message_part):
        try:
            self.current_messages.append(self.crypto.decrypt(message_part))
            message = ''
            for m in self.current_messages:
                message += m
            message = json.loads(message)
            self.message_handler(message)
            self.current_messages = []
        except Exception as e:
            pass

    def on_error(self, ws, error):
        print(error)

    def on_close(self, ws):
        print("### closed ###")

    def on_open(self):
        puts(colored.green('Connection established, ') +
             colored.red('but messages are not encrypted yet.'))
        puts(colored.yellow('Use /help for command list. /exit to leave server'))
        handshake = json.dumps(vars(Message('Handshake', self.crypto.my_public.n)))
        self.send(handshake, False)
        thread.start_new_thread(self.chatting, ())

    def send(self, message, encrypted=True):
        if self.crypto.partner_public is not None and encrypted is True:
            try:
                message = self.crypto.encrypt(message)
            except:
                self.send(message[:int(len(message) / 2)])
                self.send(message[int(len(message) / 2):])
                return
            self.ws.send(message)
        else:
            self.ws.send(message)  # Unencrypted

    def chatting(self):  # Function to input text
        while True:
            message = input()
            if message[0] == '/':  # Call the commands func if message contains '/'
                self.commands(message)
                continue
            message = Message('Message', {'Name': self.name, 'Message': message})
            self.send(json.dumps(vars(message)))

    def main(self):  # Main function
        if not DEBUG:
            address = input('Server IP address in format {0.0.0.0:1234}: ')
            address = ('ws://' + address) if address.find('ws://') == -1 else address
            self.name = input('Your name: ')
        else:
            address = 'ws://localhost:1234'
            self.name = 'User'
        self.ws = websocket.WebSocketApp(address,
                                         on_message=self.on_message,
                                         on_error=self.on_error,
                                         on_close=self.on_close)
        self.command_handler = Commands(self.ws, self)
        self.ws.on_open = self.on_open
        self.ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})


if __name__ == '__main__':
    Client().main()  # Start client
