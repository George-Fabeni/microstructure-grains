from gui import setup_gui
from customtkinter import *


def main():
    window = CTk()
    window.resizable(width=False, height=False)
    setup_gui(window)
    # Start the GUI loop
    window.mainloop()


if __name__ == "__main__":
    main()
