import socket
import threading
import sys

def receive_messages(sock):
    while True:
        try:
            msg = sock.recv(1024).decode()
            if msg:
                print(msg)
        except:
            break

def start_newClient(ip, port, role):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    sock.send(role.encode())
    print(f"\nServer running at IP: {ip} on port: {port}")
    print("To end the session type 'terminate'\n")


    if role == "SUBSCRIBER":
        threading.Thread(target=receive_messages, args=(sock,)).start()

    while True:
        msg = input("You    :   ")
        sock.send(msg.encode())
        if msg.lower() == "terminate":
            break

    sock.close()
    print("Disconnected from server.\n")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("\nWrong Command format!:")
        print("Please Enter 'python client.py <SERVER_IP> <PORT> <PUBLISHER/SUBSCRIBER>' format command.\n")
        sys.exit(1)
    start_newClient(sys.argv[1], int(sys.argv[2]), sys.argv[3].upper())