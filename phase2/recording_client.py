import os
import socket
from multiUsersRecorder import ChatRoomRecorder

SERVER_IP = '127.0.0.1'
SERVER_PORT = 8888

class RecordingClient:
    def __init__(self, room_name):
        self.room_name = room_name
        self.chat_room_recorder = ChatRoomRecorder()
    
    def start_recording(self):
        # start recording
        self.chat_room_recorder.start_recording(self.room_name)
    
    def stop_and_upload_recording(self):
        recording_file = self.chat_room_recorder.stop_recording(self.room_name)
        if recording_file:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    sock.connect((SERVER_IP, SERVER_PORT))
                    # send upload command and file metadata 
                    file_name = os.path.basename(recording_file)
                    file_size = os.path.getsize(recording_file)
                    header = f"u#{self.room_name}#{file_name}#{file_size}".encode()
                    sock.sendall(header)
                    with open(recording_file, 'rb') as f:
                        while True:
                            chunk = f.read(4096)
                            if not chunk:
                                break
                            sock.sendall(chunk)
                    print("sent to the server。")
            except Exception as e:
                print(f"error in sending files: {e}")
        else:
            print("no recording file to upload")
      
    def download_recording(self, file_name):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect((SERVER_IP, SERVER_PORT))
                request_message = f"d#{self.room_name}#{file_name}".encode()
                sock.sendall(request_message)
                # Assume that the file will fit into memory
                file_size = int(sock.recv(4096).decode())
                if file_size:
                    with open(file_name, 'wb') as f:
                        bytes_received = 0
                        while bytes_received < file_size:
                            chunk = sock.recv(min(4096, file_size - bytes_received))
                            if not chunk:
                                break
                            f.write(chunk)
                            bytes_received += len(chunk)
                    print(f"file {file_name} is downloaded。")
                else:
                    print("error in downloading file")
        except Exception as e:
            print(f"error in downloading file: {e}")

    
    def list_recordings(self):
      try:
          with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
              sock.connect((SERVER_IP, SERVER_PORT))
              request_message = f"l#{self.room_name}".encode()
              sock.sendall(request_message)
              sock.shutdown(socket.SHUT_WR) # indicates no more sending
              recordings_list = ""
              while True:
                  chunk = sock.recv(4096)
                  if not chunk:
                      break
                  recordings_list += chunk.decode()
              print(f"room '{self.room_name}' with recording lists:\n{recordings_list}")
      except Exception as e:
          print(f"broken files:{e}")
