import numpy as np
import cv2
import tkinter
from PIL import Image, ImageTk, ImageOps
from customtkinter import *
import matplotlib.pyplot as plt

window = CTk()

def process_image():
    microstructure = cv2.imread("grains.jpg", cv2.IMREAD_GRAYSCALE)
    
    blur_size = int(blur_slider.get())
    blur_size = max(1, blur_size if blur_size % 2 != 0 else blur_size + 1)
    block_size = int(block_size_slider.get())
    block_size = block_size if block_size % 2 != 0 else block_size + 1  
    const_subtract = int(c_slider.get())
    bilateral_size = int(bilateral_slider.get())
    
   
    #RGB_img = cv2.cvtColor(microstructure, cv2.COLOR_BGR2RGB)
    blurred0 = cv2.blur(microstructure, (blur_size, blur_size))
    blurred1 = cv2.GaussianBlur(microstructure, (blur_size,blur_size), 0)
    bilateral = cv2.bilateralFilter(microstructure, 9, bilateral_size, bilateral_size)
    threshgaussian = cv2.adaptiveThreshold(blurred0, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, block_size, const_subtract)
    threshbilateral = cv2.adaptiveThreshold(bilateral, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, block_size, const_subtract)
    
    hori = np.concatenate((microstructure, blurred0, blurred1), axis=1)
    vert = np.concatenate((bilateral, threshgaussian, threshbilateral), axis=1)
    total = np.concatenate((hori, vert), axis=0)
    pil_image = Image.fromarray(cv2.cvtColor(total, cv2.COLOR_BGR2RGB))
    new_size = (1300, 600)
    resized_image = pil_image.resize(new_size)
    tk_image = ImageTk.PhotoImage(resized_image)
    img_label.configure(image=tk_image)
    img_label.place(x=100, y=150)
    img_label.image = tk_image  # Keep a reference


blur_slider = CTkSlider(master=window, from_=1, to=11, orientation=HORIZONTAL, command=lambda x: process_image())
blur_label = CTkLabel(master=window, text="Image Blur")
blur_slider.set(5)  # Default value
blur_label.place(x=30, y=10)
blur_slider.place(x=30, y=40)

bilateral_slider = CTkSlider(master=window, from_=0, to=200, orientation=HORIZONTAL, command=lambda x: process_image())
bilateral_label = CTkLabel(master=window, text="Threshold Block Size")
bilateral_slider.set(75)  # Default value
bilateral_label.place(x=300,y=70)
bilateral_slider.place(x=300, y=100)

block_size_slider = CTkSlider(master=window, from_=3, to=51, orientation=HORIZONTAL, command=lambda x: process_image())
block_size_label = CTkLabel(master=window, text="Threshold Block Size")
block_size_slider.set(11)  # Default value
block_size_label.place(x=30,y=70)
block_size_slider.place(x=30, y=100)

c_slider = CTkSlider(window, from_=0, to=10, orientation=HORIZONTAL, command=lambda x: process_image())
c_slider_label = CTkLabel(master=window, text="Constant subtracted from mean")
c_slider.set(2)  # Default value
c_slider_label.place(x=300, y=10)
c_slider.place(x=300, y=40)

start = CTkButton(master=window, text="Start", corner_radius=32, command=process_image)
start.pack()

window.geometry("1500x700")
img_label = CTkLabel(window)
img_label.pack()
window.mainloop()
cv2.waitKey(0)
cv2.destroyAllWindows()