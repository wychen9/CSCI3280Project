import os
import socket
from multiUsersRecorder import ChatRoomRecorder

SERVER_IP = '10.13.79.153'
SERVER_PORT = 12345

class RecordingClient:
    def __init__(self, room_name, ip = '127.0.0.1'):
        self.room_name = room_name
        self.chat_room_recorder = ChatRoomRecorder()
        self.sock = self.connect_to_server()
        self.ip = ip
    
    def connect_to_server(self):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((self.ip, SERVER_PORT))
            return sock
        except Exception as e:
            print(f"error in connecting to the server: {e}")
            return None
    
    def start_recording(self):
        # start recording
        self.chat_room_recorder.start_recording(self.room_name)
    
    def stop_and_upload_recording(self):
        recording_file = self.chat_room_recorder.stop_recording(self.room_name)
        if recording_file and self.sock:
            try:
          
                # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    # sock.connect((SERVER_IP, SERVER_PORT))
           
                    # send upload command and file metadata 
                    file_name = os.path.basename(recording_file)
                    file_size = os.path.getsize(recording_file)
                    header = f"u#{self.room_name}#{file_name}#{file_size}".encode()
                    self.sock.sendall(header)
                    with open(recording_file, 'rb') as f:
                        while True:
                            chunk = f.read(4096)
                            if not chunk:
                                break
                            self.sock.sendall(chunk)
                    self.sock.shutdown(socket.SHUT_WR)
                    print("sent to the server。")
            except Exception as e:
                print(f"error in sending files: {e}")
        else:
            print("no recording file to upload")
      
    def download_recording(self, file_name):
        if self.sock:
            try:
                # send download command and file metadata
                request_message = f"d#{self.room_name}#{file_name}".encode()
                self.sock.sendall(request_message)
                # receive file data
                file_size = int(self.sock.recv(4096).decode())
                if file_size:
                    with open(file_name, 'wb') as f:
                        bytes_received = 0
                        while bytes_received < file_size:
                            chunk = self.sock.recv(min(4096, file_size - bytes_received))

                            if not chunk:
                                break
                            f.write(chunk)
                            bytes_received += len(chunk)
                        print(f"file {file_name} downloaded successfully.")
                else:
                    print(f"file {file_name} not found.")
            except Exception as e:
                print(f"error in downloading files: {e}")

    
    def list_recordings(self):
      if self.sock:
            try:
                request_message = f"l#{self.room_name}".encode()
                self.sock.sendall(request_message)
                self.sock.shutdown(socket.SHUT_WR)  # send EOF
                recordings_list = ""
                while True:
                    chunk = self.sock.recv(4096)
                    if not chunk:
                        break
                    recordings_list += chunk.decode()
                print(f"Recordings in room {self.room_name}:\n {recordings_list}")
            except Exception as e:
                print(f"error in lisiting files:{e}")


'''
if __name__ == '__main__':
    client = RecordingClient("my_room_name")
    client.start_recording()

    client.stop_and_upload_recording()
'''

