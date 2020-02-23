import socket
from threading import *

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "localhost"
port = 16969
serversocket.bind((host, port))

class client(Thread):
    def __init__(self, socket, address):
        Thread.__init__(self)
        self.sock = socket
        self.addr = address
        self.start()
    def run(self):
        while 1:
            r=input("Send data -->")
            clientsocket.send(r.encode())
            if r == 'bye' or r == 'Bye' :
                serversocket.close()
                break
            ack = clientsocket.recv(1024).decode()
            if ack == 'Acknowledgement: Message Received' :
                print(ack)
            else :
                print("Acknowledgement not yet received")
            

serversocket.listen(5)
print ('Sender ready and is listening')
while (True):
    clientsocket, address = serversocket.accept()
    print("Receiver " + str(address) + " connected")
    client(clientsocket, address)
    