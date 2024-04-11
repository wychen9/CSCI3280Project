import socket
import threading
import os

ip = '10.13.79.153'
port = 12345
DIRECTORY = "shared_recordings"

class RecordingServer:
    def __init__(self):
        # ensure the shared directory exists
        if not os.path.exists(DIRECTORY):
            os.makedirs(DIRECTORY)

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((ip, port))
        self.sock.listen(5)  # listen for connections made to the socket
        print(f"Server started at {ip}:{port}")

        self.clients = []
        self.server_thread = threading.Thread(target=self.accept_connections)
        self.server_thread.start()

    def accept_connections(self):
        while True:
            client, address = self.sock.accept()
            print(f"Connection from {address} has been established.")
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
                        self.receive_file(client, room_name, file_name)
                    elif command == 'd':
                        # Handle file download
                        self.send_file(client, room_name, file_name)
                    elif command == 'l':
                        # Handle listing files
                        self.list_files(client, room_name)

                except Exception as e:
                    print(f"An error occurred: {e}")
                    break

    def receive_file(self, client, room_name, file_name):
       
        file_size = int(client.recv(4096).decode())
        received_size = 0
        room_directory = os.path.join(DIRECTORY, room_name)
        if not os.path.exists(room_directory):
            os.makedirs(room_directory)
        file_path = os.path.join(room_directory, file_name)
        with open(file_path, 'wb') as file:
            while received_size < file_size:
                file_data = client.recv(4096)
                if not file_data:
                    break
                file.write(file_data)
                received_size += len(file_data)
        print(f"File {file_name} saved in room {room_name}")

    def send_file(self, client, room_name, file_name):
        file_path = os.path.join(DIRECTORY, room_name, file_name)
        if os.path.isfile(file_path):
            file_size = os.path.getsize(file_path)
            # Send the file size first
            client.sendall(str(file_size).encode('utf-8'))
            with open(file_path, 'rb') as file:
                client.sendfile(file)
            print(f"File {file_name} sent to client.")
        else:
            print(f"File {file_name} not found.")
            client.sendall(b"0")  # send '0' to indicate file not found

    def list_files(self, client, room_name):
        room_directory = os.path.join(DIRECTORY, room_name)
        if os.path.exists(room_directory):
            files = os.listdir(room_directory)
            client.sendall('\n'.join(files).encode('utf-8'))
        else:
            client.sendall(b"")  # send empty bytes to indicate room not found
        print(f"List of recordings sent for room {room_name}")

    def shutdown(self):
        for client in self.clients:
            client.close()
        self.sock.close()
        print("Server has been shut down.")

if __name__ == '__main__':
    server = RecordingServer()
    try:
        server.server_thread.join()
    except KeyboardInterrupt:
        server.shutdown()



