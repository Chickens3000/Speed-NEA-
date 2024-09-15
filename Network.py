import socket
import pickle


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = ""
        self.port = 5050
        self.addr = ()
        self.p = None

    def getP(self):
        return self.p

    def connect(self):
        try:
            print(self.addr)
            print(type(self.addr[0]))
            self.client.connect(self.addr)
            return pickle.loads(self.client.recv(2048*16))
        except Exception as e:
            print("network",e)

    def send(self, data):
        self.client.send(str.encode(data))
        return pickle.loads(self.client.recv(2048*16))
    
    def set_ip(self,HostIP):
        if HostIP == "Host":
            self.server =  socket.gethostbyname(socket.gethostname())
        else:
            self.server = HostIP
        self.addr = (self.server, self.port)
        self.p = self.connect()
        return self.server