import cv2
import socket
import pickle
import numpy as np
import threading
from time import sleep

DATA_PROC_IP = "0.0.0.0"
DATA_PROC_PORT =49148
Message = "Hello, Client"
DATA_BUFFER_SIZE = 65000
APP_LISTEN_PORT = 49147

def receive():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", APP_LISTEN_PORT))
    frame_info = None
    buffer = None
    frame = None
    frameCount = 1

    while True:
        data = sock.recv(DATA_BUFFER_SIZE)
        print("Received from Hub: " + str(data))
        try:
            frame_info = pickle.loads(data)
        except:
            pass
        if frame_info and "packs" in frame_info:
            nums_of_packs = frame_info["packs"]
            for i in range(nums_of_packs):
                data, address = sock.recvfrom(DATA_BUFFER_SIZE)
                if i == 0:
                    buffer = data
                else:
                    buffer += data

            frame = np.frombuffer(buffer, dtype=np.uint8)
            frame = frame.reshape(frame.shape[0], 1)
            frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
            frame = cv2.flip(frame, 1)

            frameCount += 1

            if frame is not None and type(frame) == np.ndarray:
                cv2.imwrite("frame" + str(frameCount) +".jpg", frame)


def publish(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        sleep(2.0)
        print("sending data to data process.")
        sock.sendto(bytes(Message, "utf-8"), (ip, port))

#threading.Thread(target=publish, args=(DATA_PROC_IP, DATA_PROC_PORT)).start()
threading.Thread(target=receive).start()
