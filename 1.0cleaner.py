import os
import shutil
import ctypes
import sys
from pathlib import Path

ASCII_MS = r"""
         ____  __    ____     ________                              ____              __  ________
        / __ \/ /_  / __ \   / ____/ / _  ____ _____  ___  _____   / __/___  _____   /  |/  / ___/
       / / / / __ \/ / / /  / /   / / _ \/ __ `/ __ \/ _ \/ ___/  / /_/ __ \/ ___/  / /|_/ /\__ \ 
      / /_/ / /_/ / /_/ /  / /___/ /  __/ /_/ / / / /  __/ /     / __/ /_/ / /     / /  / /___/ / 
     /_____/_.___/_____/   \____/_/\___/\__,_/_/ /_/\___/_/     /_/  \____/_/     /_/  /_//____/  
"""

ASCII_STEAM = r"""
         ____  __    ____     ________                              ____              _____ __                     
        / __ \/ /_  / __ \   / ____/ /__  ____ _____  ___  _____   / __/___  _____   / ___// /____  ____ _____ ___ 
       / / / / __ \/ / / /  / /   / / _ \/ __ `/ __ \/ _ \/ ___/  / /_/ __ \/ ___/   \__ \/ __/ _ \/ __ `/ __ `__ \
      / /_/ / /_/ / /_/ /  / /___/ /  __/ /_/ / / / /  __/ /     / __/ /_/ / /      ___/ / /_/  __/ /_/ / / / / / /
     /_____/_.___/_____/   \____/_/\___/\__,_/_/ /_/\___/_/     /_/  \____/_/      /____/\__/\___/\__,_/_/ /_/ /_/ 
"""

ASCII_EPIC = r"""
         ____  __    ____     ________                              ____              _________________
        / __ \/ /_  / __ \   / ____/ /__  ____ _____  ___  _____   / __/___  _____   / ____/ ____/ ___/
       / / / / __ \/ / / /  / /   / / _ \/ __ `/ __ \/ _ \/ ___/  / /_/ __ \/ ___/  / __/ / / __ \__ \ 
      / /_/ / /_/ / /_/ /  / /___/ /  __/ /_/ / / / /  __/ /     / __/ /_/ / /     / /___/ /_/ /___/ / 
     /_____/_.___/_____/   \____/_/\___/\__,_/_/ /_/\___/_/     /_/  \____/_/     /_____/\____//____/  
"""

def get_texts(lang):
    if lang == "ru":
        return {
            "title": "=== DBD CLEANER ===",
            "choose_lang": "Выберите язык / Choose language",
            "ru": "1) Русский",
            "en": "2) English",
            "choose_platform": "Выберите вашу платформу:",
            "steam": "1) > Steam",
            "epic": "2) > Epic Games",
            "ms": "3) > Microsoft Store",
            "save_data": "Сохранить выбор? [Y/N]",
            "main_menu": "\n=== ГЛАВНОЕ МЕНЮ ===",
            "start_clean": "1) > Start Cleaner - запустить очистку",
            "information": "2) > Information",
            "change_platform": "3) > Change Platform",
            "exit": "4) > Exit",
            "choose_type": "Выбери тип очистки:",
            "full_clean": "1) > Полная чистка. (Очищает все от Microsoft Store / Xbox, поможет от бана по железу и бана лицензии.)",
            "xbox_only": "2) > Очистка Xbox профиля. (Очищает всё от Xbox не трогая данные Microsoft Store.)",
            "clean_complete": "✅ Очистка успешно завершена!",
            "goodbye": "До свидания! / Goodbye!",
            "invalid": "Неверный выбор! / Invalid choice!",
            "platform_changed": "Платформа успешно изменена!",
            "language_changed": "Язык успешно изменён!"
        }
    else:
        return {
            "title": "=== DBD CLEANER ===",
            "choose_lang": "Choose language",
            "ru": "1) Russian",
            "en": "2) English",
            "choose_platform": "Choose your platform:",
            "steam": "1) > Steam",
            "epic": "2) > Epic Games",
            "ms": "3) > Microsoft Store",
            "save_data": "Save selection? [Y/N]",
            "main_menu": "\n=== MAIN MENU ===",
            "start_clean": "1) > Start Cleaner",
            "information": "2) > Information",
            "change_platform": "3) > Change Platform",
            "exit": "4) > Exit",
            "choose_type": "Choose cleanup type:",
            "full_clean": "1) > Full Cleanup. (Cleans everything from Microsoft Store / Xbox, helps with HWID and license bans.)",
            "xbox_only": "2) > Xbox Profile Cleanup. (Cleans only Xbox data without touching Microsoft Store.)",
            "clean_complete": "✅ Cleanup completed successfully!",
            "goodbye": "Goodbye!",
            "invalid": "Invalid choice!",
            "platform_changed": "Platform changed successfully!",
            "language_changed": "Language changed successfully!"
        }

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def save_settings(language, platform):
    try:
        with open("save_info.txt", "w", encoding="utf-8") as f:
            f.write(f"language={language}\n")
            f.write(f"platform={platform}\n")
    except:
        pass

