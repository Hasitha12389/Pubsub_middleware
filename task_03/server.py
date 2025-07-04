import socket
import threading
import sys
from collections import defaultdict

subscribers = defaultdict(list)  # topic: [socket list]

def client_communication_handler(client_socket, role, topic):
    if role == "SUBSCRIBER":
        subscribers[topic].append(client_socket)
        print(f"Topic '{topic}' subscriber connected.\n")
    elif role == "PUBLISHER":
        print(f"Topic '{topic}' Publisher connected.\n")

    while True:
        try:
            message = client_socket.recv(1024).decode()
            if message.lower() == "terminate":
                break
            if role == "PUBLISHER":
                print(f"[{topic}] {message}")
                for sub in subscribers[topic]:
                    try:
                        sub.send(f"[{topic}] {message}".encode())
                    except:
                        pass
        except:
            break

    client_socket.close()
    if role == "SUBSCRIBER" and client_socket in subscribers[topic]:
        subscribers[topic].remove(client_socket)
    print(f"Topic '{topic}' {role} disconnected.")

def start_server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('', port))
    server_socket.listen(10)
    print(f"\nListening on port  :  {port} ...\n")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection established with client in {addr}")
        meta = client_socket.recv(1024).decode().split()
        if len(meta) != 2:
            continue
        role, topic = meta[0], meta[1]
        threading.Thread(target=client_communication_handler, args=(client_socket, role, topic)).start()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("\nWrong Command format!:")
        print("Please Enter 'python server.py <PORT>' format command.\n")
        sys.exit(1)
    start_server(int(sys.argv[1]))