import socket
import threading
from time import sleep

DATA_PROC_IP = "0.0.0.0"
DATA_PROC_PORT =49148
Message = "Hello, Client"

def receive(sock, ip, port):
    while True:
        data = sock.recv(1024)
        print("Received from Hub: " + data.decode("utf-8"))

def publish(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect((ip, port))
    while True:
        sleep(2.0)
        print("sending data to data process.")
        sock.sendto(bytes(Message, "utf-8"), (ip, port))

threading.Thread(target=publish, args=(DATA_PROC_IP, DATA_PROC_PORT)).start()
