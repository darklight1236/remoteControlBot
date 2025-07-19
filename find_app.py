import os
import subprocess

def find_app(root_dir, app_name):
    for dirpath, dirnames, filenames in os.walk(root_dir):
        if app_name in filenames:
            return os.path.join(dirpath, app_name)
    return None

def open_exe(app):
    app_path = find_app("C:\\", app)
    app_path2 = find_app("D:\\", app)
    if app_path:
        subprocess.Popen([app_path])
    elif app_path2:
        subprocess.Popen([app_path2])
    else:
        print("Приложение не найдено")