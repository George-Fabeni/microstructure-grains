import cv2
import numpy as np
from tkinter import *
from customtkinter import CTkImage
from PIL import Image
from skimage.feature import canny
from skimage.util import img_as_ubyte
scale = 10


def process_image(file_path, blur_size, block_size, const_subtract, min_area):
    # 'Read' the image
    image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        return None, None, None, None, None, None

    # Image processing
    blurred = cv2.GaussianBlur(image, (blur_size, blur_size), 0)
    # blurred = cv2.bilateralFilter(image, 9, blur_size, blur_size)
    # canny_img = canny(blurred, sigma=2)
    # canny_img = cv2.dilate(canny_img, 3, iterations=2)
    # blurred = img_as_ubyte(canny_img), 3
    thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, block_size,
                                   const_subtract)
    kernel = np.ones((3, 3), np.uint8)
    cv2.imshow('thresh1', thresh)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    cv2.imshow('thresh2', thresh)
    return thresh, image


def draw_contours(thresh, image, min_area):
    contours, _ = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    h, w = image.shape  # Altura e largura da imagem para checar bordas
    filtered_contours = []
    for cnt in contours:
        if cv2.contourArea(cnt) > min_area:
            x, y, width, height = cv2.boundingRect(cnt)
            if x > 0 and y > 0 and (x + width) < w and (y + height) < h:
                filtered_contours.append(cnt)

    contour_img = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    cv2.drawContours(contour_img, filtered_contours, -1, (0, 255, 0), 1)
    return contour_img, filtered_contours


def count_grains(contour_img, filtered_contours):
    if contour_img is None or filtered_contours is None:
        return  # Não faz nada se não há contornos ou imagem

    # Calculate the areas and other statistics
    grain_areas_px = [cv2.contourArea(cnt) for cnt in filtered_contours]
    grain_areas_um2 = [area_px / (scale ** 2) for area_px in grain_areas_px]
    average_grain_size_um2 = sum(grain_areas_um2) / len(grain_areas_um2) if grain_areas_um2 else 0
    average_grain_diameter = (average_grain_size_um2 / np.pi) ** 0.5
    return average_grain_diameter


def update_image(contour_img, average_grain_diameter, filtered_contours,
                 img_label, grain_count_label, grain_size_label):
    # Update the image on the GUI
    pil_image = Image.fromarray(cv2.cvtColor(contour_img, cv2.COLOR_BGR2RGB))

    # Resize the image
    w, h = pil_image.size
    width_ratio = int(600 * (h / w))
    new_size = (width_ratio, 400)

    # Convert the resized PIL image to a PhotoImage
    tk_image = CTkImage(pil_image, size=new_size)

    # Configure the existing img_label to display the new image
    img_label.configure(image=tk_image)
    img_label.image = tk_image

    # Update grain count and size on the GUI
    grain_count_label.configure(text=f'Number of grains: {len(filtered_contours)}')
    grain_size_label.configure(text=f'Average grain size: {average_grain_diameter:.2f} um')
