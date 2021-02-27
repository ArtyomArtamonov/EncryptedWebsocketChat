import sys

class Commands:
    def __init__(self, ws, client):
        self.commands = {
            '/exit': self.exit,
            '/quit': self.exit,
            '/bye': self.exit,
            '/help': self.help,
        }
        self.client = client
        self.ws = ws

    def exit(self, args):
        self.ws.close()
        sys.exit()
        pass

    def help(self, args):
        self.out(str([key for key in self.commands.keys()])) # Print commands list

    def out(self, text):
        print(text)

    def get_args(self, command):
        args = []
        if command.find(' ') == -1:
            return args
        command += '&'
        command = command[command.find(' ') + 1:]
        arg = ''
        for c in command:
            if c == ' ':
                args.append(arg)
                arg = ''
            elif c == '&':
                args.append(arg)
                return args
            else:
                arg += c

    def execute(self, command):
        args = self.get_args(command)
        command = command[:command.find(' ')] if command.find(' ') != -1 else command
        if command in self.commands:
            self.commands[command](args)
        else:
            print('Command not found')
