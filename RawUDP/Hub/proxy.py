import socket
from time import sleep
import threading
import json

KEEP_ALIVE_INTERVAL = 5
DATA_BUFFER_SIZE = 65000
SERVER_PORTs = [49152, 49153]
SERVER_SOCKs = [None, None]
NUM_SERVERs = 2
SERVER_ADDRs = [None, None]
Lock = threading.Lock()

def keepAlive(sock, addr):
    while True:
        sleep(KEEP_ALIVE_INTERVAL)
        print("sending keep alive to ... " + str(addr))
        sock.sendto(b"Keep alive from Hub ...", addr)

def listenForData(sock, serverNum):
    while True:
        data, addr = sock.recvfrom(DATA_BUFFER_SIZE)
        print ("Message: ", data)
        for otherServerNum in range(0, NUM_SERVERs):
            if otherServerNum != serverNum - 1:
                otherServerSock = SERVER_SOCKs[otherServerNum-1]
                otherServerSock.sendto(data, SERVER_ADDRs[otherServerNum-1])
            
def launchDataProcess(serverNum):
    HOST = "0.0.0.0"
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((HOST, SERVER_PORTs[serverNum-1]))
    global SERVER_SOCKs, SERVER_ADDRs, Lock
    SERVER_SOCKs[serverNum - 1] = sock
    print("listening for server: " + str(serverNum))
    data, addr = sock.recvfrom(DATA_BUFFER_SIZE)
    SERVER_ADDRs[serverNum - 1] = addr
    print ("Message: ", data)
    threading.Thread(target=keepAlive, args=(sock, addr,)).start()
    threading.Thread(target=listenForData, args=(sock, serverNum)).start()

t1=threading.Thread(target=launchDataProcess,args=(1,))
t2=threading.Thread(target=launchDataProcess,args=(2,))
t1.start()
t2.start()
t1.join()
t2.join()
