    # Removing any existing widgets inside the frame
    for widget in previewIMG_frame.winfo_children():
        widget.destroy()

    label_img_preview = CTkLabel(previewIMG_frame, image=show_img_preview, text="")
    label_img_preview.grid(row=0,column=0)   
