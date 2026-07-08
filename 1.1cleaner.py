import os
import shutil
import ctypes
import sys
from pathlib import Path

ASCII_MS = r"""
    ____  __    ____     ________                              ____              __  ________
   / __ \/ /_  / __ \   / ____/ /__  ____ _____  ___  _____   / __/___  _____   /  |/  / ___/
  / / / / __ \/ / / /  / /   / / _ \/ __ `/ __ \/ _ \/ ___/  / /_/ __ \/ ___/  / /|_/ /\__ \ 
 / /_/ / /_/ / /_/ /  / /___/ /  __/ /_/ / / / /  __/ /     / __/ /_/ / /     / /  / /___/ / 
/_____/_.___/_____/   \____/_/\___/\__,_/_/ /_/\___/_/     /_/  \____/_/     /_/  /_//____/  
"""

def get_texts(lang):
    if lang == "ru":
        return {
            "title": "=== DBD ACCOUNT CLEANER ===",
            "choose_lang": "Выберите язык / Choose language",
            "ru": "1) Русский",
            "en": "2) English",
            "save_data": "Сохранить выбор? [Y/N]",
            "main_menu": "\n=== ГЛАВНОЕ МЕНЮ ===",
            "start_clean": "1) > Start Cleaner - запустить очистку",
            "change_language": "2) > Сменить язык",
            "exit": "3) > Exit",
            "choose_type": "Выбери тип очистки:",
            "full_clean": "1) > Полная чистка (Microsoft Store / Xbox + DBD). Рекомендуется для HWID / лицензионных банов.",
            "xbox_only": "2) > Очистка только Xbox профиля (не трогает Microsoft Store данные).",
            "clean_complete": "✅ Очистка успешно завершена!",
            "goodbye": "До свидания! / Goodbye!",
            "invalid": "Неверный выбор! / Invalid choice!",
            "language_changed": "Язык успешно изменён!"
        }
    else:
        return {
            "title": "=== DBD ACCOUNT CLEANER ===",
            "choose_lang": "Choose language",
            "ru": "1) Russian",
            "en": "2) English",
            "save_data": "Save selection? [Y/N]",
            "main_menu": "\n=== MAIN MENU ===",
            "start_clean": "1) > Start Cleaner",
            "change_language": "2) > Change Language",
            "exit": "3) > Exit",
            "choose_type": "Choose cleanup type:",
            "full_clean": "1) > Full Cleanup (Microsoft Store / Xbox + DBD). Helps with HWID and license bans.",
            "xbox_only": "2) > Xbox Profile Cleanup only (doesn't touch Microsoft Store data).",
            "clean_complete": "✅ Cleanup completed successfully!",
            "goodbye": "Goodbye!",
            "invalid": "Invalid choice!",
            "language_changed": "Language changed successfully!"
        }

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def save_settings(language):
    try:
        with open("save_info.txt", "w", encoding="utf-8") as f:
            f.write(f"language={language}\n")
            f.write("platform=Microsoft Store\n")
    except:
        pass

def load_settings():
    if not os.path.exists("save_info.txt"):
        return None
    try:
        lang = "ru"
        with open("save_info.txt", "r", encoding="utf-8") as f:
            for line in f:
                if "=" in line:
                    key, value = line.strip().split("=", 1)
                    if key == "language":
                        lang = value
        return lang
    except:
        return None

