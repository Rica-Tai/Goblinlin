import tkinter as tk
import pyautogui as pt
import random
from PIL import Image, ImageTk, ImageSequence
import threading

WIDTH, HEIGHT = pt.size()
taskbarHeight = 40
imgWidth, imgHeight = 1080, 1080
posX, posY = int(WIDTH / 2 - imgWidth / 2), taskbarHeight  
root = tk.Tk()
root.geometry(f"{imgWidth}x{imgHeight}+{posX}+{posY}")
root.overrideredirect(1)

root.configure(bg='black')
root.attributes('-transparentcolor', 'black')
root.wm_attributes('-topmost', 1)

def load_image(file_path):
    try:
        img = Image.open(file_path)
        frames = []
        durations = []
        for frame in ImageSequence.Iterator(img):
            # 将每一帧转换为RGBA模式以保留透明度
            frame_rgba = frame.convert('RGBA')
            
            # 将黑色像素设置为透明
            pixels = frame_rgba.load()
            for x in range(frame_rgba.size[0]):
                for y in range(frame_rgba.size[1]):
                    r, g, b, a = pixels[x, y]
                    if r < 3 and g < 3 and b < 3:  # 如果像素是close黑色
                        pixels[x, y] = (0, 0, 0, 0)  # 设置为透明
            
            frames.append(frame_rgba)  # 不直接转换为PhotoImage
            durations.append(frame.info['duration'])
        return frames, durations
    except Exception as e:
        print(f"Error loading GIF: {e}")
        return None, None

def convert_to_photoimage(frames):
    return [ImageTk.PhotoImage(frame) for frame in frames]

def load_images_async():
    global layDown_frames, layDown_durations, getUp_frames, getUp_durations, idleRight_frames, idleLeft_frames, walkLeft_frames, walkRight_frames, brokeHouse_frames, eatChild_frames, goblinMask_frames, greenDuck_frames, err404_frames, touchFish_frames
    global idleRight_durations, idleLeft_durations, walkLeft_durations, walkRight_durations, brokeHouse_durations, eatChild_durations, goblinMask_durations, greenDuck_durations, err404_durations, touchFish_durations
    
    layDown_raw, layDown_durations = load_image("./LayFlat.gif")
    getUp_raw, getUp_durations = load_image("./GetUp.gif")
    idleRight_raw, idleRight_durations = load_image("./IdleRight.gif")
    idleLeft_raw, idleLeft_durations = load_image("./IdleLeft.gif")
    walkLeft_raw, walkLeft_durations = load_image("./WalkingLeft.gif")
    walkRight_raw, walkRight_durations = load_image("./WalkingRight.gif")
    touchFish_raw, touchFish_durations = load_image("./TouchFish.gif")
    brokeHouse_raw, brokeHouse_durations = load_image("./BrokeHouse.gif")
    eatChild_raw, eatChild_durations = load_image("./EatChild.gif")
    goblinMask_raw, goblinMask_durations = load_image("./GoblinMask.gif")
    greenDuck_raw, greenDuck_durations = load_image("./GreenDuck.gif")
    err404_raw, err404_durations = load_image("./Error404.gif")

    
    # 在主线程中转换为PhotoImage
    layDown_frames = convert_to_photoimage(layDown_raw)
    getUp_frames = convert_to_photoimage(getUp_raw)
    idleRight_frames = convert_to_photoimage(idleRight_raw)
    idleLeft_frames = convert_to_photoimage(idleLeft_raw)
    walkLeft_frames = convert_to_photoimage(walkLeft_raw)
    walkRight_frames = convert_to_photoimage(walkRight_raw)
    touchFish_frames = convert_to_photoimage(touchFish_raw)
    brokeHouse_frames = convert_to_photoimage(brokeHouse_raw)
    eatChild_frames = convert_to_photoimage(eatChild_raw)
    goblinMask_frames = convert_to_photoimage(goblinMask_raw)
    greenDuck_frames = convert_to_photoimage(greenDuck_raw)
    err404_frames = convert_to_photoimage(err404_raw)

# 异步加载图像
load_images_async()

if not layDown_frames:
    print("Error: Unable to load layDown images.")
