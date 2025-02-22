import tkinter as tk  # Alias 'tk' pour tkinter
from tkinter import messagebox, ttk

import datetime
from tkinter.constants import Y, RIDGE, VERTICAL, RIGHT, BOTTOM, X, HORIZONTAL, BOTH, END
import mysql.connector
from PIL import Image, ImageTk
import os
import tkinter as tk  # Alias 'tk' pour tkinter


class Fournisseur:
    def __init__(self, root):
        self.root = root
        root.title("Fournisseur")
        root.geometry("1200x600+300+500")
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

        # Déclaration des variables
        self.var_recherche_text = tk.StringVar()
        self.var_fourni_id = tk.StringVar()
        self.var_nom = tk.StringVar()
        self.var_contact = tk.StringVar()

        self.var_naissance = tk.StringVar()

        # Titre
        titre = tk.Label(self.root, text="Formulaire Fournisseur", font=("algerian", 20), cursor="hand2", bg="cyan")
        titre.place(x=0, y=0, relwidth=1)

        ###option de recherche
        reche_option = tk.Label(self.root, text="Recherche ID Fournisseur", font=("times new roman", 16), bg="white")
        reche_option.place(x=475, y=80)

        recher_txt = tk.Entry(self.root, textvariable=self.var_recherche_text, font=("times new roman", 16),
                              bg="lightyellow").place(x=730, y=80, height=40)
        recherche_btn = tk.Button(self.root, command=self.recherche,text="Rechercher", font=("times new roman", 16, "bold"), cursor="hand2",
                                  bg="blue", fg="white").place(x=977, y=80, height=40)
        tous_btn = tk.Button(self.root, command=self.afficher, text="Tous", font=("times new roman", 16, "bold"),
                             cursor="hand2",
                             bg="lightgray").place(x=1099, y=80, height=40)

        ####Contenu
        #1 ligne
        lbl_fourid = tk.Label(self.root, text="ID fournisseur", font=("goudy old style", 20), bg="white").place(x=20,
                                                                                                                y=70)
        self.txt_fourid = tk.Entry(self.root, textvariable=self.var_fourni_id, font=("goudy old style", 20),
                                   bg="lightyellow")
        self.txt_fourid.place(x=200, y=70, width=250)

        # 2 ligne
        lbl_nom = tk.Label(self.root, text="Nom", font=("goudy old style", 20), bg="white").place(x=20, y=140)
        txt_nom = tk.Entry(self.root, textvariable=self.var_nom, font=("goudy old style", 20), bg="lightyellow").place(
            x=200, y=140, width=250)

        # 3ligne
        lbl_contact = tk.Label(self.root, text="Contact", font=("goudy old style", 20), bg="white").place(x=20, y=210)
        txt_contact = tk.Entry(self.root, textvariable=self.var_contact, font=("goudy old style", 20),
                               bg="lightyellow").place(x=200, y=210, width=250)

        # 4 ligne
        lbl_description = tk.Label(self.root, text="Description", font=("goudy old style", 20), bg="white").place(x=20,
                                                                                                                  y=280)
        self.txt_description = tk.Text(self.root, font=("goudy old style", 20), bg="lightyellow")
        self.txt_description.place(x=200, y=280, width=600, height=100)

        ###Button
        self.ajout_btn = tk.Button(self.root, command=self.ajouter, text="Ajouter",
                                   font=("times new roman", 20, "bold"), cursor="hand2", bg="green", state="normal")
        self.ajout_btn.place(x=65, y=400, height=40, width=150)

        self.modifier_btn = tk.Button(self.root, command=self.modifier,text="Modifier", font=("times new roman", 20, "bold"), cursor="hand2",
                                      bg="yellow", state="disabled")
        self.modifier_btn.place(x=250, y=400, height=40, width=150)

        self.supprimer_btn = tk.Button(self.root,command=self.supprimer,text="Supprimer", font=("times new roman", 20, "bold"),
                                       cursor="hand2", bg="red", state="disabled")
        self.supprimer_btn.place(x=450, y=400, height=40, width=150)

        self.reinitialiser_btn = tk.Button(self.root,command=self.reini, text="Reinitialiser", font=("times new roman", 20, "bold"),
                                           cursor="hand2", bg="lightgray")
        self.reinitialiser_btn.place(x=650, y=400, height=40, width=150)

        ###listes fournisseurs
        listeFrame = tk.Frame(self.root, bd=3, relief=RIDGE)
        listeFrame.place(x=820, y=150, height=400, width=365)

        scroll_y = tk.Scrollbar(listeFrame, orient=VERTICAL)
        scroll_y.pack(side=RIGHT, fill=Y)

        scroll_x = tk.Scrollbar(listeFrame, orient=HORIZONTAL)
        scroll_x.pack(side=BOTTOM, fill=X)

        self.fournisseurliste = ttk.Treeview(listeFrame, columns=("forid", "nom", "contact", "description"),
                                             yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        scroll_x.config(command=self.fournisseurliste.xview)
        scroll_y.config(command=self.fournisseurliste.yview)

        self.fournisseurliste.heading("forid", text="ID")
        self.fournisseurliste.heading("nom", text="nom")
        self.fournisseurliste.heading("contact", text="contact")
        self.fournisseurliste.heading("description", text="description")

        self.fournisseurliste["show"] = "headings"
        self.fournisseurliste.pack(fill=BOTH, expand=1)
        self.fournisseurliste.bind("<ButtonRelease-1>", self.get_donne)

        ###methode pour ajouter

    def ajouter(self):
        try:
            if self.var_fourni_id.get() == "" or self.var_nom.get() == "" or self.var_contact.get() == "":
                messagebox.showerror("Erreur", "Veuillez mettre un ID, un mot de passe et un type")
            else:
                self.cur.execute("select * from fournisseur where forid=%s", (self.var_fourni_id.get(),))
                row = self.cur.fetchone()
                if row is not None:
                    messagebox.showerror("Erreur", "L'ID fournisseur existe déjà")
                else:
                    self.cur.execute(
                        "insert into fournisseur (forid, nom, contact, description) values(%s,%s,%s,%s)",
                        (
                            self.var_fourni_id.get(),
                            self.var_nom.get(),
                            self.var_contact.get(),
                            self.txt_description.get("1.0", END),

                        ))
                    self.con.commit()
                    # Appel de la méthode afficher
                    self.afficher()
                    ###self.reini()
                    messagebox.showinfo("Succès", "Ajout effectué avec succès")

        except Exception as ex:
            messagebox.showerror("Erreur", f"Erreur de connexion {str(ex)}")

            ##fonction pour afficher


    def afficher(self):
                try:
                    self.cur.execute("select * from fournisseur ")
                    rows = self.cur.fetchall()
                    self.fournisseurliste.delete(*self.fournisseurliste.get_children())
                    for row in rows:
                        self.fournisseurliste.insert("", END, values=row)

                except Exception as ex:
                    messagebox.showerror("Erreur", f"Erreur de connexion {str(ex)}")


    def get_donne(self, ev):
        self.ajout_btn.config(state="disabled")
        self.modifier_btn.config(state="normal")
        self.supprimer_btn.config(state="normal")
        self.txt_fourid.config(state="readonly")
        r = self.fournisseurliste.focus()
        contenu = self.fournisseurliste.item(r)
        row = contenu["values"]

        self.var_fourni_id.set(row[0]),
        self.var_nom.set(row[1]),
        self.var_contact.set(row[2]),
        self.txt_description.delete("1.0",END),
        self.txt_description.insert(END,row[3]),

 ###fonction pour modifier
    def modifier(self):
        try:
                self.cur.execute("""
                        UPDATE fournisseur 
                        SET nom=%s, contact=%s, description=%s 
                        WHERE forid=%s
                    """, (
                    self.var_nom.get(),
                    self.var_contact.get(),
                    self.txt_description.get("1.0", END),
                    self.var_fourni_id.get(),
                ))
                self.con.commit()
                self.afficher()
               ### self.reini()
                messagebox.showinfo("Succès", "Modification effectuée avec succès")
        except Exception as ex:
                messagebox.showerror("Erreur", f"Erreur de connexion {str(ex)}")



###fonction qui permet de supprimer
    def supprimer(self):
        try:
            op = messagebox.askyesno("Confirmer", "Voulez-vous vraiment supprimer?")
            if op == True:
                self.cur.execute("DELETE FROM fournisseur WHERE forid=%s", (self.var_fourni_id.get(),))
                self.con.commit()
                self.afficher()
                ###self.reini()
                messagebox.showinfo("Succès", "Suppression effectuée avec succès")
        except Exception as ex:
            messagebox.showerror("Erreur", f"Erreur de connexion {str(ex)}")



###methode pour reinitialiser
    def reini(self):
        self.txt_fourid.config(state ="normal")
        self.ajout_btn.config(state="normal")
        self.modifier_btn.config(state="disabled")
        self.supprimer_btn.config(state="disabled")
        self.var_nom.set(""),
        self.var_contact.set(""),
        self.txt_description.delete("1.0", END),
        self.var_fourni_id.set(""),
        self.var_recherche_text.set(""),



  ##methode pour recherche
    def recherche(self):
        try:
            if self.var_recherche_text.get() == "":
                messagebox.showerror("Erreur", "Veillez saisir dans le champ recherche")
            else:
                query = "SELECT * FROM fournisseur WHERE forid LIKE '%" + self.var_recherche_text.get() + "%' OR nom LIKE '%" + self.var_recherche_text.get() + "%'"
                self.cur.execute(query)
                rows = self.cur.fetchall()
                if len(rows) != 0:
                    self.fournisseurliste.delete(*self.fournisseurliste.get_children())
                    for row in rows:
                        self.fournisseurliste.insert("", END, values=row)
                else:
                    messagebox.showerror("Erreur", "Aucun resultat trouvé")

        except Exception as ex:
            messagebox.showerror("Erreur", f"Erreur de connexion {str(ex)}")



if __name__ == "__main__":
    root = tk.Tk()
    obj = Fournisseur(root)
    root.mainloop()
