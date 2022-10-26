import socket
import threading
from time import sleep

HUB_IP = "44.211.205.92"
HUB_DATA_PORT = 49152
APP_PORT =49148
LOCAL_IP = "0.0.0.0"
Message = "Hello, Server"
BUFFER_SIZE = 65000

def receive(sock, ip, port):
    while True:
        data = sock.recv(BUFFER_SIZE)
        print("Received from Hub: " + data.decode("utf-8"))

def publish(localIP, appPort, hubSock, hubIP, hubPort):
    appSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    appSock.bind((localIP, appPort))
    while True:
        data = appSock.recv(BUFFER_SIZE)
        #print("Received from App: " + data.decode("utf-8"))
        hubSock.sendto(data, (hubIP, hubPort))

hubSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
hubSock.sendto(bytes(Message, "utf-8"), (HUB_IP, HUB_DATA_PORT))
threading.Thread(target=publish, args=(LOCAL_IP, APP_PORT, hubSock, HUB_IP, HUB_DATA_PORT)).start()
threading.Thread(target=receive, args=(hubSock, HUB_IP, HUB_DATA_PORT)).start()


