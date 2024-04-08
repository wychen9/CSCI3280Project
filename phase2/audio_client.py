
import socket
import threading
import pyaudio
import time

class Client():
    def __init__(self, target_ip, target_port):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.target_ip = target_ip
        self.target_port = int(target_port)
        while 1:
            try:
                self.s.connect((self.target_ip, self.target_port))
                break
            except Exception as e:
                print("Couldn't connect to server")

        chunk_size = 1024
        audio_format = pyaudio.paInt16
        channels = 1
        rate = 20000

        self.p = pyaudio.PyAudio()
        self.playing_stream = self.p.open(format=audio_format, channels=channels, rate=rate, output=True,
                                          frames_per_buffer=chunk_size)
        self.recording_stream = self.p.open(format=audio_format, channels=channels, rate=rate, input=True,
                                            frames_per_buffer=chunk_size)

        self.mic_open = True
        self.running = True
        print("Connected to Server")

    def init_audio(self):
        chunk_size = 1024
        audio_format = pyaudio.paInt16
        channels = 1
        rate = 20000
        self.p = pyaudio.PyAudio()
        self.playing_stream = self.p.open(format=audio_format, channels=channels, rate=rate, output=True,
                                          frames_per_buffer=chunk_size)
        self.recording_stream = self.p.open(format=audio_format, channels=channels, rate=rate, input=True,
                                            frames_per_buffer=chunk_size)


    def receive_server_data(self):
        while self.running:
            try:
                data = self.s.recv(1024)
                self.playing_stream.write(data)
            except:
                pass

    def send_data_to_server(self):
        while self.running:
            if self.mic_open:
                try:
                    #print("Mic is open")
                    data = self.recording_stream.read(1024)
                    self.s.sendall(data)
                except:
                    pass
            else:
                time.sleep(0.1)
    
    def open_mic(self):
        self.mic_open = True
        self.init_audio()
        #print("Mic is now open:", self.mic_open)

    def close_mic(self):
        self.mic_open = False


    def stop(self):  # add this method
        self.running = False
        self.s.close()
        self.p.terminate()

    def run(self):
        receive_thread = threading.Thread(target=self.receive_server_data).start()
        send_thread = threading.Thread(target=self.send_data_to_server).start()



def control(cmd):
        command = cmd
        #command = input("Enter command (start, open mic, close mic, exit):")
        if command.startswith("start"):
            _, ip, port = command.split()
            client = Client(ip, port)
            client.run()
        elif command in ["open mic", "close mic", "exit"]:
            if client is None:
                print("Please start the client first.")
            if command == "open mic":
                client.open_mic()
            elif command == "close mic":
                client.close_mic()
            elif command == "exit":
                client.stop()
        else:
            print("Unknown command")


if __name__ == '__main__':
    control()
    #create_server(audioserver)
