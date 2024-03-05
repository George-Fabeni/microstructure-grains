# -*- coding: utf-8 -*-
"""
Created on Sun Mar  3 21:28:10 2024

@author: georgefabeni
"""

import cv2
import numpy as np
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
from customtkinter import *

# Create the main window
window = CTk()

# Variable to store file path
file_path_var = StringVar()

def upload_image():
    file_path = filedialog.askopenfilename()
    if file_path:
        file_path_var.set(file_path)
        process_image()

def process_image():
    # 'Read' the image
    image = cv2.imread(file_path_var.get(), cv2.IMREAD_GRAYSCALE)
    if image is None:
        return

    # Get current parameters
    blur_size = int(blur_slider.get())
    blur_size = max(1, blur_size if blur_size % 2 != 0 else blur_size + 1)
    
    block_size = int(block_size_slider.get())
    block_size = block_size if block_size % 2 != 0 else block_size + 1  
    
    const_subtract = int(c_slider.get())
    min_area = int(min_area_slider.get())

    # Image processing
    blurred = cv2.GaussianBlur(image, (blur_size, blur_size), 0)
    thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, block_size, const_subtract)
    contours, _ = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    filtered_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_area]
    contour_img = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    cv2.drawContours(contour_img, filtered_contours, -1, (0, 255, 0), 1)

    # Update the image on the GUI
    pil_image = Image.fromarray(cv2.cvtColor(contour_img, cv2.COLOR_BGR2RGB))
    new_size = (700, 500)

    # Resize the image
    resized_image = pil_image.resize(new_size)

    # Convert the resized PIL image to a PhotoImage
    tk_image = ImageTk.PhotoImage(resized_image)

    # Configure the existing img_label to display the new image
    img_label.configure(image=tk_image)
    img_label.image = tk_image  # Keep a reference

    # Update grain count
    grain_count_label.configure(text=f'Number of grains: {len(filtered_contours)}')
    

window.title("Grain Counter")
window.geometry("500x500")
set_appearance_mode("dark")

img_label = CTkLabel(master=window, text="No image assigned")  # Initially, no image is assigned
img_label.pack()

# Button to upload image
upload_button = CTkButton(master=window, text="Upload Image", corner_radius=32, command=upload_image)
upload_button.pack()

# Blurring Slider
blur_slider = CTkSlider(master=window, 
                        from_=1, 
                        to=11, 
                        orientation=HORIZONTAL, 
                        command=lambda x: process_image())
blur_label = CTkLabel(master=window, text="Image Blur")
blur_slider.set(5)  # Default value
blur_label.pack(pady=20)
blur_slider.pack()

# Block size slider
block_size_slider = CTkSlider(master=window, 
                              from_=3, 
                              to=51, 
                              orientation=HORIZONTAL, 
                              command=lambda x: process_image())
block_size_label = CTkLabel(master=window, text="Threshold Block Size")
block_size_slider.set(11)  # Default value
block_size_label.pack(pady=20)
block_size_slider.pack()

#Constant subtraction slider
c_slider = CTkSlider(window, 
                     from_=0, 
                     to=10, 
                     orientation=HORIZONTAL, 
                     command=lambda x: process_image())
c_slider_label = CTkLabel(master=window, text="Constant subtracted from mean")
c_slider.set(2)  # Default value
c_slider_label.pack(pady=20)
c_slider.pack()

#"Minimum grain area considered" Slider
min_area_slider = CTkSlider(window, 
                            from_=0, 
                            to=200, 
                            orientation=HORIZONTAL, 
                            command=lambda x: process_image())
min_area_label = CTkLabel(master=window, text="Minimum Grain Area")
min_area_slider.set(50)  # Default value
min_area_label.pack(pady=20)
min_area_slider.pack()

# Label to display grain count
grain_count_label = CTkLabel(window, text="Number of grains: 0")
grain_count_label.pack()

# Label to display the image
img_label = CTkLabel(window)
img_label.pack()

# Start the GUI loop
window.mainloop()
