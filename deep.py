import os
import sys
import json
import requests
import subprocess
import platform
from pathlib import Path
from urllib.parse import urlparse
import shutil
import tempfile
import ctypes
import time

versionprogram = 'release-1.3.5'

print("⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⠀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀")
print("⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⡤⠶⠚⠉⢉⣩⠽⠟⠛⠛⠛⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀")
print("⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠞⠉⠀⢀⣠⠞⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀")
print("⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡞⠁⠀⠀⣰⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀")
print("⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⠀⠀⠀⡼⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣠⡤⠤⠄⢤⣄⣀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀")
print("⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇⠀⠀⢰⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⠴⠒⠋⠉⠀⠀⠀⣀⣤⠴⠒⠋⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀")
print("⠀⠀⠀⠀⠀⠀⠀⠀⠀⠻⡄⠀⠀⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠞⢳⡄⢀⡴⠚⠉⠀⠀⠀⠀⠀⣠⠴⠚⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀")
print("⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢦⡀⠘⣧⠀⠀⠀⠀⠀⠀⠀⠀⣰⠃⠀⠀⠹⡏⠀⠀⠀⠀⠀⣀⣴⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀")
print("⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠳⢬⣳⣄⣠⠤⠤⠶⠶⠒⠋⠀⠀⠀⠀⠹⡀⠀⠀⠀⠀⠈⠉⠛⠲⢦⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀")
print("⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⠤⠖⠋⠉⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠱⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⢳⠦⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀")
print("⠀⠀⠀⠀⠀⠀⠀⠀⣠⠖⠋⠀⠀⠀⣠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢱⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⠀⢃⠈⠙⠲⣄⡀⠀⠀⠀⠀⠀⠀⠀")
print("⠀⠀⠀⠀⠀⠀⢠⠞⠁⠀⠀⠀⢀⢾⠃⠀⠀⠀⠀⠀⠀⠀⠀⢢⠀⠀⠀⠀⠀⠀⠀⢣⠀⠀⠀⠀⠀⠀⠀⠀⠀⣹⠮⣄⠀⠀⠀⠙⢦⡀⠀⠀⠀⠀⠀")
print("⠀⠀⠀⠀⠀⣰⠋⠀⠀⢀⡤⡴⠃⠈⠦⣀⠀⠀⠀⠀⠀⠀⢀⣷⢸⠀⠀⠀⠀⢀⣀⠘⡄⠤⠤⢤⠔⠒⠂⠉⠁⠀⠀⠀⠑⢄⡀⠀⠀⠙⢦⡀⠀")
print("⠀⠀⠀⠀⣼⠃⠀⠀⢠⣞⠟⠀⠀⠀⡄⠀⠉⠒⠢⣤⣤⠄⣼⢻⠸⠀⠀⠀⠀⠉⢤⠀⢿⡖⠒⠊⢦⠤⠤⣀⣀⡀⠀⠀⠀⠈⠻⡝⠲⢤⣀⠙⢦⠀⠀")
print("⠀⠀⠀⢰⠃⠀⠀⣴⣿⠎⠀⠀⢀⣜⠤⠄⢲⠎⠉⠀⠀⡼⠸⠘⡄⡇⠀⠀⠀⠀⢸⠀⢸⠘⢆⠀⠘⡄⠀⠀⠀⢢⠉⠉⠀⠒⠒⠽⡄⠀⠈⠙⠮⣷⡀")
print("⠀⠀⠀⡟⠀⠀⣼⢻⠧⠐⠂⠉⡜⠀⠀⡰⡟⠀⠀⠀⡰⠁⡇⠀⡇⡇⠀⠀⠀⠀⢺⠇⠀⣆⡨⢆⠀⢽⠀⠀⠀⠈⡷⡄⠀⠀⠀⠀⠹⡄⠀⠀⠀⠈⠁")
print("⠀⠀⢸⠃⠀⠀⢃⠎⠀⠀⠀⣴⠃⠀⡜⠹⠁⠀⠀⡰⠁⢠⠁⠀⢸⢸⠀⠀⠀⢠⡸⢣⠔⡏⠀⠈⢆⠀⣇⠀⠀⠀⢸⠘⢆⠀⠀⠀⠀⢳⠀⠀⠀⠀⠀")
print("⠀⠀⢸⠀⠀⠀⡜⠀⠀⢀⡜⡞⠀⡜⠈⠏⠀⠈⡹⠑⠒⠼⡀⠀⠀⢿⠀⠀⠀⢀⡇⠀⢇⢁⠀⠀⠈⢆⢰⠀⠀⠀⠈⡄⠈⢢⠀⠀⠀⠈⣇⠀⠀⠀⠀")
print("⠀⠀⢸⡀⠀⢰⠁⠀⢀⢮⠀⠇⡜⠀⠘⠀⠀⢰⠃⠀⠀⡇⠈⠁⠀⢘⡄⠀⠀⢸⠀⠀⣘⣼⠤⠤⠤⣈⡞⡀⠀⠀⠀⡇⠰⡄⢣⡀⠀⠀⢻⠀⠀⠀⠀")
print("⠀⠀⠈⡇⠀⡜⠀⢀⠎⢸⢸⢰⠁⠀⠄⠀⢠⠃⠀⠀⢸⠀⠀⠀⠀⠀⡇⠀⠀⡆⠀⠀⣶⣿⡿⠿⡛⢻⡟⡇⠀⠀⠀⡇⠀⣿⣆⢡⠀⠀⢸⡇⠀⠀⠀")
print("⠀⠀⢠⡏⠀⠉⢢⡎⠀⡇⣿⠊⠀⠀⠀⢠⡏⠀⠀⠀⠎⠀⠀⠀⠀⠀⡇⠀⡸⠀⠀⠀⡇⠀⢰⡆⡇⢸⢠⢹⠀⠀⠀⡇⠀⢹⠈⢧⣣⠀⠘⡇⠀⠀⠀")
print("⠀⠀⢸⡇⠀⠀⠀⡇⠀⡇⢹⠀⠀⠀⢀⡾⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇⢠⠃⠀⠀⠠⠟⡯⣻⣇⢃⠇⢠⠏⡇⠀⢸⡆⠀⢸⠀⠈⢳⡀⠀⡇⠀⠀⠀")
print("⠀⠀⠀⣇⠀⡔⠋⡇⠀⢱⢼⠀⠀⡂⣼⡇⢹⣶⣶⣶⣤⣤⣀⠀⠀⠀⣇⠇⠀⠀⠀⠀⣶⡭⢃⣏⡘⠀⡎⠀⠇⠀⡾⣷⠀⣼⠀⠀⠀⢻⡄⡇⠀⠀⠀")
print("⠀⠀⠀⣹⠜⠋⠉⠓⢄⡏⢸⠀⠀⢳⡏⢸⠹⢀⣉⢭⣻⡽⠿⠛⠓⠀⠋⠀⠀⠀⠀⠀⠘⠛⠛⠓⠀⡄⡇⠀⢸⢰⡇⢸⡄⡟⠀⠀⠀⠀⢳⡇⠀⠀⠀")
print("⠀⣠⠞⠁⠀⠀⠀⠀⠀⢙⠌⡇⠀⣿⠁⠀⡇⡗⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠰⠀⠀⠀⠀⠀⠀⠁⠁⠀⢸⣼⠀⠈⣇⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀")
print("⢸⠁⠀⠀⢀⡠⠔⠚⠉⠉⢱⣇⢸⢧⠀⠀⠸⣱⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⡤⠦⡔⠀⠀⠀⠀⠀⢀⡼⠀⠀⣼⡏⠀⠀⢹⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀")
print("⢸⠀⠀⠀⠋⠀⠀⠀⢀⡠⠤⣿⣾⣇⣧⠀⠀⢫⡆⠀⠀⠀⠀⠀⠀⠀⢨⠀⠀⣠⠇⠀⠀⢀⡠⣶⠋⠀⠀⡸⣾⠁⠀⠀⠈⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀")
print("⢸⡄⠀⠀⠀⠀⠠⠊⠁⠀⠀⢸⢃⠘⡜⡵⡀⠈⢿⡱⢲⡤⠤⢀⣀⣀⡀⠉⠉⣀⡠⡴⠚⠉⣸⢸⠀⠀⢠⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀")
print("⠀⢧⠀⠀⠀⠀⠀⠀⠀⣀⠤⠚⠚⣤⣵⡰⡑⡄⠀⢣⡈⠳⡀⠀⠀⠀⢨⡋⠙⣆⢸⠀⠀⣰⢻⡎⠀⠀⡎⡇⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀")
print("⠀⠈⢷⡀⠀⠀⠀⠀⠀⠁⠀⠀⠀⡸⢌⣳⣵⡈⢦⡀⠳⡀⠈⢦⡀⠀⠘⠏⠲⣌⠙⢒⠴⡧⣸⡇⠀⡸⢸⠇⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀")
print("⠀⠀⢠⣿⠢⡀⠀⠀⠀⠠⠄⡖⠋⠀⠀⠙⢿⣳⡀⠑⢄⠹⣄⡀⠙⢄⡠⠤⠒⠚⡖⡇⠀⠘⣽⡇⢠⠃⢸⢀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀")
print("⠀⠀⣾⠃⠀⠀⠀⠀⠀⢀⡼⣄⠀⠀⠀⠀⠀⠑⣽⣆⠀⠑⢝⡍⠒⠬⢧⣀⡠⠊⠀⠸⡀⠀⢹⡇⡎⠀⡿⢸⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀")
print("⠀⡼⠁⠀⠀⠀⠀⠀⠀⢀⠻⣺⣧⠀⠀⠀⠰⢢⠈⢪⡷⡀⠀⠙⡄⠀⠀⠱⡄⠀⠀⠀⢧⠀⢸⡻⠀⢠⡇⣾⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀")
print("⢰⠇⠀⠀⠀⠀⠀⠀⠀⢸⠀⡏⣿⠀⠀⠀⠀⢣⢇⠀⠑⣄⠀⠀⠸⡄⠀⠀⠘⡄⠀⠀⠸⡀⢸⠁⠀⡾⢰⡏⢳⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀")
print("-------------------------------------------------------------")
import requests
import os

