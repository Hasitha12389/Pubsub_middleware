import socket
import threading
import sys

subscribers = []

def client_communication_handler(client_socket, role):
    if role == "SUBSCRIBER":
        subscribers.append(client_socket)
        print("A Subscriber connected.\n")
    elif role == "PUBLISHER":
        print("A Publisher connected.\n")

    while True:
        try:
            message = client_socket.recv(1024).decode()
            if message.lower() == "terminate":
                break
            if role == "PUBLISHER":
                print(f"[PUBLISHER]  :  {message}")
                for sub in subscribers:
                    try:
                        sub.send(f"\n[PUBLISHER]  :  {message}".encode())
                    except Exception as e:
                        pass
        except Exception as e:
            break

    client_socket.close()
    if client_socket in subscribers:
        subscribers.remove(client_socket)
    print(f"\nA {role} disconnected.")

def start_server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('', port))
    server_socket.listen(10)
    print(f"\nListening on port  :  {port} ...\n")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection established with client in {addr}")
        role = client_socket.recv(1024).decode()
        threading.Thread(target=client_communication_handler, args=(client_socket, role)).start()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("\nWrong Command format!:")
        print("Please Enter 'python server.py <PORT>' format command.\n")
        sys.exit(1)
    start_server(int(sys.argv[1]))