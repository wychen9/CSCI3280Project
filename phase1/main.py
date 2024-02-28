import audioop
import wave
import struct
import pyaudio
from datetime import datetime

# Audio format parameters
FORMAT = pyaudio.paInt16
CHANNELS = 1
SAMPLE_WIDTH = pyaudio.PyAudio().get_sample_size(FORMAT)
FRAME_RATE = 44100
# FRAME_RATE = 8000 # for samples in audio file
CHUNK = 1024
RECORD_SECONDS = 5

def generate_wav_header(sample_rate, bits_per_sample, channels, num_frames):
    byte_rate = sample_rate * channels * bits_per_sample // 8
    block_align = channels * bits_per_sample // 8
    subchunk2_size = num_frames * channels * bits_per_sample // 8
    
    # 'RIFF' chunk descriptor
    riff_chunk = struct.pack('<4sI4s', b'RIFF', 36 + subchunk2_size, b'WAVE')
    
    # 'fmt ' sub-chunk
    fmt_chunk = struct.pack('<4sIHHIIHH',
                            b'fmt ',
                            16,  # Subchunk1Size
                            1,   # AudioFormat (1 for PCM)
                            channels,
                            sample_rate,
                            byte_rate,
                            block_align,
                            bits_per_sample)
    
    # 'data' sub-chunk
    data_chunk_header = struct.pack('<4sI', b'data', subchunk2_size)
    
    return riff_chunk + fmt_chunk + data_chunk_header

def record_audio():
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    wave_output_filename = f"recording_{current_time}.wav"

    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=FRAME_RATE, input=True,
                        frames_per_buffer=CHUNK)

    print("Recording...")
    frames = []
    for _ in range(0, int(FRAME_RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    print("Finished recording.")

    stream.stop_stream()
    stream.close()
    audio.terminate()

    num_frames = len(frames) * CHUNK
    wav_header = generate_wav_header(FRAME_RATE, SAMPLE_WIDTH * 8, CHANNELS, num_frames)

    with open(wave_output_filename, 'wb') as wf:
        wf.write(wav_header)
        for frame in frames:
            wf.write(frame)

    print(f"File saved as {wave_output_filename}")

if __name__ == "__main__":
    record_audio()
