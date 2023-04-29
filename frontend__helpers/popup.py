from PIL import Image, ImageTk, ImageSequence
import tkinter as tk
from tkinter import ttk
import time

def show_popup(root, text):
    def on_closing():
        root.destroy()

    # def thinking_animation():
    #     for frame in thinking_frames:
    #         thinking_label.config(image=frame)
    #         thinking_label.image = frame
    #         root.update()
    #         time.sleep(0.1)

    root.attributes("-topmost", True)
    root.title("Nacho")
    root.protocol("WM_DELETE_WINDOW", on_closing)

    # Get screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    frame = ttk.Frame(root, padding="10")
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    nacho_gif = Image.open("assets/nacho.gif")
    thinking_frames = [ImageTk.PhotoImage(frame) for frame in ImageSequence.Iterator(nacho_gif)]

    thinking_label = ttk.Label(frame, image=thinking_frames[0])
    thinking_label.grid(row=0, column=0, padx=(0, 20))

    text_label = ttk.Label(frame, text=text, font=("Arial", 16))
    text_label.grid(row=0, column=1, padx=(0, 20))

    # Calculate x and y coordinates for the popup window
    x = screen_width - root.winfo_reqwidth() - 10
    y = screen_height - nacho_gif.height - root.winfo_reqheight() - 10

    # Set the geometry of the popup window
    root.geometry("500x{}+{}+{}".format(nacho_gif.height, x, y))

    root.update()