# Arquivo principal

# Assistente online!
'''
import speech_recognition as sr

# Criar um reconhecedor de voz
r = sr.Recognizer()

# Abrir o microfone para capturar áudio
with sr.Microphone() as source:
    while True:
        # Definir microfone como fonte de áudio
        audio = r.listen(source)
        print(r.recognize_google(audio, language='pt'))
'''

# Assistente offline!
#!/usr/bin/env python3

#Pacotes de captura de voz e reconhecimento de fala
import pyaudio
from vosk import Model, KaldiRecognizer

#Pacotes para resposta, em áudio, da assistente
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play

#Pacotes de funções secundárias
import platform
from time import sleep
from os import system, path



#Identificação de sistema operacional
sistema = platform.system()

#Configurações do vosk
model_path = f"{path.abspath(path.dirname(__file__))}\\vosk-model-small-pt-pf\\vosk-model-small-pt-0.3"

model = Model(model_path)
rec = KaldiRecognizer(model, 16000)

#Configurações do PyAudio
p = pyaudio.PyAudio()
rate = 16000
frames_per_buffer =  16384

stream = p.open(format=pyaudio.paInt16, channels=1, rate=rate, input=True, frames_per_buffer=frames_per_buffer)
stream.start_stream()

#Função de fala usando gtts e pydub
def speak(frase):
    
    language = 'pt'
    file_name = 'gtts1.wav'

    gtts_object = gTTS(text = frase, 
                    lang = language, 
                    slow = False)
    gtts_object.save(file_name)

    audio = AudioSegment.from_mp3(file_name)
    play(audio)

    if(sistema == "Windows"):
        system(f"del {file_name}")
    else:
        system(f"rm {file_name}")

    sleep(0.5)

while True:

    data = stream.read(6000, exception_on_overflow=False)

    if len(data) == 0:
        break
    if rec.AcceptWaveform(data):
        #Recorta os excessos da string de fala e a armazena
        string = str(rec.Result()[14:-3])

        #Respostas padrão
        if(string == ""):
            continue
        elif(string.lower() == "hora de dormir"):
            speak("Mas já? Tudo bem, até mais!")
            break
        elif("diga seu nome" in string.lower() or 
             string.lower() == "quem é você"):
            speak("Eu sou sexta feira. Prazer!")
        elif(string.lower() == "qual o nome do seu chefe" or
             string.lower() == "qual o nome de seu chefe"):
            speak("Jonathas. Mas não diga que eu contei, ele é tímido!")
        else:
            print(string)
            speak(f"Você disse {string}")
