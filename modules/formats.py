class Message:
    def __init__(self, type, data):
        self.type = type
        self.data = data

'''
_____________________________________________________________
| Type |           Message           | System  | Handshake  |
| Data | {'Name':'', 'Message': ''}  |  int    |    int     |
|______|_____________________________|_________|____________|

System: 
1 Partner disconnect
2 ...
'''
