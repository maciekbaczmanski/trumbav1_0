import paho.mqtt.client as mqtt
import PIL
from PIL import Image,ImageTk
import cv2
from tkinter import *
import time


'''sekcja MQTT'''
count = 6
counter2 = 8
im1 = 2
im2 = 2
Squats1 = 0
Squats2 = 0
UpFlag1 = 0
DownFlag1 = 0
UpFlag2 = 0
DownFlag2 = 0
MasterReady = 0
PlayerQuit = 0
Player1Win = 0
Player2Win = 0
def on_message(client, userdata, message):
    global Player2Win,Player1Win,PlayerQuit,MasterReady, UpFlag1, DownFlag1, UpFlag2, DownFlag2, Squats1, Squats2
    if message.topic == "Akcelerometr1/Down":
       UpFlag1 = 1

    if message.topic == "Akcelerometr1/Up":
        DownFlag1 = 1
        Squats1 += 1
        
    if message.topic == "AkcelerometrBur/Down":
        UpFlag2 = 1
    
    if message.topic == "AkcelerometrBur/Up":
        DownFlag2 = 1
        Squats2 += 1
        
    if message.topic == "Player/Quit":
        PlayerQuit = 1
        
    if message.topic == "Master/Ready":
        MasterReady = 1
     
    if message.topic == "Win/Player1":
        Player1Win = 1
        
    if message.topic == "Win/Player2":
        Player2Win = 1
        
broker_address="192.168.0.180"
client = mqtt.Client("Receiver_Tablet1")  # Zmiana na 2 tablecie
client.on_message=on_message
client.connect(broker_address)
client.loop_start()
client.subscribe("Akcelerometr1/Up")
client.subscribe("Akcelerometr1/Down")
client.subscribe("AkcelerometrBur/Up")
client.subscribe("AkcelerometrBur/Down")
client.subscribe("Player/Quit")
client.subscribe("Win/Player2")
client.subscribe("Win/Player1")
client.subscribe("Master/Ready")
'''koniec sekcji MQTT'''

#width, height = 596, 444 640x480 
width, height = 480, 360
cap = cv2.VideoCapture('http://192.168.0.190:8000/stream.mjpg')
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

root = Tk()
root.title('Trumba')
root.geometry("800x480")
root.resizable(0, 0)
root.bind('<Escape>', lambda e: root.quit())
#root.attributes("-fullscreen", True)
lmain = Label(root)
left = Label(root)
right = Label(root)
text = Text(root, height=3, width=70)
text_me = Text(root, height=1, width=20)
text_enemy = Text(root, height=1, width=20)
frame = Frame(root)
frame.pack()
flag = 0

def auto_start():
    client.publish("Mode/Auto","Here we go cleaning again")
    auto_mode()
    return 0

def auto_mode():
    global flag
    if flag == 1:
        start()
        return 0
    lmain.pack()
    Sport_button.pack_forget()
    Game_button.pack_forget()
    Auto_button.pack_forget()
    Back_button.pack(side=RIGHT, anchor=NE)
    
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = PIL.Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.after(5, auto_mode)
    
def sport_start():
    client.publish("Mode/Sport","Let's a go Mario")
    sport_mode1()
    return 0

def sport_mode1():
    global flag, DownFlag1, UpFlag1, Napis, Squats1
    Napis = "Ilość przysiadów:\n{}".format(Squats1)
    if flag == 1:
        start()
        return 0
    
    Sport_button.pack_forget()
    Auto_button.pack_forget()
    Game_button.pack_forget()
    
    
    photo = ImageTk.PhotoImage(file="squat1.png")
    lmain.imgtk = photo
    lmain.configure(image=photo)
    lmain.pack(side=LEFT, anchor=NW)
    
    text.delete('1.0', END)
    text.insert(END, Napis)
    text.config(font=("Helvetica", 50))
    text.pack(side = TOP,anchor = NE)
    Back_button.pack(side = TOP,anchor = NE)
    
    if UpFlag1 == 1:
        DownFlag1 = 0
        UpFlag1 = 0
        lmain.after(100, sport_mode2)
    else:
        lmain.after(100, sport_mode1)
    
def sport_mode2():
    global flag, DownFlag1, UpFlag1
    if flag == 1:
        start()
        return 0
    
    Sport_button.pack_forget()
    Auto_button.pack_forget()
    Game_button.pack_forget()
    
    photo = ImageTk.PhotoImage(file="squat2.png")
    lmain.imgtk = photo
    lmain.configure(image=photo)
    lmain.pack(side=TOP, anchor=NW)
    
    text.delete('1.0', END)
    text.insert(END, Napis)
    text.config(font=("Helvetica", 50))
    text.pack(side = TOP,anchor = NE)
    Back_button.pack(side = TOP,anchor = NE)
    if DownFlag1 == 1:
        UpFlag1 = 0
        DownFlag1 = 0
        lmain.after(100, sport_mode1)
    else:
        lmain.after(100, sport_mode2)
   
   
