#Ådne Øvrebø 2019

#Code to run the program
#source ~/cvpi/bin/activate
#python /home/pi/Desktop/face-recognition-door-opener-raspberry-pi/user_interface.py

#Importint necessary packages
import tkinter
import door
import recognize_faces_and_open_door
from PIL import ImageTk, Image

#function for locking door and updating text
def lock():
    text = door.lock()
    status.config(text=text)
    status.update_idletasks()

#function for unlocking door and updating text
def unlock():
    text = door.unlock()
    status.config(text=text)
    status.update_idletasks()

#Class and function for fullscreen app
class FullScreenApp(object):
    def __init__(self, master, **kwargs):
        self.master=master
        pad=3
        self._geom='200x200+0+0'
        master.geometry("{0}x{1}+0+0".format(
            master.winfo_screenwidth()-pad, master.winfo_screenheight()-pad))
        master.bind('<Escape>',self.toggle_geom)            
    def toggle_geom(self,event):
        geom=self.master.winfo_geometry()
        print(geom,self._geom)
        self.master.geometry(self._geom)
        self._geom=geom

#Function for repeating the facerecognition and updating the last picture
def repeat():
    text = recognize_faces_and_open_door.recogniceFaces()
    status.config(text=text)
    status.update_idletasks()
    
    #Updating the last picture.
    lastimage = ImageTk.PhotoImage(Image.open("/home/pi/Desktop/face-recognition-door-opener-raspberry-pi/lastimage/lastimage.jpg"))   
    panel.configure(image = lastimage)
    panel.image = lastimage
    
    #Repeating the function making it a loop
    top.after(1, repeat)

#Intialising the window.
top = tkinter.Tk()
top.title("Raspberry Pi Face Recognition Door opener")

#Initialising fullscreen app
app=FullScreenApp(top)

#Statuslable
status = tkinter.Label(text = "Door is closed")
status.config(font=("Arial", 44))

#Button for locking door.
closeDoor = tkinter.Button(top, text ="Lock Door", command = lock)
closeDoor.config( height = 10, width = 100 )

#Button for unlocking the door
openDoor = tkinter.Button(top, text ="Unlock Door", command = unlock)
openDoor.config( height = 10, width = 100 )

#Showing the last image
img = ImageTk.PhotoImage(Image.open("/home/pi/Desktop/face-recognition-door-opener-raspberry-pi/lastimage/lastimage.jpg"))
panel = tkinter.Label(top, image = img)
panel.pack(side = "bottom", fill = "both", expand = "yes")

#Adding the items
status.pack()
closeDoor.pack()
openDoor.pack()

#Running the repeat function as a loop.
top.after(1, repeat)

top.mainloop()
