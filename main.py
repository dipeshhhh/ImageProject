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
from PIL import Image, ImageOps, ImageTk, ImageEnhance
#ignore::CTkLabelWarning

def re_frame(image_name, frame_name):
    # Empties frame then adds PhotoImage to grid(row=0,column=0)
    # image_name: ImageTk.PhotoImage(), frame_name: CTkFrame()
    show_image_name = ImageTk.PhotoImage(image_name)

    for widget in frame_name.winfo_children():
        widget.destroy()

    label_img_preview = CTkLabel(frame_name, image=show_image_name, text="")
    label_img_preview.grid(row=0,column=0)  

def open_file():
    # Opens image and resizes it to fit the window
    global img, img_preview, previewIMG_frame

    image_extentions = (
        ("All Files","*.*"),
        ("PNG","*.png"),
        ("JPG","*.jpg"),
        ("JPEG","*.jpeg"))

    image_path = filedialog.askopenfilename(initialdir="./", title="Open your image",
                filetypes=image_extentions)
    
    # Get the current tkinter window width and height
    window_width = root.winfo_width()
    window_height = root.winfo_height()
    width_inputIMG = int((window_width/2)-46)

    img = Image.open(image_path)
    img_preview = ImageOps.contain(img,(width_inputIMG,window_height))
    # show_img_preview = ImageTk.PhotoImage(img_preview)

    re_frame(img_preview, previewIMG_frame)

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
    # Rotates both <img> and <img_preview> by 90 degrees in direction = clockwise/anticlockwise
    # Also updates the <img_preview> in GUI
    global img, img_preview, previewIMG_frame

    if(direction.upper() == "ANTICLOCKWISE"):
        img = img.rotate(90, expand=True)
        img_preview = img_preview.rotate(90, expand=True)
    elif(direction.upper() == "CLOCKWISE"):
        img = img.rotate(-90, expand=True)
        img_preview = img_preview.rotate(-90, expand=True)

    # show_img_preview = ImageTk.PhotoImage(img_preview)

    re_frame(img_preview, previewIMG_frame) 

def flip_image(orientation):
    # Flips both <img> and <img_preview> in given orientation = vertical/horizontal
    global img, img_preview

    if(orientation.upper() == "VERTICAL"):
        img = img.transpose(Image.TRANSPOSE.FLIP_TOP_BOTTOM)
        img_preview = img_preview.transpose(Image.TRANSPOSE.FLIP_TOP_BOTTOM)
    elif(orientation.upper() == "HORIZONTAL"):
        img = img.transpose(Image.TRANSPOSE.FLIP_LEFT_RIGHT)
        img_preview = img_preview.transpose(Image.TRANSPOSE.FLIP_LEFT_RIGHT)

    # show_image_preview = ImageTk.PhotoImage(img_preview)

    re_frame(img_preview, previewIMG_frame)

def black_and_white():
    # Toggles greyscale in the image
    global img, img_preview, isGrayscale, grayscale_backup, grayscale_preview_backup
    
    if(isGrayscale):
        img = grayscale_backup
        img_preview = grayscale_preview_backup

        isGrayscale = False
    
    elif(not(isGrayscale)):
        grayscale_backup = img
        grayscale_preview_backup = img_preview

        img = ImageEnhance.Color(img).enhance(0)
        img_preview = ImageEnhance.Color(img_preview).enhance(0)

        isGrayscale = True
    
    # show_image_preview = ImageTk.PhotoImage(img_preview)
    re_frame(img_preview, previewIMG_frame)

def add_text(img, img_preview):
    # Adds text with white background to bottom of the image

    pass

