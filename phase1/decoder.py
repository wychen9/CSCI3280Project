# decoder.py
import struct
import numpy as np
def read_wav(file_path):
    with open(file_path, 'rb') as f:
        # 读取文件头
        riff, size, fformat = struct.unpack('<4sI4s', f.read(12))
        if riff != b'RIFF' or fformat != b'WAVE':
            raise ValueError('Not a valid WAV file')

        # 初始化音频参数
        audio_format = num_channels = sample_rate = byte_rate = block_align = bits_per_sample = None

        # 读取各个子块
        chunk_header = f.read(8)
        while chunk_header:
            subchunkid, subchunksize = struct.unpack('<4sI', chunk_header)

            if subchunkid == b'fmt ':
                # 读取fmt子块，包含了音频格式、通道数、采样率等信息
                subchunkdata = f.read(subchunksize)
                if subchunksize >= 16:
                    audio_format, num_channels, sample_rate, byte_rate, block_align, bits_per_sample = struct.unpack('<HHIIHH', subchunkdata[:16])
                else:
                    print(f'Warning: fmt chunk size is less than 16 bytes, some information may be missing')
            
            elif subchunkid == b'data':
                # 读取data子块，包含了音频数据
                audio_data = f.read(subchunksize)
                audio_data = np.frombuffer(audio_data, dtype=np.int16)  # 假设音频数据是16位的
                audio_data = audio_data.astype(np.float32) / 32768.0  # 归一化
                return {
                    'audio_data': audio_data,
                    'num_channels': num_channels,
                    'sample_width': bits_per_sample // 8,
                    'frame_rate': sample_rate
                }
            
            """
            elif subchunkid == b'data':
                # 读取data子块，包含了音频数据
                audio_data = f.read(subchunksize)
                return {
                    'audio_data': audio_data,
                    'num_channels': num_channels,
                    'sample_width': bits_per_sample // 8,
                    'frame_rate': sample_rate
                }
"""
            chunk_header = f.read(8)
