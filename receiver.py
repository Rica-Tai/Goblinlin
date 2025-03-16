import socket
import cv2
import pygame
import threading
import ctypes
import sys

# 設定
VIDEO_PATH = "your_video.mp4"      # 替換成你的影片路徑
AUDIO_PATH = "bigriver (mp3cut.net).mp3"      # 替換成你的音訊路徑
UDP_PORT = 4210
WINDOW_NAME = "Video"

# 播放音訊
def play_audio(audio_path):
    pygame.mixer.init()
    pygame.mixer.music.load(audio_path)
    pygame.mixer.music.play()

# 設定視窗為永遠最上層 (僅限 Windows)
def set_window_always_on_top():
    if sys.platform == "win32":
        hwnd = ctypes.windll.user32.FindWindowW(None, WINDOW_NAME)
        if hwnd:
            ctypes.windll.user32.SetWindowPos(hwnd, -1, 0, 0, 0, 0, 0x0001 | 0x0002)

# 播放影片
def play_fullscreen_video(video_path, audio_path):
    # 啟動音訊播放執行緒
    audio_thread = threading.Thread(target=play_audio, args=(audio_path,))
    audio_thread.start()

    # 播放影片
    cap = cv2.VideoCapture(video_path)
    cv2.namedWindow(WINDOW_NAME, cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty(WINDOW_NAME, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    # 設定視窗為最上層
    set_window_always_on_top()

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow(WINDOW_NAME, frame)
        set_window_always_on_top()  # 確保視窗一直在最上層
        if cv2.waitKey(25) & 0xFF == 27:  # 按 ESC 離開
            break

    cap.release()
    cv2.destroyAllWindows()
    pygame.mixer.music.stop()

# UDP 監聽
def udp_listener():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("", UDP_PORT))
    print(f"Listening for UDP messages on port {UDP_PORT}...")

    while True:
        data, addr = sock.recvfrom(1024)
        message = data.decode('utf-8').strip()
        print(f"Received message: {message} from {addr}")

        if message == "SLAP":
            print("'SLAP' command received. Executing video playback.")
            play_fullscreen_video(VIDEO_PATH, AUDIO_PATH)

if __name__ == "__main__":
    udp_listener()
