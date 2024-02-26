import speech_recognition as sr

def speech2text(path):
    # path - string, path for .wav file
    # 
    # return - string, processing result of speech to text
    r = sr.Recognizer()
    file = sr.AudioFile(path)
    with file as source:
        audio = r.record(source)
    return(r.recognize_google(audio))

## Sample usage
# filePath = "./audioFile/harvard.wav"
# ret = speech2text(filePath)
# print(ret)
# print(type(ret))