def load_settings():
    if not os.path.exists("save_info.txt"):
        return None, None
    try:
        lang = "ru"
        platform = "Microsoft Store"
        with open("save_info.txt", "r", encoding="utf-8") as f:
            for line in f:
                if "=" in line:
                    key, value = line.strip().split("=", 1)
                    if key == "language":
                        lang = value
                    elif key == "platform":
                        platform = value
        return lang, platform
    except:
        return None, None

def clean_paths(platform, lang="ru"):
    texts = get_texts(lang)
    clear_console()
    
    if platform == "Microsoft Store":
        print(texts["choose_type"])
        print(texts["full_clean"])
        print(texts["xbox_only"])
        clean_choice = input("\nВаш выбор: ").strip()
        is_full = clean_choice == "1"
    else:
        is_full = True

    print("\n" + "="*70)
    print(f"ЗАПУСК ОЧИСТКИ ДЛЯ {platform.upper()}...")
    print("="*70 + "\n")

    paths = [
        (r"%APPDATA%\Xbox", "Xbox"),
        (r"%LOCALAPPDATA%\Xbox", "Xbox Local"),
        (r"%LOCALAPPDATA%\Microsoft\XboxLive", "XboxLive"),
        (r"%LOCALAPPDATA%\Microsoft\Windows\GameServices", "GameServices"),
        (r"%LOCALAPPDATA%\Microsoft\GameCache", "GameCache"),
        (r"%LOCALAPPDATA%\Temp", "Temp"),
        (r"C:\XboxGames", "XboxGames C:"),
        (r"D:\XboxGames", "XboxGames D:"),
        (r"E:\XboxGames", "XboxGames E:"),
    ]

    for p, desc in paths:
        try:
            path = Path(os.path.expandvars(p))
            if path.exists():
                print(f"[+] Cleaning: {desc}")
                shutil.rmtree(path, ignore_errors=True)
        except:
            pass

    if platform == "Microsoft Store" and is_full:
        print("[+] Запуск wsreset.exe...")
        os.system("wsreset.exe")

    if platform == "Steam":
        print("[+] Очистка Steam...")
        steam_folders = ["appcache", "depotcache", "htmlcache", "steamapps/downloading", "steamapps/temp", "steamapps/workshop"]
        steam_paths = [rf"%ProgramFiles(x86)%\Steam\{folder}" for folder in steam_folders]
        steam_paths.extend([r"%LOCALAPPDATA%\Steam", r"%APPDATA%\Steam"])
        for p_str in steam_paths:
            try:
                p = Path(os.path.expandvars(p_str))
                if p.exists():
                    shutil.rmtree(p, ignore_errors=True)
                    print(f"    → {p.name if hasattr(p, 'name') else p_str.split('\\')[-1]} очищен")
            except:
                pass

    if platform == "Epic Games":
        print("[+] Очистка Epic Games...")
        epic_folders = [
            r"%LOCALAPPDATA%\EpicGamesLauncher",
            r"%LOCALAPPDATA%\Epic Games",
            r"%LOCALAPPDATA%\UnrealEngine",
            r"%APPDATA%\Epic",
            r"%ProgramData%\Epic"
        ]
        for p_str in epic_folders:
            try:
                p = Path(os.path.expandvars(p_str))
                if p.exists():
                    shutil.rmtree(p, ignore_errors=True)
                    print(f"    → {p.name} очищен")
            except:
                pass

    print("\n" + texts["clean_complete"])
    input("\nНажмите Enter для возврата в меню...")