def image_crop():
    # Crops image
    crop_function = CTkToplevel()
    crop_function.title("Crop Image")
    global img, img_preview, cropped_image
    
    img_width, img_height = img.size
    img_preview_width, img_preview_height = img_preview.size
    show_img_preview = ImageTk.PhotoImage(img_preview)

    img_to_preview_ratio = img_width/img_preview_width    

    def crop(left, top, right, bottom):
        # Crops and Displays in real-time
        global cropped_image, Left, Right, Top, Bottom

        crop_image = img_preview.copy()
        cropped_image = crop_image.crop((left, top, img_preview_width-right, img_preview_height-bottom))
        show_cropped_image = ImageTk.PhotoImage(cropped_image)
        
        label_show_preview_img.configure(image=show_cropped_image)
        
        # Updating Values for original img
        Left = left*img_to_preview_ratio
        Top = top*img_to_preview_ratio
        Right = right*img_to_preview_ratio
        Bottom = bottom*img_to_preview_ratio

    def save():
        # Updates the original image with cropped one

        global img_preview, img, Left, Right, Top, Bottom

        window_width = root.winfo_width()
        window_height = root.winfo_height()
        width_inputIMG = int((window_width/2)-46)

        img_preview = ImageOps.contain(cropped_image,(width_inputIMG,window_height))
        img = img.crop((Left,Top,img_width-Right,img_height-Bottom))
        re_frame(img_preview, previewIMG_frame)
        crop_function.destroy()

    # Sliders in Control Frame
    control_frame = CTkFrame(crop_function)

    label_left_text = CTkLabel(control_frame,text="Left")
    label_left_text.grid(row=0,column=0, padx=2, pady=2)
    left_slider = CTkSlider(master=control_frame,from_=0, to=img_preview_width, 
                            orientation=HORIZONTAL,
                            command=lambda X: crop(left_slider.get(),
                                                    top_slider.get(),
                                                    right_slider.get(),
                                                    bottom_slider.get()))
    left_slider.set(0)
    left_slider.grid(row=0,column=1, padx=2, pady=2)

    label_right_text = CTkLabel(control_frame,text="Right")
    label_right_text.grid(row=1,column=0, padx=2, pady=2)
    right_slider = CTkSlider(master=control_frame,from_=0, to=img_preview_width, 
                            orientation=HORIZONTAL,
                            command=lambda X: crop(left_slider.get(),
                                                    top_slider.get(),
                                                    right_slider.get(),
                                                    bottom_slider.get()))
    right_slider.set(0)
    right_slider.grid(row=1,column=1, padx=2, pady=2)

    label_topTXT = CTkLabel(control_frame,text="Top")
    label_topTXT.grid(row=2,column=0, padx=2, pady=2)
    top_slider = CTkSlider(master=control_frame,from_=0, to=img_preview_height, 
                            orientation=HORIZONTAL,
                            command=lambda X: crop(left_slider.get(),
                                                    top_slider.get(),
                                                    right_slider.get(),
                                                    bottom_slider.get()))
    top_slider.set(0)
    top_slider.grid(row=2,column=1, padx=2, pady=2)

    label_bottomTXT = CTkLabel(control_frame,text="Bottom")
    label_bottomTXT.grid(row=3,column=0, padx=2, pady=2)
    bottom_slider = CTkSlider(master=control_frame,from_=0, to=img_preview_height, 
                            orientation=HORIZONTAL,
                            command=lambda X: crop(left_slider.get(),
                                                    top_slider.get(),
                                                    right_slider.get(),
                                                    bottom_slider.get()))
    bottom_slider.set(0)
    bottom_slider.grid(row=3,column=1, padx=2, pady=2)

    cancel_button = CTkButton(control_frame, text="Cancel", command=crop_function.destroy)
    cancel_button.grid(row=4,column=0,pady=20)

    ok_button = CTkButton(control_frame,text="OK",command=save)
    ok_button.grid(row=4,column=1)

    control_frame.grid(row=0,column=2,padx=10,sticky=N+S)

    # Creating image frame -> grid_propagate(0)
    cropImage_Frame = CTkFrame(crop_function, width=img_preview_width+2, height=img_preview_height+2)
    cropImage_Frame.grid_propagate(0)
    label_show_preview_img = CTkLabel(master=cropImage_Frame,image = show_img_preview, text="")
    label_show_preview_img.place(relx=0.5, rely=0.5, anchor=CENTER)
    cropImage_Frame.grid(row=0,column=1, sticky=N+S)

def save_as(img_output):
    # Saves the given image

    image_extentions = (
        ("PNG","*.png"),
        ("JPG","*.jpg"),
        ("JPEG","*.jpeg"),
        ("All Files","*.*"))
    
    file_path = filedialog.asksaveasfilename(filetypes=image_extentions, defaultextension=image_extentions, 
                                            initialfile="PrintImage.png", title="Save Image")
    
    img_output.save(file_path)

def output_image(sheet_size):
    # Takes in sheet size and outputs final image required
    # 300 DPI 2.5cm x 3.5cm sized passport image on an A4 sheet (21cm x 29.7cm)
    global img, result_image, result_image_preview

    if(sheet_size == "SelectSize"): # On selecting default option
        for widget in outputIMG_frame.winfo_children():
            widget.destroy()
        return
    if(sheet_size == "A4"):
        result_image = Image.new("RGB",(2520,3564),color="white")
    elif(sheet_size == "A3"):
        result_image = Image.new("RGB",(3564,5040),color="white")
    else:
        return

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
    # show_result_image_preview = ImageTk.PhotoImage(result_image_preview)

    re_frame(result_image_preview, outputIMG_frame)

### ----Initializing Variables---- ###

img=""
img_preview=""

result_image=""
result_image_preview=""

isGrayscale = False
grayscale_backup = ""
grayscale_preview_backup = ""

cropped_image = ""
Left = Top = Right = Bottom = 0

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
button_flip_vertical = CTkButton(button_frame, text="", image=icon_flip_vertical, command = lambda: flip_image("VERTICAL"), width=40,height=80)
button_flip_horizontal = CTkButton(button_frame, text="", image=icon_flip_horizontal, command = lambda: flip_image("HORIZONTAL"), width=40,height=80)
button_grayscale = CTkButton(button_frame, text="", image=icon_grayscale, command = black_and_white, width=80, height=80)
button_crop = CTkButton(button_frame, text="", image=icon_crop, command = image_crop, width=80, height=80)
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
button_save = CTkButton(result_button_frame, text="Save As", command= lambda: save_as(result_image), width=100)
button_save.grid(row=0,column=1)
result_button_frame.grid(row=0,column=0)

outputIMG_frame = CTkFrame(result_frame)
outputIMG_frame.grid(row=1,column=0)

result_frame.grid(row=0,column=1,sticky=N+S,padx=2,pady=2)

root.state("zoomed")
root.mainloop()