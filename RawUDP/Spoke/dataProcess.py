import socket
import threading
from time import sleep

HUB_IP = "18.207.212.184"
HUB_DATA_PORT = 49152
Message = "Hello, Server"

def receive(sock, ip, port):
    while True:
        data = sock.recv(1024)
        print("Received from Hub: " + data.decode("utf-8"))

def publish(sock, ip, port):
    while True:
        sleep(2)
        sock.sendto(bytes(Message, "utf-8"), (ip, port))


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.connect((HUB_IP, HUB_DATA_PORT))
sock.sendto(bytes(Message, "utf-8"), (HUB_IP, HUB_DATA_PORT))
threading.Thread(target=publish, args=(sock,HUB_IP,HUB_DATA_PORT)).start()
threading.Thread(target=receive, args=(sock, HUB_IP, HUB_DATA_PORT)).start()


