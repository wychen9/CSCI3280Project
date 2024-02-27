# * modify the start and end times of the audio.
# * Capability of overwriting a section of audio with fresh recordings.
# To facilitate the cutting process, you should provide a seekbar with a slider, allowing users to quickly navigate through the audio.
import wave
import pyaudio
import os
from main import FORMAT, CHANNELS, SAMPLE_WIDTH,FRAME_RATE,CHUNK

def audioTrim(start, end, wav, path):
    # start - new start time(second) of the audio
    # end - new end time(second) of the audio
    # wav - original wav file
    #
    # new audio file will overwrite the original one
    channelCnt = wav.getnchannels()
    sampleWidth = wav.getsampwidth()
    frameRate = wav.getframerate()
    wav.setpos(int(start*frameRate))
    newAudio = wav.readframes(int(end+1-start)*frameRate)

    with wave.open(path,'wb') as output:
        output.setnchannels(channelCnt)
        output.setsampwidth(sampleWidth)
        output.setframerate(frameRate)
        output.setnframes(int(len(newAudio)/sampleWidth))
        output.writeframes(newAudio)

def overwrite(start, end, wav, path):
    # start - start time(second) of the target section that will be overwritten
    # end -  end time(second) of the target section that will be overwritten
    # wav - path of the original audio file
    # newSec - audio section that will be used to substitute the original one
    #
    # return - none
    # new audio file will overwrite the original one

    duration = end+1 - start
    # Initialize the audio stream
    audio = pyaudio.PyAudio()
    # print("----------------------record device list---------------------")
    # info = audio.get_host_api_info_by_index(0)
    # numdevices = info.get('deviceCount')
    # for i in range(0, numdevices):
    #         if (audio.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
    #             print("Input Device id ", i, " - ", audio.get_device_info_by_host_api_device_index(0, i).get('name'))

    # print("-------------------------------------------------------------")

    index = 3
    print("recording via index "+str(index))
    stream = audio.open(format=FORMAT, channels=CHANNELS,
            rate=FRAME_RATE, input=True,input_device_index = index,
            frames_per_buffer=CHUNK)
    print("Recording...")
    # record new section
    frames = []
    for i in range(0, int(FRAME_RATE / CHUNK * duration)):
        data = stream.read(CHUNK)
        frames.append(data)
    print("Finished recording.")
    stream.stop_stream()
    stream.close()
    audio.terminate()
    
    channelCnt = wav.getnchannels()
    sampleWidth = wav.getsampwidth()
    frameRate = wav.getframerate()
    print("original frame rate: " + str(frameRate))

    tempPath = './audioFile/temp.wav'
    with wave.open(tempPath, 'wb') as tempOutput:
        tempOutput.setnchannels(channelCnt)
        tempOutput.setsampwidth(sampleWidth)
        tempOutput.setframerate(frameRate)
        for frame in frames:
            tempOutput.writeframes(frame)

    print("original frames: " + str(wav.getnframes()))

    newSec = wave.open(tempPath, 'rb')
    print("new section frames: " + str(newSec.getnframes()))
    frameRate = wav.getframerate()

    wav.setpos(0)
    head = wav.readframes(int(start*frameRate))
    
    if(newSec.getnframes()>wav.getnframes()-int(start*frameRate)):
        tail = None
    else:
        wav.setpos(int(end*frameRate))
        tail = wav.readframes(int(wav.getnframes() - end*frameRate))

    middle = newSec.readframes(newSec.getnframes())
    with wave.open(path,'wb') as output:
        output.setnchannels(channelCnt)
        output.setsampwidth(sampleWidth)
        output.setframerate(frameRate)
        if(tail!=None):
            output.setnframes(int(len(head)/sampleWidth)+int(len(middle)/sampleWidth)+int(len(tail)/sampleWidth))
        else:
            output.setnframes(int(len(head)/sampleWidth)+int(len(middle)/sampleWidth))

        output.writeframes(head)
        output.writeframes(middle)
        if(tail!=None): output.writeframes(tail)
    os.remove(tempPath)

# # Sample usage:
# with wave.open('./audioFile/harvard_list1.wav','rb') as inputWav:
#     audioTrim(1,5,inputWav,'./audioFile/harvard1_trim.wav')
#     overwrite(3,5,inputWav,'./audioFile/harvard1_overwrite.wav')