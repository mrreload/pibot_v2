from Tkinter import *
from PIL import Image, ImageTk

root = Tk()
c = Canvas(root, width=640, height=480, bd=0, highlightthickness=0)
c.create_line(0,240,640,240, fill='blue')
c.pack()

#blank standard photoimage with red vertical borders
photo = ImageTk.PhotoImage(file="96x96.png")
c.create_image(200,200, image=photo, anchor='nw')

def on_motion(event):
    left,top = c.coords(photo)
    dx = event.x - (left+7)
    c.move(photo, dx, 0)

c.bind('<Motion>', on_motion)
root.mainloop()