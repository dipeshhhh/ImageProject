'''
- Empty GUI (Functionality will be added later)
- WARNING: USE CTkImage() instead of ImageTk.PhotoImage()
'''
from tkinter import *
from customtkinter import *
from PIL import Image

def open_file():
    # Opens image and resizes it to fit the window
    
    pass

def undo_change():
    # Reverts back to previous change

    pass

def redo_change():
    # Reverts back to next change

    pass

def change_history(change_name):
    # Reverts to a specific point in history

    pass

def track_history(image_name, change_made):
    # Tracks image name and change happened to it 

    pass

def rotate_image(img, img_preview, direction):
    # Rotates both <img> and <img_preview> by 90 degrees in direction = clockwise/anticlockwise
    # Also updates the <img_preview> in GUI

    pass

def flip_image(img, img_preview, orientation):
    # Flips both <img> and <img_preview> in given orientation = vertical/horizontal

    pass

def black_and_white(img, img_preview, level):
    # Turns image to black and white by given level

    pass

def add_text(img, img_preview):
    # Adds text with white background to bottom of the image

    pass

def image_crop(img, img_preview):
    # Crops image while keeping the original height and width ratio

    pass

def save_as(img_output):
    # Saves the given image

    pass

'''
Functions for different size of papers here : )

'''

### ----Initializing Variables---- ###

img=""
img_preview=""

# 2D list to track changes made throughout the execution
history_tracker=[] # [["<Previous image name>", "<Change happened to it>"], [...], ...]

### ----GUI---- ###

## ---Initializing root--- ##
root = CTk()
root.title("Image Handler") # !+! Add icon too
set_appearance_mode("Dark")
set_default_color_theme("blue")
# Menu Bar
menu_bar = Menu(root)
menu_bar.add_command(label="Open Image", command=open_file)
menu_bar.add_command(label="Undo", command = undo_change)
menu_bar.add_command(label="Redo", command = redo_change)
# History Drop Down Menu
history_menu = Menu(menu_bar)
menu_bar.add_cascade(label="History", menu=history_menu)
'''
history_menu.add_command(label=<change_name>, command = lambda: change_history(<change_name>))
'''
root.config(menu=menu_bar)

## ---For the input image--- ##
inputIMG_frame = CTkFrame(root)
# --For Buttons--
button_frame = CTkFrame(inputIMG_frame)

icon_rotate_anticlockwise = CTkImage(Image.open("./Icons/anticlockwise-rotation.png").resize((30,30),Image.Resampling.LANCZOS))
icon_rotate_clockwise = CTkImage(Image.open("./Icons/clockwise-rotation.png").resize((30,30),Image.Resampling.LANCZOS))
icon_flip_vertical = CTkImage(Image.open("./Icons/vertical-flip.png").resize((30,30),Image.Resampling.LANCZOS))
icon_flip_horizontal = CTkImage(Image.open("./Icons/horizontal-flip.png").resize((30,30),Image.Resampling.LANCZOS))
icon_grayscale = CTkImage(Image.open("./Icons/black-and-white.png").resize((60,60),Image.Resampling.LANCZOS))
icon_crop = CTkImage(Image.open("./Icons/crop.png").resize((60,60),Image.Resampling.LANCZOS))
icon_add_text = CTkImage(Image.open("./Icons/add-text.png").resize((60,60),Image.Resampling.LANCZOS))

button_rotate_anticlockwise = CTkButton(button_frame, text="", image=icon_rotate_anticlockwise, command = lambda: rotate_image("<X>","<X>","ANTICLOCKWISE"), width=40,height=80)
button_rotate_clockwise = CTkButton(button_frame, text="", image=icon_rotate_clockwise, command = lambda: rotate_image("<X>","<X>","CLOCKWISE"), width=40,height=80)
button_flip_vertical = CTkButton(button_frame, text="", image=icon_flip_vertical, command = lambda: flip_image("<X>","<X>","VERTICAL"), width=40,height=80)
button_flip_horizontal = CTkButton(button_frame, text="", image=icon_flip_horizontal, command = lambda: flip_image("<X>","<X>","HORIZONTAL"), width=40,height=80)
button_grayscale = CTkButton(button_frame, text="", image=icon_grayscale, command = lambda: black_and_white("<X>","<X>"), width=80, height=80)
button_crop = CTkButton(button_frame, text="", image=icon_crop, command = lambda: image_crop("<X>","<X>"), width=80, height=80)
button_add_text = CTkButton(button_frame, text="", image=icon_add_text, command = lambda: add_text("<X>","<X>"), width=80, height=80)

button_rotate_anticlockwise.grid(row=0,column=0,padx=2,pady=2)
button_rotate_clockwise.grid(row=0,column=1,padx=2,pady=2)
button_flip_vertical.grid(row=1,column=0,padx=2,pady=2)
button_flip_horizontal.grid(row=1,column=1,padx=2,pady=2)
button_grayscale.grid(row=2,column=0, columnspan=2,padx=2,pady=2)
button_crop.grid(row=3,column=0, columnspan=2,padx=2,pady=2)
button_add_text.grid(row=4,column=0, columnspan=2,padx=2,pady=2)

button_frame.grid(row=0,column=0, sticky=N+S)

# --Image Frame-- 
previewIMG_frame = CTkFrame(inputIMG_frame)
# img = Image.open(<image path from open_image() function>)
# img_preview = img.resize(<>)
# img_show = ImageTk.PhotoImage(imgPIL)
previewIMG_frame.grid(row=0,column=1, sticky=N+S,padx=2,pady=2)
inputIMG_frame.grid(row=0,column=0)

# ---Output Image Frame---
outputIMG_frame = CTkFrame(root)

sheet_sizes = ["SelectSize","A4", "A3"]
selected_size = StringVar()
drop_menu = CTkOptionMenu(outputIMG_frame, variable=selected_size, values=sheet_sizes, width=100)
drop_menu.set(sheet_sizes[0])
drop_menu.grid(row=0,column=0)

button_save = CTkButton(outputIMG_frame, text="Save As", command= lambda: save_as("<outIMG>"), width=100)
button_save.grid(row=0,column=1)

outputIMG_frame.grid(row=0,column=1,sticky=N+S,padx=2,pady=2)

root.mainloop()