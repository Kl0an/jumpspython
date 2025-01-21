import cv2
import pygame
import threading
import ctypes
import pygetwindow as gw
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import time
import logging

# Configuração do logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Função para reproduzir áudio
def play_audio(audio_path):
    logging.info(f"Reproduzindo áudio: {audio_path}")
    pygame.mixer.init()
    pygame.mixer.music.load(audio_path)
    pygame.mixer.music.set_volume(1.0)
    pygame.mixer.music.play()
    logging.info("Áudio iniciado")

# Função para manter a janela do vídeo ativa e maximizada
def keep_window_active(window_name):
    logging.info(f"Monitorando janela: {window_name}")
    while True:
        windows = gw.getWindowsWithTitle(window_name)
        if windows:
            window = windows[0]
            if not window.isActive:
                window.activate()
                logging.info(f"Janela '{window_name}' ativada")
            if not window.isMaximized:
                window.maximize()
                logging.info(f"Janela '{window_name}' maximizada")
        time.sleep(0.1)

# Função para reproduzir vídeo em tela cheia
def play_video_fullscreen(video_path):
    logging.info(f"Iniciando reprodução do vídeo: {video_path}")
    user32 = ctypes.windll.user32
    screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        logging.error("Erro ao abrir o vídeo.")
        return
    
    cv2.namedWindow('Jumpscare Video', cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty('Jumpscare Video', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    # Thread para manter a janela do vídeo em primeiro plano e tela cheia
    threading.Thread(target=keep_window_active, args=('Jumpscare Video',), daemon=True).start()

    fps = cap.get(cv2.CAP_PROP_FPS)
    wait_time = int(1000 / fps)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            logging.warning("Não foi possível ler o frame.")
            break
        frame = cv2.resize(frame, screensize)
        cv2.imshow('Jumpscare Video', frame)
        cv2.setWindowProperty('Jumpscare Video', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        if cv2.waitKey(wait_time) & 0xFF == ord('q'):
            break

    time.sleep(5)
    cap.release()
    cv2.destroyAllWindows()
    logging.info("Reprodução do vídeo finalizada")

# Função para definir o volume do sistema
def set_system_volume(volume_level):
    logging.info(f"Definindo volume do sistema para: {volume_level * 100}%")
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volume.SetMasterVolumeLevelScalar(volume_level, None)

# Função principal para configurar e iniciar a reprodução
def main():
    video_path = 'C:/Users/liman/OneDrive/Documentos/scripts/FNaF 4 - Nightmare Freddy Jumpscare.mp4'
    audio_path = 'C:/Users/liman/OneDrive/Documentos/scripts/FNaF 4 - Nightmare Freddy Jumpscare.mp3'

    logging.info("Iniciando o script de jumpscare")
    set_system_volume(1.0)

    threading.Thread(target=play_audio, args=(audio_path,)).start()

    play_video_fullscreen(video_path)
    logging.info("Script de jumpscare finalizado")

if __name__ == "__main__":
    main()
