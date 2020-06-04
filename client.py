import websocket, ssl
import _thread as thread
from clint.textui import colored, puts
from modules.encryption import Encrypter


class Client:
    aliases = {
        'kazakh': 'ws://93.100.235.43:1234',
    }

    def settings_message(self, message): # Settings messages handler
        if message.find('key&') != -1 and self.crypto.partner_public is None:
            self.crypto.save_partner_public(message[message.find('&') + 1:])
            self.ws.send('key&' + str(self.crypto.my_public.n))
            puts(colored.magenta('All messages are now encrypted!'))

    def on_message(self, message):
        try:
            message = self.crypto.decrypt(message)
        except:
            pass
        colon = message.find(':')
        amper = message.find('&')
        if amper != -1:
            self.settings_message(message)
            return
        if colon != -1:
            puts(colored.cyan(message[:colon]) + message[colon:])
        else:
            print(message)

    def on_error(self, ws, error):
        print(error)

    def on_close(self, ws):
        print("### closed ###")

    def on_open(self):
        self.crypto = Encrypter()
        self.ws.send('key&' + str(self.crypto.my_public.n))
        thread.start_new_thread(self.chatting, ())

    def send(self, message):
        try:
            message = self.crypto.encrypt(message)
        except:
            self.send(message[:int(len(message)/2)])
            self.send(message[int(len(message)/2):])
            return
        self.ws.send(message)

    def chatting(self): # Function to input text
        while True:
            message = input()
            self.send(self.name + ': ' + message)

    def main(self): # Main function
        self.DEBUG = False
        if not self.DEBUG:
            puts(colored.red('aliases: ') + self.aliases)
            address = input('Server IP address in format {0.0.0.0:1234} or alias {kazakh}: ')
            if self.aliases[address] is not None:
                address = self.aliases[address]
            else:
                address = ('ws://' + address) if address.find('ws://') == -1 else address
            self.name = input('Your name: ')
        else:
            address = 'ws://localhost:1234'
            self.name = 'User'
        self.ws = websocket.WebSocketApp(address,
                                         on_message=self.on_message,
                                         on_error=self.on_error,
                                         on_close=self.on_close)
        self.ws.on_open = self.on_open
        self.ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})


Client().main() # Start client
