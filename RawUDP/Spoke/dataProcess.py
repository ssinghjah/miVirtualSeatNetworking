import socket
import threading
from time import sleep

HUB_IP = "44.211.205.92"
HUB_DATA_PORT = 49152
APP_PORT =49148
LOCAL_IP = "0.0.0.0"
Message = "Hello, Server"

def receive(sock, ip, port):
    while True:
        data = sock.recv(1024)
        print("Received from Hub: " + data.decode("utf-8"))

def publish(LOCAL_IP, APP_PORT):
    appSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    appSock.bind((LOCAL_IP, APP_PORT))
    while True:
        data = appSock.recv(1024)
        print("Received from App: " + data.decode("utf-8"))

hubSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
hubSock.connect((HUB_IP, HUB_DATA_PORT))
hubSock.sendto(bytes(Message, "utf-8"), (HUB_IP, HUB_DATA_PORT))
threading.Thread(target=publish, args=(LOCAL_IP,APP_PORT)).start()
threading.Thread(target=receive, args=(hubSock, HUB_IP, HUB_DATA_PORT)).start()


