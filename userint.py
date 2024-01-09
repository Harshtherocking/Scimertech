import tkinter as tk
from jcamp import jcamp_readfile

import urllib.request
import urllib.parse
import re
import os
import io
import joblib

from jdx_help import * 
from model import * 
from PIL import Image, ImageTk

from matplotlib import pyplot as plt 

HISTORY = os.path.join(os.getcwd(), "history")



def on_submit():
    input_text = entry.get()
  
    compName = input_text
    
    # getting the link and saving jdx in the history
    JDXlink, CAS = get_jdx_link(compName)
    if (JDXlink or CAS )is None :
        result_label.config(text = "CAS not found")
        return
    else:
        result_text = process_input(CAS)
        result_label.config(text = result_text)

    download_and_save_file(JDXlink, CAS ,location = HISTORY)

    # reading jdx
    jdx_dict = get_coordinates(os.path.join(HISTORY, CAS))

    

    if plt : 
        plt.close()
        
    plt.plot(jdx_dict["x"] , jdx_dict["y"])

    imgBuffer = io.BytesIO()
    plt.savefig(imgBuffer, format = "jpg")

    img = Image.open(imgBuffer)

    # img = img.resize((150, 150))  # Adjust the size as needed
    photo = ImageTk.PhotoImage(img)
    image_label.config(image=photo)
    image_label.image = photo

    imgBuffer.close()





def process_input(input_text):
    return "CAS found: " + input_text






# Create the main window
root = tk.Tk()
root.geometry("720x480")
root.title("IR Analysis")

# Create and place a text box
entry = tk.Entry(root, width=30)
entry.pack(pady=10)

# Create and place a submit button
submit_button = tk.Button(root, text="Submit", command=on_submit)
submit_button.pack()


# Create and place a label to display the result text
result_label = tk.Label(root, text="")
result_label.pack(pady=10)

# FuncGrp
fg = tk.Label(root, text = "")
fg.pack(pady = 10)

# Create and place a label to display the image
image_label = tk.Label(root)
image_label.pack()

# Start the Tkinter event loop
root.mainloop()