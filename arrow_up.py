import ctypes
import time

# Константы
INPUT_KEYBOARD = 1
KEYEVENTF_KEYUP = 0x0002
VK_DOWN = 0x28  # стрелка вниз

# Структуры
class KEYBDINPUT(ctypes.Structure):
    _fields_ = [
        ("wVk", ctypes.c_ushort),
        ("wScan", ctypes.c_ushort),
        ("dwFlags", ctypes.c_ulong),
        ("time", ctypes.c_ulong),
        ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong))
    ]

class INPUT(ctypes.Structure):
    class _INPUT(ctypes.Union):
        _fields_ = [("ki", KEYBDINPUT)]
    _anonymous_ = ("_input",)
    _fields_ = [
        ("type", ctypes.c_ulong),
        ("_input", _INPUT)
    ]

def press_vk(vk_code):
    extra = ctypes.c_ulong(0)

    # Нажатие клавиши
    ki_down = KEYBDINPUT(
        wVk=vk_code,
        wScan=0,
        dwFlags=0,
        time=0,
        dwExtraInfo=ctypes.pointer(extra)
    )
    input_down = INPUT(type=INPUT_KEYBOARD, ki=ki_down)
    ctypes.windll.user32.SendInput(1, ctypes.byref(input_down), ctypes.sizeof(INPUT))

    time.sleep(0.05)

    # Отпускание клавиши
    ki_up = KEYBDINPUT(
        wVk=vk_code,
        wScan=0,
        dwFlags=KEYEVENTF_KEYUP,
        time=0,
        dwExtraInfo=ctypes.pointer(extra)
    )
    input_up = INPUT(type=INPUT_KEYBOARD, ki=ki_up)
    ctypes.windll.user32.SendInput(1, ctypes.byref(input_up), ctypes.sizeof(INPUT))

# ▶ Нажать стрелку вниз
#press_vk(0x28)