import requests
import os
import time

print("| Проверяю подключение к интернету... 🩸")

import requests, os, subprocess; print("| Интернет:", "✓" if requests.get("https://www.google.com", timeout=3).status_code == 200 else "✗", "Ping:", "✓" if subprocess.run(['ping', '-n' if os.name=='nt' else '-c', '2', '8.8.8.8'], capture_output=True).returncode == 0 else "✗")

print("| Ver : ", versionprogram)
print("| Наш Телеграм - https://t.me/+Bf2OFfq6ztU1ZTJi")
print("| By @DeepGit :#")
print("| 🩸 Deep - Привет! Что сегодня скачаем?")
print("--------------------------------------")
print("1. ISO Образы")
print("2. Игры")
print("3. Программы")
print("4. Дрова (Драйвера)")
print("--------------------------------------")

menuselect = input("Введите номер раздела > ")


def download_file(url, filename):
    try:
        print(f"Скачиваю с: {url}")
        response = requests.get(url, stream=True)
        response.raise_for_status()

        total_size = int(response.headers.get('content-length', 0))
        block_size = 8192
        downloaded = 0

        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=block_size):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)

                    if total_size > 0:
                        progress = (downloaded / total_size) * 100
                        filled_length = int(50 * downloaded // total_size)
                        bar = '█' * filled_length + '░' * (50 - filled_length)
                        print(f'\rПрогресс: |{bar}| {progress:.1f}% {downloaded}/{total_size} байт', end='')

        print(f"\n🩸 Загрузка завершена! Файл сохранен: {filename}")
        time.sleep(10)
    except Exception as e:
        print(f"\n🩸 Ошибка загрузки: {e}")


if menuselect == "1":
    print(" ")
    print("Выбери ISO Образ 🩸")
    print("-------------------")
    print("1. Windows 10 | Maku-OS (Сборка от @makuadarii)")
    print("2. Windows 11 | Maku-OS (Сборка от @makuadarii)")
    print("3. Linux | Debian")
    print("4. Linux | Ubuntu")
    print("5. Linux | Nyarch")
    print("6. Linux | Nyarch - For NVIDIA")
    isoselect = input("Введите номер ISO > ")

    folder = input("Введите путь для сохранения (например: C:/Downloads): ")
    if not os.path.exists(folder):
        os.makedirs(folder)

    if isoselect == "1":
        print("\nНачинаю загрузку Windows 10... 🩸")
        url = "https://pixeldrain.com/api/file/Etnqpk1D?download"
        download_file(url, os.path.join(folder, "windows10.iso"))
    elif isoselect == "2":
        print("\nНачинаю загрузку Windows 11... 🩸")
        url = "https://pixeldrain.com/api/file/JrXsz7kN?download"
        download_file(url, os.path.join(folder, "windows11.iso"))
    elif isoselect == "3":
        print("\nНачинаю загрузку Debian... 🩸")
        url = "https://cdimage.debian.org/debian-cd/current/amd64/iso-cd/debian-13.2.0-amd64-netinst.iso"
        download_file(url, os.path.join(folder, "debian.iso"))
    elif isoselect == "4":
        print("\nНачинаю загрузку Ubuntu... 🩸")
        url = "Ошибка! Добавьте свой url на скачку Ubuntu а то у меня чёт не грузит"
        download_file(url, os.path.join(folder, "ubuntu.iso"))
    elif isoselect == "5":
        print("\nНачинаю загрузку Nyarch... 🩸")
        url = "https://mirror.nyarchlinux.moe/Nyarch_Gnome_25.04.2.iso"
        download_file(url, os.path.join(folder, "Nyarch_Gnome_25.04.2.iso"))
    elif isoselect == "6":
        print("\nНачинаю загрузку Nyarch... 🩸")
        url = "https://mirror.nyarchlinux.moe/Nyarch_Nyaovidea_Gnome_25.04.2.iso"
        download_file(url, os.path.join(folder, "Nyarch_Nyaovidea_Gnome_25.04.2.iso"))

elif menuselect == "2":
    print(" ")
    print("Выбери игру 🩸")
    print("-------------------")
    print("1. DDNet")
    gameselect = input("Введите номер игры > ")

    folder = input("Введите путь для сохранения (например: C:/Games): ")
    if not os.path.exists(folder):
        os.makedirs(folder)
    elif gameselect == "1":
        print("\nНачинаю загрузку DDNet... 🩸")
        url = "https://ddnet.org/downloads/DDNet-19.5-win64.zip"
        download_file(url, os.path.join(folder, "DDNet-19.5-win64.zip"))

elif menuselect == "3":
    print(" ")
    print("Выбери программу 🩸")
    print("-------------------")
    print("1. Amnezia WG")
    print("2. Visual Code Studio")
    print("3. Olama AI - ИИ без интернета, для хорошей модели вам потребуется 70гб. Лучшая модель 'gpt-oss:120b'")
    print("4. qBittorrent")
    print("5. Android Debug Bridge (adb)")
    print("6. Scrcpy")
    programselect = input("Введите номер программы > ")

    folder = input("Введите путь для сохранения (например: C:/Programs): ")
    if not os.path.exists(folder):
        os.makedirs(folder)

    if programselect == "1":
        print("\nНачинаю загрузку Amnezia WG... 🩸")
        url = "https://github.com/amnezia-vpn/amneziawg-windows-client/releases/download/1.0.2/amneziawg-amd64-1.0.2.msi"
        download_file(url, os.path.join(folder, "amneziawg-amd64-1.0.2.msi"))
    elif programselect == "2":
        print("\nНачинаю загрузку Visual Code Studio... 🩸")
        url = "https://vscode.download.prss.microsoft.com/dbazure/download/stable/bf9252a2fb45be6893dd8870c0bf37e2e1766d61/VSCodeUserSetup-x64-1.106.3.exe"
        download_file(url, os.path.join(folder, "VSCodeUserSetup-x64-1.106.3.exe"))
    elif programselect == "3":
        print("\nНачинаю загрузку Olama AI... 🩸")
        url = "https://release-assets.githubusercontent.com/github-production-release-asset/658928958/8992aa4f-d3f1-46eb-a8f9-7c74e6482d3d?sp=r&sv=2018-11-09&sr=b&spr=https&se=2025-12-09T13%3A42%3A22Z&rscd=attachment%3B+filename%3DOllamaSetup.exe&rsct=application%2Foctet-stream&skoid=96c2d410-5711-43a1-aedd-ab1947aa7ab0&sktid=398a6654-997b-47e9-b12b-9515b896b4de&skt=2025-12-09T12%3A42%3A01Z&ske=2025-12-09T13%3A42%3A22Z&sks=b&skv=2018-11-09&sig=XoEcf4igj6zbqynlEQX%2BYNDrLBRRnGnG45bn5DL%2FGiU%3D&jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmVsZWFzZS1hc3NldHMuZ2l0aHVidXNlcmNvbnRlbnQuY29tIiwia2V5Ijoia2V5MSIsImV4cCI6MTc2NTI4ODUxMCwibmJmIjoxNzY1Mjg0OTEwLCJwYXRoIjoicmVsZWFzZWFzc2V0cHJvZHVjdGlvbi5ibG9iLmNvcmUud2luZG93cy5uZXQifQ.Gsb6b0_Z42ARHLaaUCCDDL0m5Wp-IiYf-xNbZeRwtwY&response-content-disposition=attachment%3B%20filename%3DOllamaSetup.exe&response-content-type=application%2Foctet-stream"
        download_file(url, os.path.join(folder, "olama.exe"))
    elif programselect == "4":
        print("\nНачинаю загрузку qBittorrent... 🩸")
        url = "https://release-assets.githubusercontent.com/github-production-release-asset/658928958/8992aa4f-d3f1-46eb-a8f9-7c74e6482d3d?sp=r&sv=2018-11-09&sr=b&spr=https&se=2025-12-09T13%3A42%3A22Z&rscd=attachment%3B+filename%3DOllamaSetup.exe&rsct=application%2Foctet-stream&skoid=96c2d410-5711-43a1-aedd-ab1947aa7ab0&sktid=398a6654-997b-47e9-b12b-9515b896b4de&skt=2025-12-09T12%3A42%3A01Z&ske=2025-12-09T13%3A42%3A22Z&sks=b&skv=2018-11-09&sig=XoEcf4igj6zbqynlEQX%2BYNDrLBRRnGnG45bn5DL%2FGiU%3D&jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmVsZWFzZS1hc3NldHMuZ2l0aHVidXNlcmNvbnRlbnQuY29tIiwia2V5Ijoia2V5MSIsImV4cCI6MTc2NTI4ODUxMCwibmJmIjoxNzY1Mjg0OTEwLCJwYXRoIjoicmVsZWFzZWFzc2V0cHJvZHVjdGlvbi5ibG9iLmNvcmUud2luZG93cy5uZXQifQ.Gsb6b0_Z42ARHLaaUCCDDL0m5Wp-IiYf-xNbZeRwtwY&response-content-disposition=attachment%3B%20filename%3DOllamaSetup.exe&response-content-type=application%2Foctet-stream"
        download_file(url, os.path.join(folder, "olama.exe"))
    elif programselect == "5":
        print("\nНачинаю загрузку adb... 🩸")
        url = "https://dl.google.com/android/repository/platform-tools-latest-windows.zip"
        download_file(url, os.path.join(folder, "platform-tools-latest-windows.zip"))
    elif programselect == "6":
        print("\nНачинаю загрузку scrcpy... 🩸")
        url = "https://github.com/Genymobile/scrcpy/releases/download/v3.3.3/scrcpy-win64-v3.3.3.zip"
        download_file(url, os.path.join(folder, "scrcpy-win64-v3.3.3.zip"))
elif menuselect == "4":
    print(" ")
    print("Выбери программу 🩸")
    print("-------------------")
    print("1. Пак Драйверов (SDL Full - 44,0 GB) | .torrent")
    programselect = input("Введите номер программы > ")

    folder = input("Введите путь для сохранения (например: C:/Drivers): ")
    if not os.path.exists(folder):
        os.makedirs(folder)

    if programselect == "1":
        print("\nНачинаю загрузку SDL Full... 🩸 Что бы установить используйте любой торрент программу, например : qBittorrent")
        url = "https://github.com/kuzzov/Deep-Cheburnet/raw/refs/heads/main/SDI_Update.torrent"
        download_file(url, os.path.join(folder, "SDI_Update.torrent"))


