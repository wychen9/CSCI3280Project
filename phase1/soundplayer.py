import simpleaudio as sa
#from pydub import AudioSegment
import numpy as np
import time
from decoder import read_wav
import threading
#多声道？

class AudioPlayer:
    def __init__(self, filename):
        audio = read_wav(filename)
        self.waveData = np.frombuffer(audio['audio_data'], dtype=np.int16)
        self.original_waveData = self.waveData
        self.nchannels = audio['num_channels']
        self.sampwidth = audio['sample_width']
        self.framerate = audio['frame_rate']
        self.speed = 1.0
        #self.is_paused = True
        self.play_obj = None
        self.start_index = 0
        self.start_time = None
        self.elapsed_time_at_speed_change = 0 # 用于记录速度改变时的已经播放的时间
        self.total_length = len(self.waveData) / (self.framerate * self.nchannels)
        self.thread = None
        self.progress_thread = None
        self.stop_progress_update = False
        self.last_progress = "00:00:00"
        self.stop_index = len(self.waveData)/self.nchannels

    #def play(self, start_index=None):
    def play(self, start_percentage=0.0, stop_percentage=100.0):
        # 如果已经有一个线程在运行，先停止它
        if self.thread is not None:
            self.stop_progress_update = True
            self.thread.join()
        if self.play_obj is not None and self.play_obj.is_playing():
            self.play_obj.stop()
            self.play_obj = None

        # 计算开始播放的样本索引
        start_index = int(start_percentage * len(self.waveData) / (100*self.nchannels))
        stop_index = int(stop_percentage * len(self.waveData) / (100*self.nchannels))


        # 计算开始播放的时间并设置为 self.elapsed_time_at_speed_change
        start_seconds = start_percentage * self.total_length / (100 * self.nchannels)
        self.elapsed_time_at_speed_change = start_seconds

        # 将开始播放的时间转换为 HH:MM:SS 格式并设置为 self.last_progress
        hours, remainder = divmod(int(start_seconds), 3600)
        minutes, seconds = divmod(remainder, 60)
        self.last_progress = "{:02}:{:02}:{:02}".format(hours, minutes, seconds)

        if self.speed != 1.0:
            new_framerate = int(self.framerate * self.speed)
        else:
            new_framerate = self.framerate

        self.play_obj = sa.play_buffer(self.waveData[start_index * self.nchannels:stop_index * self.nchannels].tobytes(), self.nchannels, self.sampwidth, new_framerate)

        # 设置开始播放的时间
        #self.start_time = time.time() - start_seconds
        self.start_time = time.time() - start_seconds / self.speed
        self.stop_progress_update = False
        self.thread = threading.Thread(target=self.update_progress)
        self.thread.start()

    def pause(self):
        #self.is_paused = True
        if self.play_obj is not None and self.play_obj.is_playing():
            
            self.play_obj.stop()
            time.sleep(0.1)  # 等待音频停止
            elapsed_time = time.time() - self.start_time
            if self.speed != 1.0:
                new_framerate = int(self.framerate * self.speed)
                #self.waveData = self.original_waveData
            else:
                new_framerate = self.framerate
            elapsed_samples = int(new_framerate * elapsed_time)
            # 确保 start_index 是每个样本的字节数和通道数的倍数
            self.start_index += elapsed_samples - elapsed_samples % self.nchannels
        self.last_progress = self.get_progress()
        #print(f'当前last播放进度：{self.last_progress}/{self.get_total_length()}')
        # while self.play_obj.is_playing():
        #     time.sleep(0.1)
        self.stop_progress_update = True
        if self.progress_thread is not None:
            self.progress_thread.join()
            self.progress_thread = None
        
        

    def resume(self, start_index=None):
        #?self.start_index = int(self.start_index * self.speed)
        #
        hours, minutes, seconds = map(int, self.last_progress.split(':'))
        last_progress_in_seconds = hours * 3600 + minutes * 60 + seconds
        start_percentage = last_progress_in_seconds / self.total_length * 100
        self.play(start_percentage=start_percentage)
        

    def set_speed(self, speed):
        speed = float(speed)
        if self.play_obj is None or not self.play_obj.is_playing():
            self.speed = speed
            #self.play()
        else:
            #self.elapsed_time_at_speed_change += (time.time() - self.start_time) * self.speed
            self.pause()
            # 重新计算 start_index
            #start_index = int(start_index * self.speed)
            self.speed = speed
            self.resume()
            #time.sleep(0.1)
            #self.play()
        #播放时不能改变速度
            
    def get_progress(self):
        if self.play_obj is not None and self.start_time is not None:
            total_elapsed_time = self.elapsed_time_at_speed_change + (time.time() - self.start_time) * self.speed
            minutes, seconds = divmod(total_elapsed_time, 60)
            hours, minutes = divmod(minutes, 60)
            return "{:0>2}:{:0>2}:{:0>2}".format(int(hours), int(minutes), int(seconds))
        else:
            return "00:00:00"

    def get_total_length(self):
        minutes, seconds = divmod(self.total_length, 60)
        hours, minutes = divmod(minutes, 60)
        return "{:0>2}:{:0>2}:{:0>2}".format(int(hours), int(minutes), int(seconds))

    def get_start_length(self):
        start_length = int(self.start_index * self.nchannels * self.total_length / len(self.waveData))
        minutes, seconds = divmod(start_length, 60)
        hours, minutes = divmod(minutes, 60)
        return "{:0>2}:{:0>2}:{:0>2}".format(int(hours), int(minutes), int(seconds))

    def get_stop_length(self):
        stop_length = self.stop_index * self.nchannels * self.total_length / len(self.waveData)
        minutes, seconds = divmod(stop_length, 60)
        hours, minutes = divmod(minutes, 60)
        return "{:0>2}:{:0>2}:{:0>2}".format(int(hours), int(minutes), int(seconds))

    def update_progress(self):
        first_loop = True
        first_progress = None
        while not self.stop_progress_update:
            current_progress = self.get_progress()
            if first_loop:
                first_progress = current_progress
                first_loop = False
            #print(f'当前播放进度：{current_progress}/{self.get_total_length()}')
            time.sleep(1)
            if current_progress >=self.get_stop_length():
                #print(f'当前播放进度：{first_progress}/{self.get_stop_length()}')
                self.stop_index = len(self.waveData)/self.nchannels
                self.stop()
            if current_progress > self.get_total_length():
                #print(f'当前播放进度：00:00:00/{self.get_total_length()}')
                self.stop()
        #print(f'第一次循环的播放进度：{first_progress}/{self.get_total_length()}')
        self.stop_progress_update = True
        

    def stop_progress_thread(self):
        self.stop_progress_update = True
        if self.thread is not None:
            self.thread.join()
            self.thread = None


    def stop(self):
        self.start_index = 0
        self.stop_index = len(self.waveData)/self.nchannels
        if self.play_obj is not None:
            self.play_obj.stop()
            
            self.last_progress = "00:00:00"
            self.stop_progress_update = True
            # 如果当前线程不是更新进度的线程，那么加入它
            if self.thread is not None and threading.current_thread() != self.thread:
                self.thread.join()
                self.thread = None
            
        


#player = AudioPlayer('demo.wav')
#total_length = player.get_total_length()

# def print_progress(player):
#     while player.play_obj is not None and player.play_obj.is_playing():
#         print(f'当前播放进度：{player.get_progress()}/{total_length}')
#         time.sleep(1)
#     print(f'当前播放进度：00:00:00/{total_length}')

# while True:
#     command = input("请输入指令（load/play/pause/resume/speed/progress/stop/quit）：")
#     if command == 'load':
#         path = input('请输入音频文件的路径：')
#         player = AudioPlayer(path)
#         total_length = player.get_total_length()
#     elif command == 'play':
#         player.play(20)
#     elif command == 'pause':
#         player.pause()
#     elif command == 'resume':
#         player.resume()
#     elif command == 'stop':
#         player.stop()
#     elif command == 'speed':
#         speed = float(input('Enter a speed (0.5 to 2.0): '))
#         player.set_speed(speed)
#     elif command == 'quit':
#         player.stop()
#         break
#     else:
#         print("无效的指令，请重新输入。")

