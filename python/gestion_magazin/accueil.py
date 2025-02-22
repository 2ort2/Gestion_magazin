import tkinter as tk
from tkinter import messagebox, TOP, X, LEFT, BOTTOM
from tkinter import ttk

import mysql.connector
from PIL import Image, ImageTk
import datetime
import os


class Accueil:
    def __init__(self, root):
        self.root = root
        root.title("Accueil")
        root.geometry("2000x1800+0+0")
        root.config(bg="white")

        # Connexion à la base de données MySQL sur XAMPP
        self.con = mysql.connector.connect(
            host="localhost",
            port=3307,
            user="root",
            password="",
            database="gestion_magazin"
        )
        self.cur = self.con.cursor()


        # Load icon image
        icon_path = r"C:\Users\ACER\Desktop\python\gestion_magazin\images\icon.png"
        icon_image = Image.open(icon_path)
        new_size = (20, 20)
        icon_image = icon_image.resize(new_size)
        self.icon_title = ImageTk.PhotoImage(icon_image)

        # Create icon label
        icon_label = tk.Label(root, image=self.icon_title,
                              text="Gestion de magasin fortune",
                              font=("times new roman", 35, "bold"), bg="cyan",
                              anchor="w", padx=30, pady=20, width=1300, compound=tk.LEFT)
        icon_label.grid(row=0, column=0, columnspan=3)

        # Disconnect button
        disconnect_button = tk.Button(root, text="Deconnecter", command=self.deconnecter, font=("times new roman", 15, "bold"),
                                      cursor="hand2", bg="orange")
        disconnect_button.grid(row=0, column=2, sticky="e")

        # Time label
        self.time_label = tk.Label(root,
                                   text=f"Bienvenu chez rinoStore!\t\t Date : {datetime.date.today().strftime('%d-%m-%Y')}\t\t Heure : {datetime.datetime.now().strftime('%H:%M:%S')}",
                                   font=("times new roman", 15), fg="white", bg="black")
        self.time_label.place(x=0, y=100, relwidth=1, height=40)

        # Cadre du menu
        cadre_menu = tk.Frame(root, bd=2, relief=tk.RIDGE, bg="white")
        cadre_menu.place(x=0, y=140, width=350, height=530)

        # Load image for menu
        chemin_image_menu = r"C:\Users\ACER\Desktop\python\gestion_magazin\images\maxresdefault.jpg"
        image_menu = Image.open(chemin_image_menu)
        nouvelle_taille = (350, 200)
        image_menu = image_menu.resize(nouvelle_taille)
        self.photo_menu = ImageTk.PhotoImage(image_menu)
        etiquette_image_menu = tk.Label(cadre_menu, image=self.photo_menu)
        etiquette_image_menu.pack()

        # Load icon for button (resize to fit the button)
        image_bouton = Image.open(r"C:\Users\ACER\Desktop\python\gestion_magazin\images\direction.png")
        largeur_max, hauteur_max = 40, 40
        image_bouton.thumbnail((largeur_max, hauteur_max))
        self.icone_bouton = ImageTk.PhotoImage(image_bouton)

        # Create menu label (text)
        etiquette_menu = tk.Label(cadre_menu, text="Menu", font=("times new roman", 30, "bold"), bg="orange")
        etiquette_menu.pack(side=TOP, fill=X)

        # Create buttons
        bouton_employe = tk.Button(cadre_menu, text="Employé", command=self.ouvrir_employe, image=self.icone_bouton, padx=9,
                                   anchor="w", compound=LEFT, font=("times new roman", 15), bd=5, cursor="hand2", bg="white")
        bouton_employe.pack(side=TOP, fill=X)

        bouton_fournisseur = tk.Button(cadre_menu, text="Fournisseur",command=self.ouvrir_fournisseur, image=self.icone_bouton, padx=9, anchor="w",
                                       compound=LEFT, font=("times new roman", 15), bd=5, cursor="hand2",
                                       bg="white")
        bouton_fournisseur.pack(side=TOP, fill=X)

        bouton_categorie = tk.Button(cadre_menu, text="Categorie",command=self.ouvrir_categorie, image=self.icone_bouton, padx=9, anchor="w",
                                     compound=LEFT, font=("times new roman", 15), bd=5, cursor="hand2",
                                     bg="white")
        bouton_categorie.pack(side=TOP, fill=X)

        bouton_produit = tk.Button(cadre_menu, text="Produit",command=self.ouvrir_produit, image=self.icone_bouton, padx=9, anchor="w",
                                   compound=LEFT, font=("times new roman", 15), bd=5, cursor="hand2", bg="white")
        bouton_produit.pack(side=TOP, fill=X)

        bouton_caisse = tk.Button(cadre_menu, text="Caisse",command=self.ouvrir_caisse, image=self.icone_bouton, padx=9, anchor="w",
                                 compound=LEFT, font=("times new roman", 15), bd=5, cursor="hand2", bg="white")
        bouton_caisse.pack(side=TOP, fill=X)

        ##contenu
        self.lbl_totalemploye = tk.Label(root, text="Total Employés\n[0]",  # Texte du label
                                         bg="green", bd=5, relief=tk.RAISED, fg="white",  # Propriétés du label
                                         font=("goudy old style", 20, "bold"))
        self.lbl_totalemploye.place(x=500, y=200, height=100, width=200)  # Positionnement du label

        self.lbl_totalfournisseur = tk.Label(root, text="Total fournisseur\n[0]",  # Texte du label
                                             bg="red", bd=5, relief=tk.RAISED, fg="white",  # Propriétés du label
                                             font=("goudy old style", 20, "bold"))
        self.lbl_totalfournisseur.place(x=800, y=200, height=100, width=200)  # Positionnement du label

        self.lbl_totalcategorie = tk.Label(root, text="Total Categories\n[0]",  # Texte du label
                                           bg="gold", bd=5, relief=tk.RAISED, fg="white",  # Propriétés du label
                                           font=("goudy old style", 20, "bold"))
        self.lbl_totalcategorie.place(x=1100, y=200, height=100, width=200)  # Positionnement du label

        self.lbl_totalproduit = tk.Label(root, text="Total Produits\n[0]",  # Texte du label
                                         bg="gray", bd=5, relief=tk.RAISED, fg="white",  # Propriétés du label
                                         font=("goudy old style", 20, "bold"))
        self.lbl_totalproduit.place(x=650, y=400, height=100, width=200)  # Positionnement du label

        self.lbl_totalvente = tk.Label(root, text="Total Ventes\n[0]",  # Texte du label
                                       bg="blue", bd=5, relief=tk.RAISED, fg="white",  # Propriétés du label
                                       font=("goudy old style", 20, "bold"))
        self.lbl_totalvente.place(x=1000, y=400, height=100, width=200)  # Positionnement du label

        ## Pied de page (Footer)
       ## lbl_footer = tk.Label(self.root,
        ##  text="Développé par fortune\t\t\togboshalom@gmail.com\t\t\t +0022897759232\tCopyright 2024",
        ##font=("times new roman", 8), bg="black", fg="white").grid(sticky="S" + "E" + "W")

    def ouvrir_employe(self):
       self.obj = os.system("python C:/Users/ACER/Desktop/python/gestion_magazin/employe.py")

    def ouvrir_fournisseur(self):
        self.obj = os.system("python C:/Users/ACER/Desktop/python/gestion_magazin/fournisseur.py")

    def ouvrir_categorie(self):
        self.obj = os.system("python C:/Users/ACER/Desktop/python/gestion_magazin/categorie.py")

    def ouvrir_produit(self):
        self.obj = os.system("python C:/Users/ACER/Desktop/python/gestion_magazin/produit.py")

    def ouvrir_caisse(self):
        self.obj = os.system("python C:/Users/ACER/Desktop/python/gestion_magazin/caisse.py")


    def ouvrir_quitter(self):
        self.root.destroy()


    def deconnecter(self):
        self.root.destroy()
        self.obj = os.system("python C:/Users/ACER/Desktop/python/gestion_magazin/login.py")



    def modifier(self):
        try:
            self.cur.execute(" SELECT * from  produit ")
            produit = self.cur.fetchall()
            self.lbl_totalproduit.config(text=f"Total Produits\n[{str(len(produit))}]")

            self.cur.execute(" SELECT * from  categorie ")
            categorie = self.cur.fetchall()
            self.lbl_totalcategorie.config(text=f"Total Categories\n[{str(len(categorie))}]")

            self.cur.execute(" SELECT * from  fournisseur ")
            fournisseur = self.cur.fetchall()
            self.lbl_totalfournisseur.config(text=f"Total fournisseur\n[{str(len(fournisseur))}]")

            self.cur.execute(" SELECT * from  employe ")
            employe = self.cur.fetchall()
            self.lbl_totalemploye.config(text=f"Total Employés\n[{str(len(employe))}]")


            nombre_facture = len(os.listdir(r"C:\Users\ACER\Desktop\python\gestion_magazin\factures"))
            self.lbl_totalvente.config(text=f"Tot[{str(nombre_facture)}]")


        except Exception as ex:
            messagebox.showerror("Erreur", f"Erreur de connexion {str(ex)}")



if __name__ == "__main__":
    root = tk.Tk()
    obj = Accueil(root)
    root.mainloop()

