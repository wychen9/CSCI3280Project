# decoder.py
import struct

def read_wav(file_path):
    with open(file_path, 'rb') as f:
        riff, size, fformat = struct.unpack('<4sI4s', f.read(12))
        if riff != b'RIFF' or fformat != b'WAVE':
            raise ValueError('Not a valid WAV file')

        audio_format = num_channels = sample_rate = byte_rate = block_align = bits_per_sample = None

        chunk_header = f.read(8)
        while chunk_header:
            subchunkid, subchunksize = struct.unpack('<4sI', chunk_header)

            if subchunkid == b'fmt ':
                subchunkdata = f.read(subchunksize)
                if subchunksize >= 16:
                    audio_format, num_channels, sample_rate, byte_rate, block_align, bits_per_sample = struct.unpack('<HHIIHH', subchunkdata[:16])
                else:
                    print(f'Warning: fmt chunk size is less than 16 bytes, some information may be missing')

            elif subchunkid == b'data':
                audio_data = f.read(subchunksize)
                return {
                    'audio_data': audio_data,
                    'num_channels': num_channels,
                    'sample_width': bits_per_sample // 8,
                    'frame_rate': sample_rate
                }

            chunk_header = f.read(8)
