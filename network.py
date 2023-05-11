import socket
import pickle

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "172.30.48.1"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.player_data = self.connect()
        print("Network successfully built")

    def getPlayerData(self):
        return self.player_data

    def connect(self):
        try:
            self.client.connect(self.addr)
            # reply get its data from server file function threaded_client
            # containing the player data itself from one client
            return pickle.loads(self.client.recv(2048))
        except:
            pass

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            receive = self.client.recv(2048)
            reply = pickle.loads(receive)
            return reply
        except socket.error as e:
            pass
            # print(e)