else:
    downUp_frames = layDown_frames
    downUp_frames.extend(getUp_frames)
    downUp_durations = layDown_durations
    downUp_durations.extend(getUp_durations)
    
    status = {
        0: (getUp_frames, getUp_durations),
        1: (layDown_frames, layDown_durations),
        2: (idleRight_frames, idleRight_durations),
        3: (idleLeft_frames, idleLeft_durations),
        4: (walkRight_frames, walkRight_durations),
        5: (walkLeft_frames, walkLeft_durations),
        6: (downUp_frames, downUp_durations),
        7: (touchFish_frames, touchFish_durations),
        8: (eatChild_frames, eatChild_durations),
        9: (goblinMask_frames, goblinMask_durations),
        10: (greenDuck_frames, greenDuck_durations),
        11: (err404_frames, err404_durations),
        12: (brokeHouse_frames, brokeHouse_durations)
    }

    status_num = 0

    player = tk.Label(root, image=layDown_frames[0], bg='black', bd=0)
    player.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    frame_index = 0

def falling():
    global status_num, posX, posY
    if root.winfo_y() + imgHeight < HEIGHT - taskbarHeight:
        if status_num != 1:
            status_num = 1
        posY+=1
        root.geometry(f"{imgWidth}x{imgHeight}+{posX}+{posY}")
    elif root.winfo_y() + imgHeight >= HEIGHT - taskbarHeight - 3 and status_num == 1:
        status_num = 0
    root.after(5, falling)

def on_click(event):
    global status_num, clicked
    clicked = True
    status_num = random.randint(7, 11)


def changeStatus():
    global status_num, clicked
    if not clicked:
        status_num = random.randint(2, 6)
        print(status_num)
        if (status_num == 0 or status_num == 1):
            root.after(6000, changeStatus)
        elif (status_num == 2 or status_num == 3):
            root.after(4000, changeStatus)
        elif (status_num == 4 or status_num == 5):
            root.after(7000, changeStatus)
        elif (status_num == 6):
            root.after(12000, changeStatus)

def moving():
    global status_num, posX
    if status_num == 4 and root.winfo_x()+imgWidth < WIDTH:
        posX += 1
        root.geometry(f"{imgWidth}x{imgHeight}+{posX}+{posY}")
    elif status_num == 4 and root.winfo_x()+imgWidth >= WIDTH:
        status_num = 2
    
    if status_num == 5 and root.winfo_x()>0:
        posX -= 1
        root.geometry(f"{imgWidth}x{imgHeight}+{posX}+{posY}")
    elif status_num == 5 and root.winfo_x() <= 0:
        status_num = 3
    root.after(3, moving)

def Anim():
    global frame_index, player, clicked
    frames, durations = status[status_num]
    if frame_index < len(frames) - 1:
        frame_index += 1
    else:
        frame_index = 0
        if status_num >= 7 and status_num <= 11:  # 如果是点击触发的动画
            clicked = False  # 动画完成后重置标志
    player.config(image=frames[frame_index])
    player.image = frames[frame_index]  # Keep a reference to avoid garbage collection
    root.after(durations[frame_index], Anim)

def on_drag(event):
    global posX, posY
    posX = event.x_root - imgWidth // 2
    posY = event.y_root - imgHeight // 2
    root.geometry(f"{imgWidth}x{imgHeight}+{posX}+{posY}")

def flat():
    global status_num
    status_num = 6

def fish():
    global status_num
    status_num = 7

def child():
    global status_num
    status_num = 8

def mask():
    global status_num
    status_num = 9

def duck():
    global status_num
    status_num = 10

def er404():
    global status_num
    status_num = 11

def house():
    global status_num
    status_num = 12

root.bind("<Button-1>", on_click)
root.bind("<B1-Motion>", on_drag)

root.bind('f', lambda event: flat())
root.bind('w', lambda event: fish())
root.bind('c', lambda event: child())
root.bind('m', lambda event: mask())
root.bind('d', lambda event: duck())
root.bind('e', lambda event: er404())
root.bind('h', lambda event: house())

changeStatus()
falling()
moving()
Anim()
root.mainloop()