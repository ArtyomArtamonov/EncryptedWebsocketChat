import websocket, ssl
import _thread as thread
from clint.textui import colored, puts
from modules.encryption import Encrypter


class Client:
    def settings_message(self, message):
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
        if colon == -1:
            self.settings_message(message)
            return
        puts(colored.cyan(message[:colon]) + message[colon:])

    def on_error(self, ws, error):
        print(error)

    def on_close(self, ws):
        print("### closed ###")

    def on_open(self):
        self.crypto = Encrypter()
        self.ws.send('key&' + str(self.crypto.my_public.n))
        thread.start_new_thread(self.chatting, ())

    def chatting(self):
        while True:
            message = input()
            try:
                message = self.crypto.encrypt(self.name + ": " + message)
            except:
                self.ws.send('UNENCRYPTED: ' + self.name + ": " + message)
                continue
            self.ws.send(message)

    def main(self):
        self.name = input('Your name: ')
        self.ws = websocket.WebSocketApp("ws://localhost:1234/",
                                         on_message=self.on_message,
                                         on_error=self.on_error,
                                         on_close=self.on_close)
        self.ws.on_open = self.on_open
        self.ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})


Client().main()