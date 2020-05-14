##  利用TKinter設計GUI
##  將溫溼度藏測值顯示在GUI判面
##  以GUI按鈕控制監測開始、停止

from tkinter import *
from tkinter import messagebox
import Adafruit_DHT
import time             ##  
import threading        ##  多執行緒模組
import mysql.connector
from mysql.connector import Error

## 抓取溫溼度執行緒物件
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
            if humidity is not None and temperature is not None and btn1['text']=='stop':
                roomtmp.set(str(temperature)+'℃')
                roomhum.set(str(humidity)+' %')  
                btn1.config(state="normal")
                root.update_idletasks()
                ds_name = dataset_name.get()
                insert_db(ds_name, temperature, humidity)

                time.sleep(600)
 
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

## 寫入資料庫
def insert_db(ds,tmp,hum):
    ##寫入資料庫
    query = "INSERT INTO dht11s(dataset,temperature,humidity) VALUES(%s,%s,%s)"
    args = (ds, tmp, hum)
    conn = None
    try:
        conn = mysql.connector.connect(host = '192.168.86.32',
                                       database = 'pi',
                                       user = 'pi',
                                       password = '123456')
        cursor = conn.cursor()
        cursor.execute(query, args)
        conn.commit()
    except Error as e:
        print(e)
    finally:
        if conn != None :
            cursor.close()
            conn.close()
        else:
            pass

## 按鈕function
def btnClick():
    if len(dataset_name.get()) != 0:
        if btn1['text'] == "start":
            btn1['text']="stop"
            if get_Data.isAlive():
                get_Data.resume()
                DS.config(state='disabled')
            else:
                get_Data.start()
                DS['state']='disabled'
        else:
            get_Data.pause()
            btn1['text']="start"
            DS['state']='normal'
    else:
        messagebox.showerror("Error", "需先輸入Dataset Name")
        pass


##  建立monitor執行續
get_Data = monitor()


root = Tk()
root.title("監測溫度、溼度")
## root.geometry('400x100')


mainframe = Frame(root)
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight = 1)
root.rowconfigure(0, weight = 1)

##  將溫、溼度以及案銨鈕顯示文字指定為字串變數
roomtmp = StringVar()       ##  溫度
roomhum = StringVar()       ##  溼度
btntxt = StringVar()        ##  按鈕
dataset_name = StringVar()

Label(mainframe, text = "Dataset Name:").grid(column = 2, row = 2, sticky = W,padx=(150,0), pady=5)
DS = Entry(mainframe, textvariable = dataset_name ,fg = 'blue')
DS.grid(column=3, row=2, sticky=(W,E),padx=(5,150), pady=5)


Label(mainframe, text = "現在室內溫度：").grid(column = 2, row = 3, sticky = W,padx=(150,0), pady=5)

##  溫度值label,顯示溫度值
Label(mainframe, textvariable=roomtmp).grid(column=3, row=3, sticky=(W,E),padx=(5,150), pady=5)

Label(mainframe, text = "現在室內溼度：").grid(column = 2, row = 5, sticky = W,padx=(150,0), pady=5)

##  溼度值label,顯示溼度值
Label(mainframe, textvariable=roomhum).grid(column=3, row=5, sticky=(W,E),padx=(5,150), pady=5)

##  開始/停止按鈕
btn1 = Button(mainframe, text = "start", command = btnClick, pady=5)
btn1.grid(column = 3, row = 6, sticky = W)

##  設定溫、溼度未監時的值
roomtmp.set(str("- - -"))
roomhum.set(str("- - -"))

##  按鈕值需設為"start"
btntxt.set("start")


root.mainloop()
