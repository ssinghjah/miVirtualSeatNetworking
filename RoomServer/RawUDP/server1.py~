import socket
import threading
from time import sleep

HUB_IP = "0.0.0.0"
HUB_DATA_PORT = 49153
APP_RECEIVE_PORT =49148
APP_SEND_PORT = 49147
LOCAL_IP = "0.0.0.0"
Message = "Hello, Server"
BUFFER_SIZE = 65000

def receive(hubSock):
    appSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        data = hubSock.recv(BUFFER_SIZE)
        #print("Received from Hub: " + str(data))
        appSock.sendto(data, (LOCAL_IP, APP_SEND_PORT))

def publish(localIP, appPort, hubSock, hubIP, hubPort):
    appSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    appSock.bind((localIP, appPort))
    while True:
        data = appSock.recv(BUFFER_SIZE)
        hubSock.sendto(data, (hubIP, hubPort))

hubSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
hubSock.sendto(bytes(Message, "utf-8"), (HUB_IP, HUB_DATA_PORT))
threading.Thread(target=publish, args=(LOCAL_IP, APP_RECEIVE_PORT, hubSock, HUB_IP, HUB_DATA_PORT)).start()
threading.Thread(target=receive, args=(hubSock,)).start()


