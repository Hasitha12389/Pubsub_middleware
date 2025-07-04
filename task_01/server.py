import socket
import sys


def start_server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('', port))
    server_socket.listen(1)
    print(f"\nListening on port {port} ...")

    client_socket, addr = server_socket.accept()
    print(f"Connection established with client in {addr}\n")

    while True:
        data = client_socket.recv(1024).decode()
        if data.lower() == "terminate":
            print("Client requested termination.")
            break
        print(f"CLIENT  :  {data}")

    client_socket.close()
    server_socket.close()
    print("SERVER  :  Connection closed.\n")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("\nWrong Command format!:")
        print("\nPlease Enter 'python server.py <PORT>' format command.\n")
        sys.exit(1)
    start_server(int(sys.argv[1]))
