import socket
import pickle


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.0.8"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.p = self.connect()

    def getP(self):
        return self.p

    def connect(self): #função pra fazer a conexão do player
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode() #retorno decodificado para saber qual player foi conectado
        except:
            pass

    def send(self, data): #função pra enviar dados
        try:
            self.client.send(str.encode(data)) #dado enviado como string
            return pickle.loads(self.client.recv(2048*2)) #retorno feito como objeto
        except socket.error as e:
            print(e)