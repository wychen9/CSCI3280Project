import speech_recognition as sr

def speech2text(path):
    # path - string, path for .wav file
    # 
    # return - string, processing result of speech to text
    r = sr.Recognizer()
    file = sr.AudioFile(path)
    with file as source:
        audio = r.record(source)
    print('start converting...')
    text = (r.recognize_google(audio))
    print('conversion finished')
    return text

## Sample usage
# filePath = "./audioFile/harvard_list1.wav"
# ret = speech2text(filePath)
# print(ret)
# print(type(ret))