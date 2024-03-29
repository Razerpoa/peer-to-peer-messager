import socket
import threading
import argparse
from cryptography.fernet import Fernet
import time

HOST = '127.0.0.1'  # Use localhost for testing
PORT = 7777
own_key = Fernet.generate_key()

def encrypt(message):
    fernet = Fernet(own_key)
    result = fernet.encrypt(message)
    return result

def decrypt(peer_key, encrypted_message):
    fernet = Fernet(peer_key)
    result = fernet.decrypt(encrypted_message)
    return result

def receive(client_socket, stop_event):
    peer_key = client_socket.recv(44)
    print(f"\nReceived key: {peer_key}")
    while True:
        if stop_event == True:
            print("Received stop signal. Exiting...")
            break
        try:
            msg = client_socket.recv(1024).decode()
            if not msg:
                print("Client disconnected")
                client_socket.shutdown(socket.SHUT_RDWR)
                client_socket.close()
                stop_event == True
                break
            data = str(decrypt(peer_key, msg))
            print(f"\nReceived: {data[1:]}")
        except ConnectionResetError:
            print("Connection reset by peer")
            break

def send(client_socket, stop_event):
    client_socket.sendall(own_key)
    time.sleep(1)
    while True:
        message = input("message: ")
        if message == 'exit':
            print("Exiting...")
            stop_event = True
            client_socket.close()
            break
        if stop_event == True:
            print("Received stop signal. Exiting...")
            break
        try:
            client_socket.sendall(encrypt(message.encode('utf-8')))
        except ConnectionResetError:
            print("Connection reset by peer")
            break
        except socket.error:
            print("Socket error")
            break

def server_mode(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection established with {client_address}")

        stop_event = threading.Event()

        thread_send = threading.Thread(target=send, args=(client_socket, stop_event))
        thread_recv = threading.Thread(target=receive, args=(client_socket, stop_event))

        thread_send.start()
        thread_recv.start()

        thread_send.join()
        thread_recv.join()

        client_socket.close()

def client_mode(host, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    print("Connected to server.")

    stop_event = threading.Event()

    thread_send = threading.Thread(target=send, args=(client_socket, stop_event))
    thread_recv = threading.Thread(target=receive, args=(client_socket, stop_event))

    thread_send.start()
    thread_recv.start()

    thread_send.join()
    thread_recv.join()

    client_socket.close()

def main():
    parser = argparse.ArgumentParser(description="A peer-to-peer messager program")
    parser.add_argument("mode", choices=["listen", "sender"], help="Choose listen (server) or sender (client) mode")
    parser.add_argument("-H", "--host", default='127.0.0.1', help="Host address (default: localhost)")
    parser.add_argument("-P", "--port", type=int, default=7777, help="Port number (default: 7777)")
    args = parser.parse_args()

    if args.mode == "listen":
        server_mode(args.host, args.port)
    elif args.mode == "sender":
        client_mode(args.host, args.port)
    else:
        print("Invalid mode. Choose 'listen' or 'send'.")

if __name__ == '__main__':
    main()