import tkinter as tk  # Alias 'tk' pour tkinter
from tkinter import messagebox, TOP, X, LEFT, BOTTOM, ttk
import datetime
from tkinter.constants import RIDGE, HORIZONTAL, RIGHT, Y, VERTICAL, BOTH, RAISED, END

import mysql.connector
from PIL import Image, ImageTk
import os
import tkinter as tk  # Alias 'tk' pour tkinter




class Categorie:
    def __init__(self, root):
        self.root = root
        root.title("Categorie")
        root.geometry("1200x600+400+200")
        root.config(bg="white")
        self.root.focus_force()

        # Connexion à la base de données MySQL sur XAMPP
        self.con = mysql.connector.connect(
            host="localhost",
            port=3307,
            user="root",
            password="",
            database="gestion_magazin"
        )
        self.cur = self.con.cursor()

        ###declaration des variables
        self.var_cat_idc = tk.StringVar()
        self.var_nom = tk.StringVar()


        title = tk.Label(self.root, text="Gestion Categorie Produit", font=("goudy old style",35,"bold"),bg="cyan",bd=3,relief=RIDGE).pack(side=TOP, fill=X, padx=10,pady=10)

        ###contenu
        lbl_categorie= tk.Label(self.root,text="Saisir Categorie Produit",font=("times new roman",19),bg="white").place(x=50,y=150)
        txt_categorie = tk.Entry(self.root,textvariable=self.var_nom, font=("times new roman",20),bg="lightyellow").place(x=45,y=230,width=300)

        ###button
        btn_ajouter = tk.Button(self.root,command=self.ajouter, text="Ajouter",font=("times new roman",19),bg="green",cursor="hand2").place(x=390,y=230,width=180,height=50)
        btn_supprimer = tk.Button(self.root, command=self.supprimer,text="Suppimer", font=("times new roman", 19), bg="red", cursor="hand2").place(x=600, y=230, width=180, height=50)


        ###liste categorie
        listeFrame = tk.Frame(self.root, bd=3, relief=RIDGE)
        listeFrame.place(x=800, y=100, height=185, width=400)

        scroll_y = tk.Scrollbar(listeFrame, orient=VERTICAL)
        scroll_y.pack(side=RIGHT, fill=Y)

        scroll_x = tk.Scrollbar(listeFrame, orient=HORIZONTAL)
        scroll_x.pack(side=BOTTOM, fill=X)

        self.categorieliste = ttk.Treeview(listeFrame, columns=(
            "cid", "nom"), yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set, selectmode="browse")
        scroll_x.config(command=self.categorieliste.xview)
        scroll_y.config(command=self.categorieliste.yview)

        self.categorieliste.heading("cid", text="ID")
        self.categorieliste.heading("nom", text="Nom")


        self.categorieliste["show"]="headings"
        self.categorieliste.pack(fill=BOTH,expand=1)
        self.categorieliste.bind("<ButtonRelease-1>", self.get_donne)
        self.afficher()

        # Chargement de l'image
        icon_paths = r"C:\Users\ACER\Desktop\python\gestion_magazin\images\phone.jpg"
        icon_image1 = Image.open(icon_paths)
        new_size = (500, 290)
        icon_image1 = icon_image1.resize(new_size)  # Suppression du paramètre ANTIALIAS
        self.icon_title1 = ImageTk.PhotoImage(icon_image1)

        # Création de l'étiquette d'icône
        icon_label1 = tk.Label(self.root, bd=7, relief=RAISED, image =self.icon_title1)
        icon_label1.place(x=50, y=300)



        # Chargement de l'image
        icon_path = r"C:\Users\ACER\Desktop\python\gestion_magazin\images\admin.png"
        icon_image = Image.open(icon_path)
        new_size = (500, 290)
        icon_image = icon_image.resize(new_size)  # Suppression du paramètre ANTIALIAS
        self.icon_title = ImageTk.PhotoImage(icon_image)

        # Création de l'étiquette d'icône
        icon_label = tk.Label(self.root, bd=7, relief=RAISED, image=self.icon_title)
        icon_label.place(x=650, y=300)



        #fonction ajouter
    def ajouter(self):
            try:
                if self.var_nom.get() == "" :
                    messagebox.showerror("Erreur", "Veuillez saisir une categorie de produit")
                else:
                    self.cur.execute("select * from categorie where nom=%s", (self.var_nom.get(),))
                    row = self.cur.fetchone()
                    if row is not None:
                        messagebox.showerror("Erreur", "La categorie existe déjà")
                    else:
                        self.cur.execute(
                            "insert into categorie (nom ) values(%s)",
                            (
                                self.var_nom.get(),

                            ))
                        self.con.commit()
                        # Appel de la méthode afficher
                        self.afficher()
                        self.var_cat_idc.set("")
                        self.var_nom.set("")
                        messagebox.showinfo("Succès", "Enregistrement effectué avec succès")

            except Exception as ex:
                messagebox.showerror("Erreur", f"Erreur de connexion {str(ex)}")

    def afficher(self):
        try:
            self.cur.execute("select * from categorie ")
            rows = self.cur.fetchall()
            self.categorieliste.delete(*self.categorieliste.get_children())
            for row in rows:
                self.categorieliste.insert("", END, values=row)

        except Exception as ex:
            messagebox.showerror("Erreur", f"Erreur de connexion {str(ex)}")

    def get_donne(self, ev):
        r = self.categorieliste.focus()
        contenu = self.categorieliste.item(r)
        row = contenu["values"]
        self.var_cat_idc.set(row[0])
        self.var_nom.set(row[1])

        # Méthode pour supprimer une categorie

    def supprimer(self):
        try:
            if self.var_cat_idc.get() == "":
                messagebox.showerror("Erreur", "Veuillez sélectionner une catégorie à partir de la liste")
            else:
                self.cur.execute("SELECT * FROM categorie WHERE idc=%s", (self.var_cat_idc.get(),))
                row = self.cur.fetchone()
                if row is None:
                    messagebox.showerror("Erreur", "L'identifiant n'existe pas")
                else:
                    op = messagebox.askyesno("Confirmer", "Voulez-vous vraiment supprimer?")
                    if op:
                        self.cur.execute("DELETE FROM categorie WHERE idc=%s", (self.var_cat_idc.get(),))
                        self.con.commit()
                        self.afficher()
                        self.var_cat_idc.set("")
                        self.var_nom.set("")
                        messagebox.showinfo("Succès", "Suppression effectuée avec succès")
        except Exception as ex:
            messagebox.showerror("Erreur", f"Erreur de connexion {str(ex)}")


if __name__ == "__main__":
    root = tk.Tk()
    obj = Categorie(root)
    root.mainloop()