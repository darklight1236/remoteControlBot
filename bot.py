import time
import telebot
import os
from telebot.apihelper import download_file

import pygame
import wave
import speech_recognition as sr
import numpy as np

import mss
from PIL import Image

import webbrowser
import subprocess
import keyboard

from CONFIG import *
from find_app import open_exe
#from hotkey_music import hotkey_music


voice_text = None

bot = telebot.TeleBot(token_bot)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Дарова, я тупой как воробушек, но ты не паникуй раньше времени, а то я сам паниковать начинаю")

@bot.message_handler(content_types=["voice"])
def test(message):
    file_info = bot.get_file(message.voice.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(f'voice.ogg', 'wb') as new_file:
        new_file.write(downloaded_file)
        print(new_file)

    # try to convert from .ogg to .wav
    pygame.mixer.init()
    sound = pygame.mixer.Sound("voice.ogg")
    samples = pygame.sndarray.array(sound)

    with wave.open("output.wav", "wb") as wf:
        wf.setnchannels(2)  # стерео
        wf.setsampwidth(2)  # 16 бит (2 байта)
        wf.setframerate(44100)
        wf.writeframes(samples.astype(np.int16).tobytes())

    # try to write voice in text
    recognizer = sr.Recognizer()
    with sr.AudioFile("output.wav") as source:
        audio_data = recognizer.record(source)
        global voice_text
        voice_text = recognizer.recognize_google(audio_data, language="ru-RU")  # для русского
        voice_text = voice_text.lower()
        print("Распознанный текст:", voice_text)
        bot.reply_to(message, voice_text)

    if voice_text == "сделай скриншот":
        with mss.mss() as sct:
            monitor = sct.monitors[1]  # left monitor (0 - screenshot of full desktop)
            monitor2 = sct.monitors[2]  # right monitor
            screenshot = sct.grab(monitor)
            screenshot2 = sct.grab(monitor2)
            img = Image.frombytes("RGB", screenshot.size, screenshot.rgb)
            img2 = Image.frombytes("RGB", screenshot2.size, screenshot2.rgb)
            img.save("screenshot.png")
            img2.save("screenshot.png")

            bot.send_photo(message.chat.id, img)
            bot.send_photo(message.chat.id, img2)

    elif voice_text == "открой браузер":
        webbrowser.open("https://www.google.com")

    elif voice_text == "открой youtube":
        webbrowser.open("https://www.youtube.com/")

    elif voice_text == "открой вк":
        webbrowser.open("https://vk.com/im")

    elif voice_text == "открой чат gpt":
        webbrowser.open("https://chatgpt.com/")

    elif voice_text == "открой deep seek":
        webbrowser.open("https://chat.deepseek.com/")

    elif voice_text == "открой яндекс почту":
        webbrowser.open("https://mail.yandex.ru/")

    elif voice_text == "открой google почту":
        webbrowser.open("https://mail.google.com/mail/")

    elif voice_text == "открой панель управления vpn":
        webbrowser.open("http://185.87.151.145:65000/")

    elif voice_text == "открой vpn хостинг":
        webbrowser.open("https://my.ishosting.com/ru/vps")

    elif voice_text == "открой будильник":
        webbrowser.open("https://onlinealarmkur.com/ru/")

    elif voice_text == "открой доту" or voice_text == "открой dota":
        subprocess.Popen(["start", "steam://rungameid/570"], shell=True)

    elif voice_text == "открой яндекс музыку":
        open_exe("Яндекс Музыка.exe")


    elif voice_text == "следующий трек":
        #hotkey_music('n')
        pass

    elif voice_text == "предыдущий трек":
        #hotkey_music('p')
        pass

    #not work
    #elif voice_text == "прибавь громкость":
    #    app = Application(backend="uia").connect(title_re=".*Яндекс.*", found_index=0)
    #    app.window(title_re=".*Яндекс.*").set_focus()
    #    press_vk(0x26)

    # not work
    #elif voice_text == "убавь громкость":
    #    app = Application(backend="uia").connect(title_re=".*Яндекс.*", found_index=0)
    #    app.window(title_re=".*Яндекс.*").set_focus()
    #    press_vk(0x26)

    elif voice_text == "останови музыку" or voice_text == "включи музыку":
        keyboard.send("play/pause media")


    elif voice_text == "открой discord" or voice_text == "открой дискорд":
        open_exe("Discord.exe")



#music turn on/off
#music value plus/minus


bot.infinity_polling()