import keyboard
from pywinauto.application import Application

def hotkey_music(key):
    app = Application(backend="uia").connect(title_re=".*Яндекс.*", found_index=0)
    app.window(title_re=".*Яндекс.*").set_focus()
    keyboard.send(key)