import tkinter as tk  # Alias 'tk' pour tkinter
from tkinter import messagebox, TOP, X, LEFT, BOTTOM, ttk
import datetime
from tkinter.constants import RIDGE, CENTER, VERTICAL, RIGHT, Y, HORIZONTAL, BOTH, END

import mysql.connector
import self
from PIL import Image, ImageTk
import os
import tkinter as tk  # Alias 'tk' pour tkinter


class Produit:
    def __init__(self, root):
        self.root = root
        root.title("Produit")
        root.geometry("1200x600+900+400")
        root.config(bg="white")
        self.root.focus_force()

        self.var_nfacture = tk.StringVar()
        self.list_facture = []


        title =tk.Label(self.root,text="consulter la facture des clients",font=("goudy old style",40,"bold"),bg="cyan",bd=3,relief=RIDGE).pack(side=TOP,fill=X,padx=10,pady=20)

        lbl_N_facture = tk.Label(self.root, text="Numero facture", font=("times new roman", 20), bg="white").place(x=5,y=150)
        txt_N_facture = tk.Entry(self.root,textvariable=self.var_nfacture,font=("times new roman",20),bg="lightyellow").place(x=250,y=150,width=200)


        btn_recherche = tk.Button(self.root,command=self.recherche,text="Rechercher",font=("times new roman",20,"bold"),bg="green",cursor="hand2").place(x=460,y=150,width=180,height=35)
        btn_reini = tk.Button(self.root,command=self.reini, text="Reinitialiser", font=("times new roman", 20, "bold"), bg="lightgray",cursor="hand2").place(x=650, y=150, width=180, height=35)

        ###liste categorie
        VenteFrame = tk.Frame(self.root, bd=3, relief=RIDGE)
        VenteFrame.place(x=10, y=200, height=390, width=300)

        scroll_y = tk.Scrollbar(VenteFrame, orient=VERTICAL)

        self.list_ventes = tk.Listbox(VenteFrame,font=("goudy old style",10),bg="white",yscrollcommand=scroll_y.set)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_y.config(command=self.list_ventes.yview)
        self.list_ventes.pack(fill=BOTH,expand=1)
        self.list_ventes.bind("<ButtonRelease-1>",self.recuperDonnee)



        #########espace facture
        FactureFrame =tk.Frame(self.root,bd=3,relief=RIDGE)
        FactureFrame.place(x=345,y=200,height=390,width=390)

        title = tk.Label(FactureFrame,text="Facture du client",font=("goudy old style",20,"bold"),bg="orange").pack(side=TOP,fill=X)

        scroll_y2 = tk.Scrollbar(FactureFrame, orient=VERTICAL)
        self.espaceFacture =tk.Text(FactureFrame,font=("goudy old style",12),bg="lightyellow",yscrollcommand=scroll_y2.set)
        scroll_y2.pack(side=RIGHT, fill=Y)
        scroll_y2.config(command=self.espaceFacture.yview)
        self.espaceFacture.pack(fill=BOTH, expand=1)


        ####emplacement de l image
        chemin_image_menu = r"C:\Users\ACER\Desktop\python\gestion_magazin\images\rome.jpg"
        image_menu = Image.open(chemin_image_menu)
        nouvelle_taille = (490, 390)
        image_menu = image_menu.resize(nouvelle_taille)
        self.photo_menu = ImageTk.PhotoImage(image_menu)
        lbl_image = tk.Label(self.root, image=self.photo_menu)
        lbl_image.place(x=750,y=200)

        self.afficher() 


        ###fonction qui va permettre d afficher les factures
    def afficher(self):
        del self.list_facture[:]
        self.list_ventes.delete(0,END)
        for i in os.listdir(r"C:\Users\ACER\Desktop\python\gestion_magazin\factures"):
            if i.split(".")[-1]=="txt":
                self.list_ventes.insert(END,i)
                self.list_facture.append(i.split(".")[0])



    def recuperDonnee(self,ev):
        index_ = self.list_ventes.curselection()
        nom_fichier = self.list_ventes.get(index_)
        fichier_ouvert = open(fr"C:\Users\ACER\Desktop\python\gestion_magazin\factures\{nom_fichier}","r")
        self.espaceFacture.delete("1.0",END)
        for i in fichier_ouvert:
            self.espaceFacture.insert(END,i)
        fichier_ouvert.close()


    def recherche(self):
        if self.var_nfacture.get()=="":
            messagebox.showerror("Erreur","Donner un numéro de facture")
        else:
            if self.var_nfacture.get() in self.list_facture:
                fichier_ouvert = open(fr"C:\Users\ACER\Desktop\python\gestion_magazin\factures\{self.var_nfacture.get()}.txt", "r")
                self.espaceFacture.delete("1.0",END)
                for i in fichier_ouvert:
                    self.espaceFacture.insert(END,i)
                fichier_ouvert.close()
            else:
                messagebox.showerror("Erreur","Numero de facture invalide")


    def reini(self):
        self.afficher()
        self.espaceFacture.delete("1.0",END)
        self.var_nfacture.set("")

if __name__ == "__main__":
    root = tk.Tk()
    obj = Produit(root)
    root.mainloop()
