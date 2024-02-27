import pyaudio
import wave
import struct
from datetime import datetime

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
        bits_per_sample = self.sample_width * 8
        byte_rate = self.rate * self.channels * bits_per_sample // 8
        block_align = self.channels * bits_per_sample // 8
        subchunk2_size = num_frames * self.channels * bits_per_sample // 8
        
        riff_chunk = struct.pack('<4sI4s', b'RIFF', 36 + subchunk2_size, b'WAVE')
        fmt_chunk = struct.pack('<4sIHHIIHH',
                                b'fmt ',
                                16,  # Subchunk1Size
                                1,   # AudioFormat (1 for PCM)
                                self.channels,
                                self.rate,
                                byte_rate,
                                block_align,
                                bits_per_sample)
        data_chunk_header = struct.pack('<4sI', b'data', subchunk2_size)
        
        return riff_chunk + fmt_chunk + data_chunk_header

    def start_recording(self):
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=self.format, channels=self.channels,
                                      rate=self.rate, input=True,
                                      frames_per_buffer=self.chunk)
        self.is_recording = True
        self.frames.clear()
        print("Recording started...")

    def stop_recording(self):
        if self.is_recording:
            print("Recording stopped.")
            self.stream.stop_stream()
            self.stream.close()
            self.audio.terminate()
            self.is_recording = False
            return self.save_recording()
        else:
            print("Recording was not active.")
            return None

    def record(self):
        if self.is_recording:
            try:
                data = self.stream.read(self.chunk, exception_on_overflow=False)  
                if data:
                    self.frames.append(data)
                    print(f"Captured {len(data)} bytes of data.") 
            except IOError as e:
                print(f"Error recording: {e}")

    def get_total_recording_length(self):
        total_bytes = sum(len(frame) for frame in self.frames)
        num_frames = sum(len(frame) for frame in self.frames) // (self.sample_width * self.channels)
        total_seconds = num_frames / self.rate
        return total_seconds
    
    def save_recording(self):
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        wave_output_filename = f"recording_{current_time}.wav"
        num_frames = sum(len(frame) for frame in self.frames) // (self.sample_width * self.channels)
        wav_header = self.generate_wav_header(num_frames)

        with open(wave_output_filename, 'wb') as wf:
            wf.write(wav_header)
            for frame in self.frames:
                wf.write(frame)
                
        print(f"File saved as {wave_output_filename}")
        return wave_output_filename
  
'''
if __name__ == "__main__":
    recorder = AudioRecorder()
    recorder.start_recording()
    print("录音开始。按 Ctrl+C 停止录音...")
    try:
        while recorder.is_recording:
            recorder.record()
    except KeyboardInterrupt:
        print("\n录音被用户中断。")
    finally:
        filename = recorder.stop_recording()
        print(recorder.get_total_recording_length())
        if filename:
            print(f"录音已保存到 {filename}")
        else:
            print("录音未能保存。")
'''
