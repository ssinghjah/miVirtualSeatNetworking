import socket
from time import sleep
import threading
import json

KEEP_ALIVE_INTERVAL = 5
CONTROL_PORT = 49155

def keepAlive(sock, addr):
    while True:
        sleep(KEEP_ALIVE_INTERVAL)
        print("sending keep alive ... ")
        sock.sendto(b"Keep alive from Hub ...", addr)        

def listenForData(sock):
    while True:
        data, addr = sock.recvfrom(1024)    
        print ("Message: ", data)

        
def launchDataProcess(port, ID):               
    HOST = "0.0.0.0"
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((HOST, port))
    data, addr = sock.recvfrom(1024)    
    print ("Message: ", data)
    threading.Thread(target=keepAlive, args=(sock, addr,)).start()
    threading.Thread(target=listenForData, args=(sock,)).start()

    
def parseControlMessage(controlMessage):
    try:
        message = json.loads(controlMessage.decode("utf-8"))
        print(message)
        port = message["port"]
        id = message["id"]
        launchDataProcess(port, id)
    except Exception as e:
        print(str(e))
        print("error in processing control message: " + str(controlMessage))
    
controlSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
controlSocket.bind(("127.0.0.1", CONTROL_PORT))
while True:
    controlMessage, addr = controlSocket.recvfrom(1024)
    parseControlMessage(controlMessage)
    
