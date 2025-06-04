import tkinter as tk
from tkinter import messagebox, PhotoImage, filedialog
import subprocess
import os
import sys

def startRoot():
    startScreen.destroy()
    # if getattr(sys, 'frozen', False):
    #     base_path = sys._MEIPASS
    # else:
    #     base_path = os.path.dirname(__file__)

    # root_path = "root.py"#os.path.join(base_path, "root.py")
    subprocess.run(["root.exe"])
def close():
    startScreen.destroy()

startScreen = tk.Tk()
startScreen.title("Images cryptography")
startScreen.geometry("500x300")  # Width x height
startScreen.configure(bg="lightgray")  # Tło okna na szary

Text = \
'                   ###########  Images Cryptography   ###########\n\n\
Subject: \n\
Cryptography and security of IT systems \n\
Title: \n\
Image encryption \n\n\
Authors:\nMarcin Janis, Jan Golenia\n\nAiR, ISS\n21.05.2025 r. '


# Info label
InfoLabel = tk.Label(startScreen, text=Text, justify='left', anchor = 'w', wraplength = 380, font = ("Arial", 10) )
InfoLabel.place(x=10, y=0, width=480, height=200) 

start_bt = tk.Button(startScreen, text="Start", command=startRoot, fg="black", font=("Arial", 12))
start_bt.place(x=30, y=250, width=100, height=30) 

start_bt = tk.Button(startScreen, text="Close", command=close, fg="black", font=("Arial", 12))
start_bt.place(x=370, y=250, width=100, height=30) 

startScreen.mainloop()