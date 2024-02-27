# * modify the start and end times of the audio.
# * Capability of overwriting a section of audio with fresh recordings.
# To facilitate the cutting process, you should provide a seekbar with a slider, allowing users to quickly navigate through the audio.
import wave
import pyaudio
import os
from recording import Recording
from main import FORMAT, CHANNELS,FRAME_RATE,CHUNK

def audioTrim(start, end, wavRecording):
    # start - new start time(second) of the audio
    # end - new end time(second) of the audio
    # wavRecording - Recording object of original wav file
    #
    # no return, new audio file will overwrite the original one
    with wave.open(wavRecording.path, 'rb') as wav:
        channelCnt = wav.getnchannels()
        sampleWidth = wav.getsampwidth()
        frameRate = wav.getframerate()
        wav.setpos(int(start*frameRate))
        newAudio = wav.readframes(int(end+1-start)*frameRate)

    with wave.open(wavRecording.path,'wb') as output:
        output.setnchannels(channelCnt)
        output.setsampwidth(sampleWidth)
        output.setframerate(frameRate)
        output.setnframes(int(len(newAudio)/sampleWidth))
        output.writeframes(newAudio)

def overwrite(start, end, wavRecording, tempRecording):
    # start - start time(second) of the target section that will be overwritten
    # end -  end time(second) of the target section that will be overwritten
    # wavRecording - Recording object of the original audio file
    # tempRecording - Recording object of the audio segment which will be used to substitute the original segment
    #
    # return - none
    # new audio file will overwrite the original one
    
    with wave.open(wavRecording.path, 'rb') as wav:
        channelCnt = wav.getnchannels()
        sampleWidth = wav.getsampwidth()
        frameRate = wav.getframerate()
        wav.setpos(0)
        head = wav.readframes(int(start*frameRate))

        with wave.open(tempRecording.path, 'rb') as newSec:
            if(newSec.getnframes()>wav.getnframes()-int(start*frameRate)):
                tail = None
            else:
                wav.setpos(int(end*frameRate))
                tail = wav.readframes(int(wav.getnframes() - end*frameRate))
            middle = newSec.readframes(newSec.getnframes())

    with wave.open(wavRecording.path,'wb') as output:
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
    os.remove(tempRecording.path)

def _tempRecord(start, end, wavRecording):
    duration = end+1 - start
    # Initialize the audio stream
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS,
            rate=FRAME_RATE, input=True,
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
    
    wav = wave.open(wavRecording.path, 'rb')
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
    return Recording('temp', '','','','./audioFile/temp.wav')

## Sample usage:
# wavRecording1 = Recording('list1', '','','','./audioFile/harvard_list1.wav')
# wavRecording2 = Recording('list2', '','','','./audioFile/harvard_list2.wav')
# tempRecording = _tempRecord(3, 5, wavRecording2)
# audioTrim(1,5,wavRecording1)
# overwrite(3,5,wavRecording2,tempRecording)