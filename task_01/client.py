import socket
import sys


def start_newClient(server_ip, server_port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))
    print(f"\nServer running at IP: {server_ip} on port: {server_port}")
    print("To end the session type 'terminate'\n")

    while True:
        msg = input("You: ")
        client_socket.send(msg.encode())
        if msg.lower() == "terminate":
            break

    client_socket.close()
    print("Disconnected from server.\n")


# main
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("\nWrong Command format!:")
        print("Usage: python client.py <SERVER_IP> <PORT>\n")
        sys.exit(1)
    start_newClient(sys.argv[1], int(sys.argv[2]))
