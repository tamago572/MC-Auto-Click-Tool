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



def detect_key_press():
    global barrage_is_running
    global long_press_is_running
    print("barrage is running: " + str(barrage_is_running))
    print("long press is running: " + str(long_press_is_running))

    while True:
        if keyboard.read_event().event_type == keyboard.KEY_DOWN:
            print("キーが押されました")
            if keyboard.is_pressed("f8"):
                print("F8が押されました")
                print(barrage_is_running)


                if not barrage_is_running:
                    interval = float(intervalbox.get())
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
                print("F9が押されました")

                if not long_press_is_running:
                    status_label2["text"] = "長押し：ON"
                    status_label2.update()

                    long_press_is_running = True

                    pyautogui.mouseDown()

                else:
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
            pyautogui.click()

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
root.geometry("400x300")

label1 = tk.Label(root, text="MC Auto Click Tool")
label1.pack()

label2 = tk.Label(root, text="連打間隔を入力")
label2.pack()

intervalbox = tk.Entry()
intervalbox.insert(tk.END, "2")
intervalbox.pack()

label3 = tk.Label(root, text="秒")
label3.pack()

status_label = tk.Label(root, text="連打：OFF")
status_label.pack()
howto_label = tk.Label(root, text="F8キーで連打開始/停止")
howto_label.pack()

status_label2 = tk.Label(root, text="長押し：OFF")
status_label2.pack()
howto_label2 = tk.Label(root, text="F9キーで連打開始/停止")
howto_label2.pack()

root.mainloop()

