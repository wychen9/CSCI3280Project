import socket
import threading
import pyaudio
import time
#import opuslib

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
        # self.encoder = opuslib.Encoder(48000, 2, opuslib.APPLICATION_AUDIO)
        # self.decoder = opuslib.Decoder(48000, 2)
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
                #pcm_data = self.decoder.decode(data, 960)
                self.playing_stream.write(data)
            except:
                pass

    def join_room(self, room):
        self.s.sendall(("join " + room).encode())

    def leave_room(self, room):
        self.s.sendall(("leave " + room).encode())
        self.stop()

    def send_data_to_server(self):
        while self.running:
            if self.mic_open:
                try:
                    #print("Mic is open")
                    data = self.recording_stream.read(1024)
                    #opus_data = self.encoder.encode(data, 960)
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


    def stop(self):
        self.running = False
        self.s.close()
        self.p.terminate()

    def run(self):
        receive_thread = threading.Thread(target=self.receive_server_data).start()
        send_thread = threading.Thread(target=self.send_data_to_server).start()

def test():
    client = None
    while True:
        command = input("Enter command (start, open mic, close mic, join, leave, exit):")
        if command.startswith("start"):
            _, ip, port = command.split()
            client = Client(ip, port)
            
        elif command.startswith("join"):
            _, room = command.split()
            if client is None:
                print("Please start the client first.")
            else:
                client.join_room(room)
                client.run()
        elif command.startswith("leave"):
            _, room = command.split()
            if client is None:
                print("Please start the client first.")
            else:
                client.leave_room(room)
                #client.stop()
                break
        elif command in ["open mic", "close mic"]:
            if client is None:
                print("Please start the client first.")
            elif command == "open mic":
                client.open_mic()
            elif command == "close mic":
                client.close_mic()
        elif command == "exit":
            if client is not None:
                client.stop()
            break
        else:
            print("Unknown command")

#client = None

def control(cmd):
    global client
    command = cmd
    if command.startswith("start"):
        _, ip, port = command.split()
        client = Client(ip, port)
        
    elif command.startswith("join"):
        _, room = command.split()
        if client is None:
            print("Please start the client first.")
        else:
            client.join_room(room)
            client.run()
    elif command.startswith("leave"):
        _, room = command.split()
        if client is None:
            print("Please start the client first.")
        else:
            client.leave_room(room)
            #client.stop()
    elif command in ["open mic", "close mic", "exit"]:
        if client is None:
            print("Please start the client first.")
        else:
            if command == "open mic":
                client.open_mic()
            elif command == "close mic":
                client.close_mic()
            elif command == "exit":
                client.stop()
    else:
        print("Unknown command")

if __name__ == "__main__":
    test()