def clean_paths():
    texts = get_texts("ru")
    clear_console()
    
    print(texts["choose_type"])
    print(texts["full_clean"])
    print(texts["xbox_only"])
    clean_choice = input("\nВаш выбор: ").strip()
    is_full = clean_choice == "1"

    print("\n" + "="*80)
    print("ЗАПУСК ОЧИСТКИ ДЛЯ MICROSOFT STORE / XBOX...")
    print("="*80 + "\n")

    paths = [
        (r"%APPDATA%\Xbox", "Xbox"),
        (r"%LOCALAPPDATA%\Xbox", "Xbox Local"),
        (r"%LOCALAPPDATA%\Microsoft\XboxLive", "XboxLive"),
        (r"%LOCALAPPDATA%\Microsoft\Windows\GameServices", "GameServices"),
        (r"%LOCALAPPDATA%\Microsoft\GameCache", "GameCache"),
        (r"%LOCALAPPDATA%\Packages\Microsoft.XboxIdentityProvider_8wekyb3d8bbwe", "Xbox Identity"),
        (r"%LOCALAPPDATA%\Packages\Microsoft.XboxApp_8wekyb3d8bbwe", "Xbox App"),
        (r"%LOCALAPPDATA%\Packages\Microsoft.XboxGamingOverlay_8wekyb3d8bbwe", "Xbox Gaming Overlay"),
        (r"%LOCALAPPDATA%\Packages\Microsoft.WindowsStore_8wekyb3d8bbwe", "Windows Store Cache"),
        (r"%LOCALAPPDATA%\Microsoft\CLR_v4.0", "CLR Cache"),
        (r"%LOCALAPPDATA%\Temp", "Temp"),
        (r"%LOCALAPPDATA%\Microsoft\Windows\INetCache", "Internet Cache"),
        (r"%APPDATA%\Microsoft\Windows\Recent", "Recent Files"),
        (r"%LOCALAPPDATA%\DeadByDaylight", "DBD Local Data"),
        (r"%LOCALAPPDATA%\BHVR", "BHVR"),
        (r"%APPDATA%\DeadByDaylight", "DBD AppData"),
        (r"%LOCALAPPDATA%\Packages\DeadByDaylight*", "DBD UWP Packages"),
        (r"C:\XboxGames", "XboxGames C:"),
        (r"D:\XboxGames", "XboxGames D:"),
        (r"E:\XboxGames", "XboxGames E:"),
        (r"F:\XboxGames", "XboxGames F:"),
        (r"G:\XboxGames", "XboxGames G:"),
    ]

    cleaned_count = 0
    for p, desc in paths:
        try:
            expanded = os.path.expandvars(p)
            if "*" in expanded:
                parent = Path(expanded).parent
                if parent.exists():
                    for item in parent.glob(Path(expanded).name):
                        if item.exists():
                            print(f"[+] Cleaning: {desc} -> {item.name}")
                            shutil.rmtree(item, ignore_errors=True)
                            cleaned_count += 1
            else:
                path = Path(expanded)
                if path.exists():
                    print(f"[+] Cleaning: {desc}")
                    shutil.rmtree(path, ignore_errors=True)
                    cleaned_count += 1
        except Exception as e:
            pass

    if is_full:
        print("[+] Запуск wsreset.exe (очистка Microsoft Store)...")
        os.system("wsreset.exe")
        print("[+] Дополнительная очистка кэша Xbox Services...")
        try:
            os.system("powershell -Command \"Get-AppxPackage *Xbox* | ForEach {Add-AppxPackage -DisableDevelopmentMode -Register '$($_.InstallLocation)\\AppXManifest.xml'}\"")
        except:
            pass

    print(f"\n[+] Очищено {cleaned_count} директорий/кэшей.")
    print("\n" + texts["clean_complete"])
    input("\nНажмите Enter для возврата в меню...")

def main():
    if not is_admin():
        print("⚠️ Рекомендуется запуск от имени администратора!")

    lang = load_settings()

    if lang is None:
        clear_console()
        print(get_texts("ru")["choose_lang"] + "\n")
        print("1) Русский")
        print("2) English")
        lang_choice = input("\nВаш выбор / Your choice: ").strip()
        lang = "ru" if lang_choice == "1" else "en"

        save_choice = input(f"\n{get_texts(lang)['save_data']} ").strip().upper()
        if save_choice in ["Y", "YES", "ДА"]:
            save_settings(lang)

    texts = get_texts(lang)

    while True:
        clear_console()
        print(ASCII_MS)
        print(texts["title"])
        print(texts["main_menu"])
        print(texts["start_clean"])
        print(texts["change_language"])
        print(texts["exit"])
        
        choice = input("\nВыберите опцию / Select option: ").strip()

        if choice == "1":
            clean_paths()
        elif choice == "2":
            lang = change_language()
            texts = get_texts(lang)
            save_settings(lang)
            print(texts["language_changed"])
            input("Нажмите Enter...")
        elif choice == "3":
            print("\n" + texts["goodbye"])
            break
        else:
            print(texts.get("invalid", "Неверный выбор!"))
            input("Нажмите Enter...")

def change_language():
    clear_console()
    print("Выберите язык / Choose language\n")
    print("1) Русский")
    print("2) English")
    choice = input("\nВаш выбор: ").strip()
    return "ru" if choice == "1" else "en"

if __name__ == "__main__":
    main()
