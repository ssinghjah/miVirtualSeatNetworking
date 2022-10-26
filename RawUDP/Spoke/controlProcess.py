import socket
import json

HUB_IP = "44.211.205.92"   # The hub's hostname or IP address
HUB_CONTROL_PORT = 65432  # The port used by the hub
ID = "1"
DEVICE_TYPE = "VP"
UI_PORT = 49153
BUFFER_SIZE = 1024

def sendControlMessage(message):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HUB_IP, HUB_CONTROL_PORT))
        s.sendall(bytes(message, "utf-8"))
        response = s.recv(BUFFER_SIZE)
        print("response from Hub: " + str(response))

def register():
    message = {}
    message['message'] = 'register'
    message['id'] = ID
    message['device-type'] = DEVICE_TYPE
    message_json = json.dumps(message)
    sendControlMessage(message_json)

def processUIMessage(message):
    response = 'error.'
    if message == 'register':
        register()
        response = 'message sent to hub'
    return response
    
    
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(("127.0.0.1", UI_PORT))
    while True:
        s.listen()
        conn, addr = s.accept()
        print("Listening ... ")
        with conn:
            print(f"Connected by {addr}")
            while True:
                data = conn.recv(BUFFER_SIZE)
                if not data:
                    break
                data = data.decode("utf-8")
                print("Received from UI: " + data)
                response = processUIMessage(data)
                if response != None:
                    conn.send(bytes(response, "utf-8"))