def main():
    if not is_admin():
        print("⚠️ Рекомендуется запуск от имени администратора!")

    lang, platform = load_settings()

    if lang is None or platform is None:
        clear_console()
        print(get_texts("ru")["choose_lang"] + "\n")
        print("1) Русский")
        print("2) English")
        lang_choice = input("\nВаш выбор / Your choice: ").strip()
        lang = "ru" if lang_choice == "1" else "en"

        texts = get_texts(lang)

        while True:
            clear_console()
            print(texts["choose_platform"] + "\n")
            print(texts["steam"])
            print(texts["epic"])
            print(texts["ms"])
            plat_choice = input("\nВаш выбор / Your choice: ").strip()

            if plat_choice == "1":
                platform = "Steam"
                ascii_art = ASCII_STEAM
                break
            elif plat_choice == "2":
                platform = "Epic Games"
                ascii_art = ASCII_EPIC
                break
            elif plat_choice == "3":
                platform = "Microsoft Store"
                ascii_art = ASCII_MS
                break
            else:
                print(texts.get("invalid", "Неверный выбор!"))

        save_choice = input(f"\n{texts['save_data']} ").strip().upper()
        if save_choice in ["Y", "YES", "ДА"]:
            save_settings(lang, platform)
    else:
        ascii_art = ASCII_STEAM if platform == "Steam" else ASCII_EPIC if platform == "Epic Games" else ASCII_MS

    texts = get_texts(lang)

    while True:
        clear_console()
        print(ascii_art)
        print(texts["title"])
        print(texts["main_menu"])
        print(texts["start_clean"])
        print(texts["information"])
        print(texts["change_platform"])
        print(texts["exit"])
        
        choice = input("\nВыберите опцию / Select option: ").strip()

        if choice == "1":
            clean_paths(platform, lang)
        elif choice == "2":
            show_information()
        elif choice == "3":
            # Change Platform
            if platform == "Steam":
                platform = "Microsoft Store"
                ascii_art = ASCII_MS
            elif platform == "Microsoft Store":
                platform = "Epic Games"
                ascii_art = ASCII_EPIC
            else:
                platform = "Steam"
                ascii_art = ASCII_STEAM
            save_settings(lang, platform)
            print(texts.get("platform_changed", "Platform changed successfully!"))
            input("Нажмите Enter...")
        elif choice == "4":
            print("\n" + texts["goodbye"])
            break
        else:
            print(texts.get("invalid", "Неверный выбор!"))
            input("Нажмите Enter...")

def show_information():
    clear_console()
    print("="*70)
    print("created by whybladez /// DbD Cleaner (v1.0) - Latest version of the cleaner.")
    print("")
    print("The cleaner will help bypass HWID ban / license ban.")
    print("")
    print("FOR FULL BYPASS YOU NEED A SPOOFER! Our private spoofer:")
    print("")
    print("https://rubyspoofer.github.io/ruby/")
    print("Discord - discord.gg/btJn66hAuM")
    print("="*70)
    input("\nPress Enter to return to menu...")

def change_language():
    clear_console()
    print("Выберите язык / Choose language\n")
    print("1) Русский")
    print("2) English")
    choice = input("\nВаш выбор: ").strip()
    return "ru" if choice == "1" else "en"

if __name__ == "__main__":
    main()