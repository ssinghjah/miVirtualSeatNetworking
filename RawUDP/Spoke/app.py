import socket
import threading
from time import sleep
import time
import os

DATA_PROC_IP = "0.0.0.0"
DATA_PROC_PORT =49148
Message = "Hello, Server"
BUFFER_SIZE = 65000
INTER_MESSAGE_INTERVAL = 1
rxMessage = None
SEND_ACKs = True
TX = True
APP_MESSAGE_SIZE = 2048

TX_FILE_PATH = "./Logs/tx_" + str(time.time()) + ".csv"
RX_FILE_PATH = "./Logs/rx_" + str(time.time()) + ".csv"
ACKs_FILE_PATH = "./Logs/acks_" + str(time.time()) + ".csv"

APP_LISTEN_PORT = 49147

COUNTER_BYTE_SIZE = 4
MESSAGE_TYPE_BYTE_SIZE = 1

ACK_MESSAGE_TYPE = b'\x02'
DATA_MESSAGE_TYPE = b'\x01'
KEEP_ALIVE_MESSAGE_TYPE = b'\x03'

def receive():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", APP_LISTEN_PORT))
    while True:
        data = sock.recv(BUFFER_SIZE)
        threading.Thread(target=processRxMessage, args=(data,)).start()

def writeToFile(filePath, content):
    # append message to file
    f = open(filePath, "a")
    f.write(content)
    f.close()
    
def publish(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #sock.connect((ip, port))
    counter = 1
    while True:
        sleep(INTER_MESSAGE_INTERVAL)
        #print("sending data to data process.")
        message = DATA_MESSAGE_TYPE
        message += counter.to_bytes(COUNTER_BYTE_SIZE, "big")
        message += os.urandom(APP_MESSAGE_SIZE - MESSAGE_TYPE_BYTE_SIZE - COUNTER_BYTE_SIZE)
        sock.sendto(message, (ip, port))
        writeToFile(TX_FILE_PATH, str(counter) + "," + str(time.time()) + "," + str(len(message)) + "\n")
        counter += 1

def processRxMessage(message):
    messageType = message[:1]
    if messageType == DATA_MESSAGE_TYPE:
        sequence = int.from_bytes(message[1:COUNTER_BYTE_SIZE+1], "big")
        ack = ACK_MESSAGE_TYPE + message[1:COUNTER_BYTES+1]
        print(sequence)
        writeToFile(RX_FILE_PATH, str(sequence) + str(time.time()) + "," + str(len(message)) + "\n")
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(ack, (DATA_PROC_IP, DATA_PROC_PORT))
    elif messageType == ACK_MESSAGE_TYPE:
        sequence = int.from_bytes(message[1:COUNTER_BYTE_SIZE+1], "big")
        print("Received ACK: " + str(sequence))
        writeToFile(ACKs_FILE_PATH, str(sequence) + "," + str(time.time()) + "\n")

if TX:
    threading.Thread(target=publish, args=(DATA_PROC_IP, DATA_PROC_PORT)).start()
threading.Thread(target=receive).start()
