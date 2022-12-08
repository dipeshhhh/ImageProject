'''
- Empty GUI (Functionality will be added later)
- Working with 300 DPI
- WARNING: USE CTkImage() INSTEAD OF ImageTk.PhotoImage()
        Using CTkImage() instead of ImageTk.PhotoImage() is not always working
- WARNING: USE Image.Resampling.LANCZOS INSTEAD OF Image.ANTIALIAS
'''
from tkinter import *
from customtkinter import *
from customtkinter import filedialog
from PIL import Image, ImageOps, ImageTk

def open_file():
    # Opens image and resizes it to fit the window
    global img, img_preview, previewIMG_frame

    image_path = filedialog.askopenfilename(initialdir="./", title="Open your image",
                filetypes=(("All types", "*.*"), ("png", "*.png"), ("jpg", "*.jpg")))
    
    # Get the current tkinter window width and height
    window_width = root.winfo_width()
    window_height = root.winfo_height()
    width_inputIMG = int((window_width/2)-46)

    img = Image.open(image_path)
    img_preview = ImageOps.contain(img,(width_inputIMG,window_height))
    show_img_preview = ImageTk.PhotoImage(img_preview)

    # Removing any existing widgets inside the frame
    for widget in previewIMG_frame.winfo_children():
        widget.destroy()

    label_img_preview = CTkLabel(previewIMG_frame, image=show_img_preview, text="")
    label_img_preview.grid(row=0,column=0)

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

def rotate_image(direction):
    global img, img_preview, previewIMG_frame
    # Rotates both <img> and <img_preview> by 90 degrees in direction = clockwise/anticlockwise
    # Also updates the <img_preview> in GUI
    
    if(direction.upper() == "ANTICLOCKWISE"):
        img = img.rotate(90, expand=True)
        img_preview = img_preview.rotate(90, expand=True)
    elif(direction.upper() == "CLOCKWISE"):
        img = img.rotate(-90, expand=True)
        img_preview = img_preview.rotate(-90, expand=True)

    show_img_preview = ImageTk.PhotoImage(img_preview)

    # Removing any existing widgets inside the frame
    for widget in previewIMG_frame.winfo_children():
        widget.destroy()

    label_img_preview = CTkLabel(previewIMG_frame, image=show_img_preview, text="")
    label_img_preview.grid(row=0,column=0)   

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

def output_image(sheet_size):
    # Takes in sheet size and outputs final image required
    # 300 DPI 2.5cm x 3.5cm sized passport image on an A4 sheet (21cm x 29.7cm)
    global img, result_image, result_image_preview

    if(sheet_size == "SelectSize"): # On selecting default option
        for widget in outputIMG_frame.winfo_children():
            widget.destroy()
        return
    if(sheet_size == "A4"):
        result_image = Image.new("RGBA",(2520,3564),color="white")
    elif(sheet_size == "A3"):
        result_image = Image.new("RGBA",(3564,5040),color="white")
    else:
        return
    # A3 Width= 3564, height = 5040
    
    resultIMG_width, resultIMG_height = result_image.size
    
    img_width, img_height = img.size    
    if(img_width > img_height): # Landscape orientation
        img = ImageOps.fit(image=img, size = (420,300))
    else: # Portrait orientation
        img = ImageOps.fit(image=img, size = (300,420))              
    img_width, img_height = img.size
    
    # Counters to check how much images can be added to the sheet
    counter_columns = 0
    counter_rows = 0
    while(resultIMG_width > (img_width+48)):
        counter_columns+=1
        resultIMG_width -= (img_width+48)
    while(resultIMG_height > (img_height+60)):
        counter_rows+=1
        resultIMG_height -= (img_height+60)
    
    # Coordinates to place image
    cord_x = 24
    cord_y = 60
    for row in range(counter_rows):
        for column in range(counter_columns):
            result_image.paste(img,(cord_x,cord_y))
            cord_x += (img_width+24)
        cord_x = 24
        cord_y += (img_height+60)

    # Get the current tkinter window width and height
    window_width = root.winfo_width()
    window_height = root.winfo_height()
    width_result_image = int((window_width/2)-46)
    height_result_image = int(window_height-29)    
    
    result_image_preview = ImageOps.contain(result_image,(width_result_image,height_result_image))

    # Removing any existing widgets inside the frame
    for widget in outputIMG_frame.winfo_children():
        widget.destroy()

    show_result_image_preview = ImageTk.PhotoImage(result_image_preview)
    label_result_image = CTkLabel(outputIMG_frame, image = show_result_image_preview, text="")
    label_result_image.grid(row=0,column=0)

### ----Initializing Variables---- ###

img=""
img_preview=""

result_image=""
result_image_preview=""

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

button_rotate_anticlockwise = CTkButton(button_frame, text="", image=icon_rotate_anticlockwise, command = lambda: rotate_image("ANTICLOCKWISE"), width=40,height=80)
button_rotate_clockwise = CTkButton(button_frame, text="", image=icon_rotate_clockwise, command = lambda: rotate_image("CLOCKWISE"), width=40,height=80)
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

# ---Result Image Frame---
result_frame = CTkFrame(root)

result_button_frame = CTkFrame(result_frame)
sheet_sizes = ["SelectSize","A4", "A3"]
selected_size = StringVar()
drop_menu = CTkOptionMenu(result_button_frame, variable=selected_size, values=sheet_sizes, width=100, 
                            command=lambda X: output_image(selected_size.get()))
drop_menu.set(sheet_sizes[0])
drop_menu.grid(row=0,column=0)
button_save = CTkButton(result_button_frame, text="Save As", command= lambda: save_as("<outIMG>"), width=100)
button_save.grid(row=0,column=1)
result_button_frame.grid(row=0,column=0)

outputIMG_frame = CTkFrame(result_frame)
outputIMG_frame.grid(row=1,column=0)

result_frame.grid(row=0,column=1,sticky=N+S,padx=2,pady=2)

root.state("zoomed")
root.mainloop()