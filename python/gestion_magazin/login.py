import tkinter as tk  # Alias 'tk' pour tkinter
from tkinter import messagebox, TOP, X, LEFT,BOTTOM
import datetime
from PIL import Image, ImageTk
import os
import tkinter as tk  # Alias 'tk' pour tkinter




class Login:
    def __init__(self, root):
        self.root = root
        root.title("Connexion")
        root.geometry("1000x600+230+200")
        root.config(bg="white")
        self.root.focus_force()










if __name__ == "__main__":
    root = tk.Tk()
    obj = Login(root)
    root.mainloop()