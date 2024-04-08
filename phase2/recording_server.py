import socket
import threading
import os

ip = '127.0.0.1'
port = 8888
DIRECTORY = "shared_recordings"

class RecordingServer:
    def __init__(self):
        # make sure the shared directory exists
        if not os.path.exists(DIRECTORY):
            os.makedirs(DIRECTORY)

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((ip, port))
        self.sock.listen()
        print(f"Server started at {ip}:{port}")

        self.clients = []
        self.server_thread = threading.Thread(target=self.accept_connections)
        self.server_thread.daemon = True
        self.server_thread.start()

    def accept_connections(self):
        while True:
            client, address = self.sock.accept()
            print(f"Connection from {address} has been established.")
            client_thread = threading.Thread(target=self.handle_client, args=(client,))
            client_thread.daemon = True
            client_thread.start()
            self.clients.append(client)

    def handle_client(self, client):
        with client:
            while True:
                try:
                    data = client.recv(1024)
                    if not data:
                        break
                    
                    #  parse the data according to the protocol used by client.py
                    # Fthe protocol is to send a string "u#room_name#file_name@file_data"
                    # extract the room name, file name and file data here
                    
                    decoded_data = data.decode('utf-8')
                    if decoded_data.startswith('u#'):  # room_name
                        _, room_name, file_info = decoded_data.split('#', 2)  #file_name
                        file_name, file_data = file_info.split('@', 1)  #file_data
                        self.save_file(room_name, file_name, file_data.encode('utf-8'))
                    
                except Exception as e:
                    print(f"An error occurred: {e}")
                    break

    def save_file(self, room_name, file_name, file_data):
        room_directory = os.path.join(DIRECTORY, room_name)
        if not os.path.exists(room_directory):
            os.makedirs(room_directory)
        file_path = os.path.join(room_directory, file_name)
        with open(file_path, 'wb') as file:
            file.write(file_data)
        print(f"File {file_name} saved in room {room_name}")

    def shutdown(self):
        for client in self.clients:
            client.close()
        self.sock.close()
        print("Server has been shut down.")

recording_server = RecordingServer()
