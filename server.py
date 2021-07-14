import socket
import threading

HOST = '127.0.0.01'
PORT = 8002

ser_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ser_sock.bind((HOST,PORT))

ser_sock.listen()

clients = []
names = []

#function for sending message to clients
def send(message):
    for client in clients:
        client.send(message)

#function for handling client
def handle_cli(client):
    while True:
        try:
            message = client.recv(1024)
            print(f"{names[clients.index(client)]}")
            send(message)
        except:
            #removing when disconnected 
            index = clients.index(client)
            client.close()
            name = names[index]
            names.remove(name)
            break


# fucntion for receiving client's message
def receive():
    while True:
        client, address = ser_sock.accept()
        print(f"Connected with {str(address)}!")
        client.send("name_key".encode("utf-8"))
        name = client.recv(1024)
        names.append(name)
        clients.append(client)
        print(f"Name {name}\n".encode("utf-8"))
        client.send("Connected!".encode("utf-8"))
        
        thread = threading.Thread(target=handle_cli, args=(client,))
        thread.start()

print("server running")
receive()