import sounddevice as sd
import soundfile as sf
import noisereduce as nr
import librosa
import librosa.display
import threading
from decoder import read_wav

class AudioPlayer:
    def __init__(self, path):
        recording = read_wav(path)
        self.raw_audio = recording['audio_data']
        self.audio = self.raw_audio
        self.sr = recording['frame_rate']
        self.speed = 1.0
        self.start = 0
        self.end = len(self.raw_audio)

    def reduce(self):
        self.audio = nr.reduce_noise( self.raw_audio, self.sr)
        
    def set(self, speed=1.0, start=0):
        self.speed = speed
        self.start = start
    
    def set(self, speed=1.0, start=0, end=None):
        if end is None:
            self.end = len(self.audio)
        else:
            self.end = end
        self.speed = speed
        self.start = start
        

    def stretch(self, data, rate):
        return librosa.effects.time_stretch(data, rate=rate)

    def play(self):
        start_sample = int(self.start * self.sr)
        end_sample = int(self.end * self.sr)
        audio_to_play = self.stretch(self.audio[start_sample:end_sample], self.speed)
        sd.play(audio_to_play, self.sr)

    def stop(self):
        sd.stop()



def control(command):
    #command = input()
    global recording 
    words = command.split(' ')
    if words[0] == 'load':
        recording = AudioPlayer(words[1])
    elif words[0] == 'reduce':
        if words[1] == 'on':
            recording.reduce()
        elif words[1] == 'off':
            recording.audio = recording.raw_audio
    elif words[0] == 'set':
        if len(words) == 3:
            recording.set(float(words[1]), float(words[2]))
        elif len(words) == 4:
            recording.set(float(words[1]), float(words[2]), float(words[3]))
    elif command == 'play':
        play_thread = threading.Thread(target=recording.play, args=())
        play_thread.start()
    elif command == 'stop':
        recording.stop()
    else:
        print("Invalid command, please try again.")

