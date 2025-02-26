import socket
import pickle

class Network:
    """Handles client-side connection with the server."""
    
    def __init__(self):
        # Connection setup
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = ""
        self.port = 5050
        self.addr = ()
        self.p = None

    def getP(self):
        """Return player ID."""
        return self.p

    def connect(self):
        """Connect to the server and receive initial data."""
        try:
            self.client.connect(self.addr)
            return pickle.loads(self.client.recv(2048 * 16))
        except Exception as e:
            print("Can't connect to server:", e)
            return None

    def send(self, data):
        """Send data to the server and receive a response."""
        try:
            self.client.send(str.encode(data))
            return pickle.loads(self.client.recv(2048 * 16))
        except Exception as e:
            print("Error sending data:", e)
            return None
    
    def set_ip(self, HostIP):
        """Set server IP and attempt to connect."""
        if HostIP == "Host":
            self.server = socket.gethostbyname(socket.gethostname())
        else:
            self.server = HostIP
        
        self.addr = (self.server, self.port)
        self.p = self.connect()
        return self.server
