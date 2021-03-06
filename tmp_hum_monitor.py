#  開發環境Raspberry Pi 4B, Phython3.7.3, TKinter 8.6
#  利用TKinter設計GUI
#  將溫溼度值顯示在GUI介面
#  以GUI按鈕控制監測開始、停止

from tkinter import *
import Adafruit_DHT
import time  # 引入time模組
import threading  # 多執行緒模組


# 抓取溫溼度執行緒
class monitor(threading.Thread):
    def __init__(self):
        super(monitor, self).__init__()
        self.iterations = 0
        self.daemon = True  # Allow main to exit even if still running.
        self.paused = True  # Start out paused.
        self.state = threading.Condition()

    def run(self):
        sensor = Adafruit_DHT.DHT11
        pin = 4
        while True:
            humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
            if humidity is not None and temperature is not None and btn1['text'] == 'stop':
                roomtmp.set(str(temperature) + '℃')
                roomhum.set(str(humidity) + ' %')
                btn1.config(state="normal")
                root.update_idletasks()
                time.sleep(3)

    def resume(self):  # 用來恢復/啓動run
        with self.state:  # 在該條件下操作
            self.paused = False
            self.state.notify()  # Unblock self if waiting.

    def pause(self):  # 用來暫停run
        with self.state:  # 在該條件下操作
            self.paused = True  # Block self.
            roomtmp.set(str("- - - -"))
            roomhum.set(str("- - - -"))
##


# 起動及停止按鈕function
def btnClick():
    if btn1['text'] == "start":
        btn1['text'] = "stop"
        if get_Data.isAlive():
            get_Data.resume()
        else:
            get_Data.start()
    else:
        get_Data.pause()
        btn1['text'] = "start"


#  建立monitor執行續
get_Data = monitor()

# Tkinter GUI
root = Tk()
root.title("監測溫度、溼度")
# root.geometry('400x100')


mainframe = Frame(root)
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# 將溫、溼度以及案銨鈕顯示文字指定為字串變數
roomtmp = StringVar()       # 溫度變數
roomhum = StringVar()       # 溼度變數
btntxt = StringVar()        # 按鈕變數

Label(mainframe, text="現在室內溫度：").grid(column=2, row=3, sticky=W, padx=(150, 0), pady=5)

# 溫度值label,顯示溫度值
Label(mainframe, textvariable=roomtmp).grid(column=3, row=3, sticky=(W, E), padx=(5, 150), pady=5)

Label(mainframe, text="現在室內溼度：").grid(column=2, row=5, sticky=W, padx=(150, 0), pady=5)

# 溼度值label,顯示溼度值
Label(mainframe, textvariable=roomhum).grid(column=3, row=5, sticky=(W, E), padx=(5, 150), pady=5)

# 開始/停止按鈕
btn1 = Button(mainframe, text="start", command=btnClick, pady=5)
btn1.grid(column=3, row=6, sticky=W)

# 設定溫、溼度未監時的值
roomtmp.set(str("- - -"))
roomhum.set(str("- - -"))

# 按鈕值需設為"start"
btntxt.set("start")

root.mainloop()
