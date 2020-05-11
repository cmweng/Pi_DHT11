from tkinter import *  ## Python3 tkinter的t為小寫

root = Tk()
root.title("TKinter Demo")
root.geometry('800x100')
frame1 = Frame(root)
frame1.grid(column=0, row=0, sticky=(N, W, E, S))

Label(frame1, text = "我在frame1裡").grid(column = 0, row = 1, sticky = W,padx=(150,0), pady=5)

testBtn = Button(frame1, text ="測試")
testBtn.grid(column = 0, row = 2, stick = W)



root.mainloop()
