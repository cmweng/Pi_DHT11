## TKinter 範例


from tkinter import *  ## Python3 tkinter的t為小寫
root = Tk()
root.title("TKinter Demo")
root.geometry('800x100')
frame1 = Frame(root)
frame1.grid(column=0, row=0, sticky=(N, W, E, S))

## label範例
Label(frame1, text = "測試label").grid(column = 0, row = 1, sticky = W,padx=(150,0), pady=5)

## Button範例
testBtn = Button(frame1, text ="測試")
testBtn.grid(column = 0, row = 2, stick = W)



root.mainloop()
