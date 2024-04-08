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
                    with open(recording_file, 'rb') as f:
                        file_data = f.read()
                        # the protocol "u#room_name#file_name@file_data"
                        file_name = os.path.basename(recording_file)
                        message = f"u#{self.room_name}#{file_name}@".encode() + file_data
                        sock.sendall(message)
                    print("sent to the server。")
            except Exception as e:
                print(f"error in sending files：{e}")              
        else:
            print("no recording file to upload")
      
    def download_recording(self, file_name):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect((SERVER_IP, SERVER_PORT))
                request_message = f"d#{self.room_name}#{file_name}".encode()
                sock.sendall(request_message)
                # assume that the file will fit into memory
                file_data = sock.recv(1024 * 1024)
                if file_data:
                    with open(file_name, 'wb') as f:
                        f.write(file_data)
                    print(f"file {file_name} is downloaded。")
                else:
                    print("error in downloading file")
        except Exception as e:
            print(f"error in downloading file：{e}")

    
    def list_recordings(self):
      try:
          with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
              sock.connect((SERVER_IP, SERVER_PORT))
              request_message = f"l#{self.room_name}".encode()
              sock.sendall(request_message)
              recordings_list = sock.recv(1024).decode()
              print(f"room '{self.room_name}' with recording lists：\n{recordings_list}")
      except Exception as e:
          print(f"broken files：{e}")
