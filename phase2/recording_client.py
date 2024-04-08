import requests
import os
import wave
from multiUsersRecorder import AudioRecorder, ChatRoomRecorder

SERVER_IP = '127.0.0.1'
SERVER_PORT = 8888
SERVER_URL = f"http://{SERVER_IP}:{SERVER_PORT}"

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
            with open(recording_file, 'rb') as f:
                files = {'file': f}
                response = requests.post(f"{SERVER_URL}/upload", files=files)
                if response.status_code == 200:
                    print("Recording uploaded successfully")
                else:
                    print("Failed to upload recording")
        else:
            print("No recording to upload")
      
    def download_recording(self, file_name):
        response = requests.get(f"{SERVER_URL}/download/{file_name}")
        if response.status_code == 200:
            with open(file_name, 'wb') as f:
                f.write(response.content)
            print(f"Recording downloaded successfully: {file_name}")
        else: 
            print("Failed to download recording")
    
    def list_recording(self):
        response = requests.get("{SERVER_URL}")
        if response.status_code == 200:
            print("Available recordings:", response.text)
        else:
            print("Failed to list recordings.")