def game_start():
    global counter2, Player2Win,Player1Win,PlayerQuit,MasterReady,count, im1, im2, flag, DownFlag1, UpFlag1,DownFlag2, UpFlag2, Squats1, Squats2
    if flag == 1 or PlayerQuit == 1 or Player1Win == 1 or Player2Win == 1:
        if flag == 1:
            start()
            if MasterReady != 0:
                client.publish("Player/Quit","Hasta la vista Baby")
            return 0   
        elif PlayerQuit != 0:
            start()
            return 0    
    
    if MasterReady==0:
        Napis1 = "Zrób 20" #Up
        Napis2 = "i wygraj" #Down
        client.publish("Ready/Player1","Ready Player One")
        
    elif MasterReady!=0 and count > 0:
        Napis1 = "Start za" #Up
        Napis2 = "{}".format(count-1)
        count -= 1
        time.sleep(1)
        Squats1 = 0
        Squats2 = 0
        im1 = 2
        im2 = 2
        UpFlag1 = 0
        UpFlag2 = 0
        DownFlag1 = 0
        DownFlag2 = 0               
    else:
        Napis1 = "<-   {}".format(Squats1) #Up
        Napis2 = "     {}   ->".format(Squats2) #Down
        
             
        
    Sport_button.pack_forget()
    Auto_button.pack_forget()
    Game_button.pack_forget()
    
    if Player1Win:
       photo1 = ImageTk.PhotoImage(file="redwin.png")
       Napis1 = "Wygrałeś!"
       Napis2 = "Gratuluję!"
    elif Player2Win:
       photo1 = ImageTk.PhotoImage(file="redloose.png")
       Napis1 = "Oponent"
       Napis2 = "zwyciężył"
    else:
        if UpFlag1 == 1:
            photo1 = ImageTk.PhotoImage(file="squat2.png")
            UpFlag1 = 0
            im1 = 1
        elif DownFlag1 == 1:
            photo1 = ImageTk.PhotoImage(file="squat1.png")
            DownFlag1 = 0
            im1 = 2
        else:
            if im1 == 1:
                photo1 = ImageTk.PhotoImage(file="squat2.png")
            elif im1 == 2:
                photo1 = ImageTk.PhotoImage(file="squat1.png")
    left.imgtk = photo1
    left.configure(image=photo1)
    left.pack(side=LEFT, anchor=NW)
    
    if Player1Win:
       photo2 = ImageTk.PhotoImage(file="blueloose.png")
    elif Player2Win:
       photo2 = ImageTk.PhotoImage(file="bluewin.png") 
    else:
        if DownFlag2 == 1:
            photo2 = ImageTk.PhotoImage(file="squat4.png")
            DownFlag2 = 0
            im2 = 1
        elif UpFlag2 == 1:
            photo2 = ImageTk.PhotoImage(file="squat3.png")
            UpFlag2 = 0
            im2 = 2
        else:
            if im2 == 1:
                photo2 = ImageTk.PhotoImage(file="squat4.png")
            elif im2 == 2:
                photo2 = ImageTk.PhotoImage(file="squat3.png") 
    right.imgtk = photo2
    right.configure(image=photo2)
    right.pack(side=RIGHT, anchor = NE)
    
    
    text_me.delete('1.0', END)
    text_me.insert(END, Napis1)
    text_me.config(font=("Helvetica", 50))
    text_me.pack(side =TOP,anchor = NW)
    
    Game_quit.pack(side = TOP,anchor = NW)
    
    text_enemy.delete('1.0', END)
    text_enemy.insert(END, Napis2)
    text_enemy.config(font=("Helvetica", 50))
    text_enemy.pack(side = TOP,anchor = NW)
    
    if Player1Win!=0 or Player2Win != 0:
        print(counter2)
        if counter2 > 0:
            counter2 -= 1
            right.after(1000, game_start)
        else:
            start()    
            return 0
    else:
        right.after(100, game_start)
  
  
def back():
    global flag
    flag = 1


def start():
    client.publish("Mode/Quit","Hard choices")
    global counter2, Player1Win,Player2Win,PlayerQuit,count, MasterReady, lmain,Squats1, Squats2, flag, UpFlag1, UpFlag2, DownFlag1, DownFlag2
    counter2 = 8
    Player2Win = 0
    Player1Win = 0
    PlayerQuit = 0
    count = 6
    flag = 0
    Squats1 = 0
    Squats2 = 0
    im1 = 2
    im2 = 2
    UpFlag1 = 0
    UpFlag2 = 0
    DownFlag1 = 0
    DownFlag = 0
    MasterReady = 0
    lmain.destroy()
    right.pack_forget()
    left.pack_forget()
    lmain = Label(root)
    lmain.pack_forget()
    text.pack_forget()
    text_me.pack_forget()
    text_enemy.pack_forget()
    Back_button.pack_forget()
    Game_quit.pack_forget()
    Sport_button.pack(side=LEFT, anchor=NW)
    Auto_button.pack(side=LEFT,anchor=NW)
    Game_button.pack(side=LEFT,anchor=NW)
    frame.pack()

    


Sport_button = Button(root, text="Tryb sportowy", fg="red",font=('Helvetica', 18, "bold"), command=sport_start, height = 26, width = 18)
Auto_button = Button(root,text="Tryb autonomiczny",font=('Helvetica', 18, "bold"),command=auto_start, height = 26, width = 19)
Back_button = Button(root, text="Quit", command=back, height = 12, width = 65)
Game_button = Button(root, text="Game start",fg="blue",font=('Helvetica', 18, "bold"), command=game_start, height = 26, width = 18)
Game_quit = Button(root, text="Quit",font=('Helvetica', 18, "bold"), command=back, height = 9, width = 21)

start()   

root.mainloop()
client.loop_stop()