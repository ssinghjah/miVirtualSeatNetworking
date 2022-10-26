import socket
import json

HOST = "0.0.0.0"
HUB_CONTROL_PORT = 65432  # Port to listen on (non-privileged ports are > 1023)
TO_CLIENT_PORTs = [65433, 65434, 65435, 65436]
FROM_CLIENT_PORTs = [65443, 65444, 65445, 65446]
ID_PORT_MAP = {'1': 49152}

def getUnusedPort():
    pass

def openUDPPort(id, port):
    message = {}
    message['id'] = id
    message['port'] = port
    message_json = json.dumps(message)
    print(message_json)
    dataProcessSock.sendto(bytes(message_json, "utf-8"), ("127.0.0.1", DATA_PROC_PORT))

def parseControlData(data):
    response = None
    print(data)
    message = json.loads(data.decode("utf-8"))
    if message["message"] == "register":
        id = message["id"]
        
        response = "confirm"
        openUDPPort(id, 49152)
        print(id)
    '''
    if "StartRx" in data:
        id = 1
        # port = #parse port
        # forward command and ID to 3D Scene Generator
        # forward command, ID, and port to DataProcess
    if "StartTx" in data:
        pass
        # id = # parse id
        # port = # get port from dictionary
        # forward command and ID to 3D Scene Generator
        # DataProcess sends data to the 3D Scene Generator
    if "KeepAlive" in data:
        pass
        # id = # parse id
    if "DeRegister" in data:
        pass
        #id = # parse id
        # release all resources kept for id
    '''
    return response



DATA_PROC_PORT = 49155
dataProcessSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, HUB_CONTROL_PORT))
    while True:
        s.listen()
        conn, addr = s.accept()
        print("Listening ... ")
        with conn:
            print(f"Connected by {addr}")
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                response = parseControlData(data)
                if response != None:
                    conn.send(bytes(response, "utf-8"))
