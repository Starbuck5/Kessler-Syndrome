titlez = "Kessler First Time Setup" #title
back = "#0A82FF" #hexadecimal color

import pygame
from tkinter import *
from pgx import *

window = Tk()
window.wm_title(titlez)
window.configure(bg=back)
height=300
width=400
window.minsize(height=height, width=width)
window.maxsize(height=height, width=width)

mainlabel = Label(window, text="Is this your monitor's correct resolution?", bg=back)
mainlabel.place(x=20, y=20)
sublabel1 = Label(window, text="If not, choose from the drop down menu", bg=back)
sublabel1.place(x=20, y=40)
sublabel2 = Label(window, text="Then press 'set resolution'", bg=back)
sublabel2.place(x=20, y=60)

pygame.display.init()
screens = pygame.display.list_modes()
default_screen = screens[0]
pygame.display.quit()

tkvar = StringVar(window)
tkvar.set(default_screen)
selector_box = OptionMenu(window, tkvar, *screens)
selector_box.place(x=250, y=30)

def set_resolution():
    target_resolution = tkvar.get()
    target_resolution = list(target_resolution)
    target_resolution.remove("(")
    target_resolution.remove(")")
    target_resolution = "".join(target_resolution)
    target_resolution = target_resolution.split(", ")

    contents = filehelper.get(0)
    contents[0] = target_resolution[0]
    contents[1] = target_resolution[1]
    filehelper.set(contents, 0)
     
    window.destroy()

file_save = Button(text="Set Resolution", command=set_resolution)
file_save.place(relx=0.4, rely=0.9)

window.mainloop()
