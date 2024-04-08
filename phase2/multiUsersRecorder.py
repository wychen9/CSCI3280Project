import pyaudio
import wave
import struct
from datetime import datetime
import time
import os

class AudioRecorder:
    def __init__(self, format=pyaudio.paInt16, channels=1, rate=44100, chunk=1024):
        self.format = format
        self.channels = channels
        self.sample_width = pyaudio.PyAudio().get_sample_size(self.format)
        self.rate = rate
        self.chunk = chunk
        self.frames = []
        self.is_recording = False
        self.audio = None
        self.stream = None

    def generate_wav_header(self, num_frames):
        # generate the WAV file header based on the provided parameters
        bits_per_sample = self.sample_width * 8
        byte_rate = self.rate * self.channels * bits_per_sample // 8
        block_align = self.channels * bits_per_sample // 8
        subchunk2_size = num_frames * self.channels * bits_per_sample // 8

        riff_chunk = struct.pack('<4sI4s', b'RIFF', 36 + subchunk2_size, b'WAVE')
        fmt_chunk = struct.pack('<4sIHHIIHH',
                                b'fmt ',
                                16,  # subchunk1Size
                                1,   # audioFormat (1 for PCM)
                                self.channels,
                                self.rate,
                                byte_rate,
                                block_align,
                                bits_per_sample)
        data_chunk_header = struct.pack('<4sI', b'data', subchunk2_size)

        return riff_chunk + fmt_chunk + data_chunk_header

    def start_recording(self):
        # start recording audio data
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=self.format, channels=self.channels,
                                      rate=self.rate, input=True,
                                      frames_per_buffer=self.chunk,
                                      stream_callback=self.callback)
        self.is_recording = True
        self.frames.clear()
        self.stream.start_stream()
        print("Recording started...")

    def callback(self, in_data, frame_count, time_info, status):
        # callback function to handle incoming audio data
        if self.is_recording:
            self.frames.append(in_data)
            return (in_data, pyaudio.paContinue)
        else:
            return (None, pyaudio.paComplete)

    def stop_recording(self):
        # stop recording and save the recorded audio data to a file
        if self.is_recording:
            self.is_recording = False
            self.stream.stop_stream()
            while self.stream.is_active():
                pass  # wait for the stream to naturally stop
            self.stream.close()
            self.audio.terminate()
            print("Recording stopped.")
            return self.save_recording()
        else:
            print("Recording was not active.")
            return None

    def get_total_recording_length(self):
        # get the total length of the recorded audio in seconds
        total_bytes = sum(len(frame) for frame in self.frames)
        num_frames = sum(len(frame) for frame in self.frames) // (self.sample_width * self.channels)
        total_seconds = num_frames / self.rate
        return total_seconds

    def save_recording(self):
        # Save the recorded audio data to a WAV file in the shared directory
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        wave_output_filename = f"recording_{current_time}.wav"
        num_frames = sum(len(frame) for frame in self.frames) // (self.sample_width * self.channels)
        wav_header = self.generate_wav_header(num_frames)

        shared_dir = "shared_recordings"
        if not os.path.exists(shared_dir):
            os.makedirs(shared_dir)
        wave_output_filename = os.path.join(shared_dir, wave_output_filename)

        with open(wave_output_filename, 'wb') as wf:
            wf.write(wav_header)
            for frame in self.frames:
                wf.write(frame)

        print(f"File saved as {wave_output_filename}")
        return wave_output_filename

class ChatRoomRecorder:
    def __init__(self):
        self.room_recorders = {}  # {room_name: AudioRecorder instance}

    def start_recording(self, room_name):
        # start recording for the specified room
        if room_name not in self.room_recorders:
            self.room_recorders[room_name] = AudioRecorder()
        self.room_recorders[room_name].start_recording()

    def stop_recording(self, room_name):
        # stop recording and save the recorded audio for the specified room
        if room_name in self.room_recorders:
            return self.room_recorders[room_name].stop_recording()
        else:
            print(f"No active recording for room: {room_name}")
            return None

    def get_recording_files(self, room_name):
        # get a list of recorded audio files for the specified room
        shared_dir = "shared_recordings"
        files = os.listdir(shared_dir)
        room_files = [f for f in files if room_name in f]
        return room_files
