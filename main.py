import webbrowser
import pyautogui
import time
import keyboard
import tkinter as tk
from tkinter import messagebox
import threading
import ctypes

barrage_is_running = False
long_press_is_running = False

thread = None


# カスタムスレッドクラス
class twe(threading.Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}):
        threading.Thread.__init__(self, group=group, target=target, name=name)
        self.args = args
        self.kwargs = kwargs
        return

    def run(self):
        self._target(*self.args, **self.kwargs)

    def get_id(self):
        if hasattr(self, '_thread_id'):
            return self._thread_id
        for id, thread in threading._active.items():
            if thread is self:
                return id

    # 強制終了させる関数
    def raise_exception(self):
        thread_id = self.get_id()
        resu = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(thread_id), ctypes.py_object(SystemExit))
        if resu > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(thread_id), 0)
            print('Failure in raising exception')


# https://qiita.com/76r6qo698/items/a0d3bdac3425dda6056a
def detect_key_press():
    global barrage_is_running
    global long_press_is_running
    print("barrage is running: " + str(barrage_is_running))
    print("long press is running: " + str(long_press_is_running))

    while True:
        if keyboard.read_event().event_type == keyboard.KEY_DOWN:
            print("キーが押されました")
            if keyboard.is_pressed("f8"):
                # 連打
                print("F8が押されました")
                print(barrage_is_running)

                if intervalbox.get() == "":
                    messagebox.showerror("エラー", "連打間隔を入力してください")
                    continue

                if not barrage_is_running:
                    try:
                        interval = float(intervalbox.get())
                    except ValueError:
                        messagebox.showerror("エラー", "連打間隔には数字を入力してください")
                        continue

                    print(interval)

                    status_label["text"] = "連打：ON"
                    status_label.update()
                    barrage_is_running = True

                    thread = twe(target=barrage, args=(interval,))
                    thread.start()
                    print("thread開始")
                else:

                    status_label["text"] = "連打：OFF"
                    status_label.update()
                    thread.raise_exception()
                    barrage_is_running = False
                    print(barrage_is_running)

            elif keyboard.is_pressed("f9"):
                # 長押し
                print("F9が押されました")

                if not long_press_is_running:
                    status_label2["text"] = "長押し：ON"
                    status_label2.update()

                    long_press_is_running = True

                    if isRightClick.get():
                        # 右クリ
                        pyautogui.mouseDown(button="right")
                    else:
                        # 左クリ
                        pyautogui.mouseDown()

                else:
                    if isRightClick.get():
                        # 右クリ
                        pyautogui.mouseUp(button="right")
                    else:
                        # 左クリ
                        pyautogui.mouseUp()

                    status_label2["text"] = "長押し：OFF"
                    status_label2.update()

                    long_press_is_running = False

        time.sleep(0.01)

threading.Thread(target=detect_key_press, daemon=True).start()


def barrage(interval):
    print("running barrage")
    try:
        while barrage_is_running:
            if isRightClick.get():
                # 右クリック
                pyautogui.rightClick()
            else:
                # 左クリック
                pyautogui.click()
            print("click")

            start = time.time()

            time.sleep(interval)
            if(not barrage_is_running):
                print("thread break")
                break

            end = time.time()
            diff = end - start
            print(diff)
    finally:
        print("ended")


root = tk.Tk()
root.title("MC Auto Click Tool")
root.geometry("520x400")

frame1 = tk.Frame(root)
frame1.pack(anchor=tk.W, padx=30, pady=15)
frame2 = tk.Frame(root)
frame2.pack(anchor=tk.W, padx=50, pady=10)
frame3 = tk.Frame(root)
frame3.pack(anchor=tk.W, padx=50, pady=10)
frame4 = tk.Frame(root)
frame4.pack(anchor=tk.W, padx=50, pady=10)
frame5 = tk.Frame(root)
frame5.pack(anchor=tk.W, padx=50, pady=10)

label1 = tk.Label(frame1, text="MC Auto Click Tool", font=("Helvetica", 24, "bold"))
label1.pack(side=tk.LEFT)

label2 = tk.Label(frame2, text="連打間隔を入力", font=("Helvetica", 16))
label2.pack(side=tk.LEFT)

intervalbox = tk.Entry(frame2)
intervalbox.insert(tk.END, "2")
intervalbox.pack(side=tk.LEFT)

label3 = tk.Label(frame2, text="秒", font=("Helvetica", 16))
label3.pack(side=tk.LEFT)

howto_label = tk.Label(frame3, text="F8キーで連打開始/停止", font=("Helvetica", 16))
howto_label.pack(anchor=tk.W)
status_label = tk.Label(frame3, text="連打：OFF", font=("Helvetica", 16))
status_label.pack(anchor=tk.W)

howto_label2 = tk.Label(frame4, text="F9キーで長押し開始/停止", font=("Helvetica", 16))
howto_label2.pack(anchor=tk.W)
status_label2 = tk.Label(frame4, text="長押し：OFF", font=("Helvetica", 16))
status_label2.pack(anchor=tk.W)

isRightClick = tk.BooleanVar()
chk = tk.Checkbutton(frame5, variable=isRightClick, text="右クリック", font=("Helvetica", 16))
chk.pack(anchor=tk.W)


def on_closing():
    if messagebox.askokcancel("終了", "終了しますか？"):
        root.destroy()

def open_usage():
    webbrowser.open("")

menubar = tk.Menu(root)
root.config(menu=menubar)

setting_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="設定", menu=setting_menu)

setting_menu.add_command(label="トリガーキーの変更")
setting_menu.add_command(label="終了", command=on_closing)

help_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="ヘルプ", menu=help_menu)

help_menu.add_command(label="使い方")
help_menu.add_command(label="バージョン情報")
help_menu.add_command(label="作者のGitHub")

root.mainloop()
