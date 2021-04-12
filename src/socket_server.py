import threading
import socket

HEADER = 64
PORT = 5052
# SERVER = socket.gethostbyname(socket.gethostname())
SERVER = "LOCALHOST"
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

current_state = [0,0]
connections = []

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                print("hi")
                connected = False
                global connections
                connections.remove(conn)
            else:
                state_change(eval(msg))

            print(f"[{addr}] {msg}")

            # print("hi")
            # conn.send("Msg received".encode(FORMAT))

    conn.close()
        

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        connections.append(conn)
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

def state_change(new_state):
    global current_state
    current_state = new_state
    broadcast()
    print(current_state)

def broadcast():
    global current_state
    for conn in connections:
        conn.send(str(current_state).encode(FORMAT))


print("[STARTING] server is starting...")
start()