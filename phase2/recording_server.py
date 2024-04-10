import socket
import threading
import os

ip = '127.0.0.1'
port = 8888
DIRECTORY = "shared_recordings"

class RecordingServer:
    def __init__(self):
        # ensure the shared directory exists
        if not os.path.exists(DIRECTORY):
            os.makedirs(DIRECTORY)

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((ip, port))
        self.sock.listen(5)  # listen for connections made to the socket
        print(f"server started at {ip}:{port}")

        self.clients = []
        self.server_thread = threading.Thread(target=self.accept_connections)
        self.server_thread.start()

    def accept_connections(self):
        while True:
            client, address = self.sock.accept()
            print(f"connection from {address} has been established.")
            client_thread = threading.Thread(target=self.handle_client, args=(client,))
            client_thread.start()
            self.clients.append(client)

    def handle_client(self, client):
        with client:
            while True:
                try:
                    data = client.recv(4096)
                    if not data:
                        break

                    decoded_data = data.decode('utf-8')
                    command, room_name, file_name = decoded_data.split('#', 2)
                    if command == 'u':
                        # handle file upload
                        file_data = client.recv(4096)
                        self.save_file(room_name, file_name, file_data)
                    elif command == 'd':
                        # Handle file download
                        self.send_file(client, room_name, file_name)
                    elif command == 'l':
                        # Handle listing files
                        self.list_files(client, room_name)

                except Exception as e:
                    print(f"an error occurred: {e}")
                    break

    def save_file(self, room_name, file_name, file_data):
        room_directory = os.path.join(DIRECTORY, room_name)
        if not os.path.exists(room_directory):
            os.makedirs(room_directory)
        file_path = os.path.join(room_directory, file_name)
        with open(file_path, 'wb') as file:
            file.write(file_data)
        print(f"File {file_name} saved in room {room_name}")

    def send_file(self, client, room_name, file_name):
        file_path = os.path.join(DIRECTORY, room_name, file_name)
        if os.path.isfile(file_path):
            with open(file_path, 'rb') as file:
                client.sendall(file.read())
            print(f"file {file_name} sent to client.")
        else:
            print(f"file {file_name} not found.")
            client.sendall(b"")  # send empty bytes to indicate file not found

    def list_files(self, client, room_name):
        room_directory = os.path.join(DIRECTORY, room_name)
        if os.path.exists(room_directory):
            files = os.listdir(room_directory)
            client.sendall('\n'.join(files).encode('utf-8'))
        else:
            client.sendall(b"")  # send empty bytes to indicate room not found
        print(f"list of recordings sent for room {room_name}")

    def shutdown(self):
        for client in self.clients:
            client.close()
        self.sock.close()
        print("server has been shut down.")


