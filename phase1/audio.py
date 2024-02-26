
import wave
import pyaudio
from datetime import datetime

# Set the audio parameters
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 5

current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
WAVE_OUTPUT_FILENAME = f"recording_{current_time}.wav"

# Initialize the audio stream
audio = pyaudio.PyAudio()
stream = audio.open(format=FORMAT, channels=CHANNELS,
          rate=RATE, input=True,
          frames_per_buffer=CHUNK)

# Create a WAV file
frames = []
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
  data = stream.read(CHUNK)
  frames.append(data)


stream.stop_stream()
stream.close()
audio.terminate()


wave_file = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wave_file.setnchannels(CHANNELS)
wave_file.setsampwidth(audio.get_sample_size(FORMAT))
wave_file.setframerate(RATE)
wave_file.writeframes(b''.join(frames))
wave_file.close()