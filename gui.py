import utils
from customtkinter import *


def upload_image():
    file_path = filedialog.askopenfilename()
    if file_path:
        file_path_var.set(file_path)
        update_process()


def get_slider_values():
    blur_size = int(blur_slider.get())
    blur_size = max(1, blur_size if blur_size % 2 != 0 else blur_size + 1)
    block_size = int(block_size_slider.get())
    block_size = block_size if block_size % 2 != 0 else block_size + 1
    const_subtract = int(c_slider.get())
    min_area = int(min_area_slider.get())
    return blur_size, block_size, const_subtract, min_area


def update_process():
    file_path = file_path_var.get()
    if file_path:
        blur_size, block_size, const_subtract, min_area = get_slider_values()
        thresh, image = utils.process_image(file_path, blur_size, block_size, const_subtract, min_area)
        if thresh is not None:
            contour_img, filtered_contours = utils.draw_contours(thresh, image, min_area)
            average_grain_diameter = utils.count_grains(contour_img, filtered_contours)
            utils.update_image(contour_img, average_grain_diameter, filtered_contours,
                               img_label, grain_count_label, grain_size_label)


def setup_gui(window):
    global blur_slider, block_size_slider, c_slider, min_area_slider, img_label, grain_count_label, grain_size_label
    global file_path_var
    file_path_var = StringVar(master=window)
    window.title("Grain Counter")
    window.geometry("1000x600")
    set_appearance_mode("dark")

    img_label = CTkLabel(master=window, text="No image assigned")  # Initially, no image is assigned
    img_label.place(x=815, y=5)

    # Button to upload image
    upload_button = CTkButton(master=window,
                              text="Upload Image",
                              corner_radius=32,
                              command=upload_image)
    upload_button.place(x=800, y=30)

    # Blurring Slider
    blur_slider = CTkSlider(master=window,
                            from_=1,
                            to=11,
                            orientation=HORIZONTAL,
                            width=100,
                            command=lambda x: update_process())
    blur_label = CTkLabel(master=window, text="Image Blur")
    blur_slider.set(5)  # Default value
    blur_label.place(x=30, y=20)
    blur_slider.place(x=30, y=50)

    # Block size slider
    block_size_slider = CTkSlider(master=window,
                                  from_=3,
                                  to=51,
                                  orientation=HORIZONTAL,
                                  width=100,
                                  command=lambda x: update_process())
    block_size_label = CTkLabel(master=window, text="Threshold Block Size")
    block_size_slider.set(11)  # Default value
    block_size_label.place(x=230, y=20)
    block_size_slider.place(x=230, y=50)

    # Constant subtraction slider
    c_slider = CTkSlider(window,
                         from_=0,
                         to=10,
                         orientation=HORIZONTAL,
                         width=100,
                         command=lambda x: update_process())
    c_slider_label = CTkLabel(master=window, text="Constant subtracted from mean")
    c_slider.set(2)  # Default value
    c_slider_label.place(x=430, y=20)
    c_slider.place(x=430, y=50)

    # "Minimum grain area considered" Slider
    min_area_slider = CTkSlider(window,
                                from_=0,
                                to=200,
                                orientation=HORIZONTAL,
                                width=100,
                                command=lambda x: update_process())
    min_area_label = CTkLabel(master=window, text="Minimum Grain Area")
    min_area_slider.set(50)  # Default value
    min_area_label.place(x=630, y=20)
    min_area_slider.place(x=630, y=50)

    # Label to display grain count
    grain_count_label = CTkLabel(window, text="Number of grains: 0")
    grain_count_label.place(x=815, y=80)

    # Label to display grain size
    grain_size_label = CTkLabel(window, text="Average grain size: 0")
    grain_size_label.place(x=813, y=110)

    # Label to display the image
    img_label = CTkLabel(window, text="Imagem")
    img_label.place(x=30, y=100)

