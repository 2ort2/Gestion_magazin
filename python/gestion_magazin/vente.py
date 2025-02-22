import tkinter as tk  # Alias 'tk' pour tkinter
from tkinter import messagebox, TOP, X, LEFT,BOTTOM
import datetime
from PIL import Image, ImageTk
import os
import tkinter as tk  # Alias 'tk' pour tkinter




class Vente:
    def __init__(self, root):
        self.root = root
        root.title("Vente")
        root.geometry("1200x600+400+200")
        root.config(bg="white")
        self.root.focus_force()










if __name__ == "__main__":
    root = tk.Tk()
    obj = Vente(root)
    root.mainloop()