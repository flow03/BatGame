import sys
import os
import json

def resource_path(relative_path):
    try:
    # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def get_num(string):
    num = str()
    for ch in string:
        if ch.isdigit():
            num += ch
        elif num:
            break

    if num.isdigit():
        num = int(num)
        return num
    else:
        return None

def load_json(json_file):
        with open(json_file, 'r', encoding='utf-8-sig') as file: # відкриття файлу з кодуванням UTF-8-BOM
            try:
                loaded_data = json.load(file) # конвертує бінарні дані в текстовий рядок
                # self.jokes.update(loaded_data)
                return loaded_data # dict
            except json.JSONDecodeError as e:
                print(f"Неможливо прочитати JSON з файлу '{json_file}'")
                print(f"Line: {e.lineno}, Column: {e.colno}, {e.msg}")
                print(f"Content: {e.doc.splitlines()[e.lineno - 1]}")
                sys.exit(1) 