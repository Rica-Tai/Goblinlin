from PIL import Image
def get_gif_frames(file_path):
    try:
        img = Image.open(file_path)
        if img.is_animated:
            return img.n_frames
        else:
            return 1  # 如果不是动画GIF，则返回1
    except Exception as e:
        print(f"Error loading GIF: {e}")
        return None

gif_path = "./IdleRight.gif"
frame_count = get_gif_frames(gif_path)
if frame_count is not None:
    print(f"GIF帧数：{frame_count}")
else:
    print("无法加载GIF文件。")