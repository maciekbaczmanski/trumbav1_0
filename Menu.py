import paho.mqtt.client as mqtt
import PIL
from PIL import Image,ImageTk
import cv2
from tkinter import *


'''sekcja MQTT'''
def on_message(client, userdata, message):
    global UpFlag, DownFlag
    if message.topic == "Akcelerometr/Down":
        DownFlag = 1
    
    if message.topic == "Akcelerometr/Up":
        UpFlag = 1
        
broker_address="192.168.0.180"
client = mqtt.Client("Receiver_Tablet")
client.on_message=on_message
client.connect(broker_address)
client.loop_start()
client.subscribe("Akcelerometr/Up")
client.subscribe("Akcelerometr/Down")
'''koniec sekcji MQTT'''

width, height = 800, 600
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

root = Tk()
root.bind('<Escape>', lambda e: root.quit())
lmain = Label(root)
frame = Frame(root)
frame.pack()
flag = 0
UpFlag = 0
DownFlag = 0




def auto_mode():
    if flag == 1:
        start()
        return 0
    lmain.pack()
    Sport_button.pack_forget()
    Auto_button.pack_forget()
    Back_button.pack()
    
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = PIL.Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.after(5, auto_mode)
    

def sport_mode1():
    global flag, DownFlag, UpFlag
    if flag == 1:
        start()
        return 0
    
    Sport_button.pack_forget()
    Auto_button.pack_forget()
    Back_button.pack(side = TOP)
    
    photo = ImageTk.PhotoImage(file="squat1.png")
    lmain.imgtk = photo
    lmain.configure(image=photo)
    lmain.pack(side = BOTTOM)
    if UpFlag == 1:
        DownFlag = 0
        UpFlag = 0
        lmain.after(100, sport_mode2)
    else:
        lmain.after(100, sport_mode1)
    
def sport_mode2():
    global flag, UpFlag, DownFlag
    if flag == 1:
        start()
        return 0
    
    Sport_button.pack_forget()
    Auto_button.pack_forget()
    Back_button.pack(side = TOP)
    
    photo = ImageTk.PhotoImage(file="squat2.png")
    lmain.imgtk = photo
    lmain.configure(image=photo)
    lmain.pack(side = BOTTOM)
    if DownFlag == 1:
        UpFlag = 0
        DownFlag = 0
        lmain.after(100, sport_mode1)
    else:
        lmain.after(100, sport_mode2)
    
    
def back():
    global flag
    flag = 1


def start():
    global lmain
    lmain.destroy()
    lmain = Label(root)
    lmain.pack_forget()
    Sport_button.pack(side=LEFT)
    Auto_button.pack(side=LEFT)
    Back_button.pack_forget()
    frame.pack()
    global flag
    flag = 0


Sport_button = Button(root, text="Tryb sportowy", fg="red", command=sport_mode1)
Auto_button = Button(root,text="Tryb autonomiczny",command=auto_mode)
Back_button = Button(root, text="Quit", command=back)
start()   

root.mainloop()
client.loop_stop()