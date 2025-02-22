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
        root.geometry("1400x600+1200+400")
        root.config(bg="white")
        self.root.focus_force()


        ####les variables
        self.var_recheche_type = tk.StringVar()
        self.var_recheche_txt = tk.StringVar()
        self.var_pid = tk.StringVar()
        self.var_cat = tk.StringVar()
        self.var_four = tk.StringVar()
        self.var_nom = tk.StringVar()
        self.var_prix = tk.StringVar()
        self.var_qte = tk.StringVar()
        self.var_status = tk.StringVar()

        ##self.four_liste =[]
        ##self.four_liste()

        # Connexion à la base de données MySQL sur XAMPP
        self.con = mysql.connector.connect(
            host="localhost",
            port=3307,
            user="root",
            password="",
            database="gestion_magazin"
        )
        self.cur = self.con.cursor()

        produit_frame = tk.Frame(self.root, bd=2, relief=RIDGE, bg="white")
        produit_frame.place(x=10, y=10, width=650, height=560)

        titre = tk.Label(produit_frame, text="Details Produit", font=("goudy old style", 25, "bold"), bg="cyan").pack( side=TOP, fill=X)

        lbl_categorie = tk.Label(produit_frame, text="Catégorie", font=("goudy old style", 25), bg="white").place(x=30,
                                                                                                                  y=80)
        lbl_fournisseur = tk.Label(produit_frame, text="Fournisseur", font=("goudy old style", 25), bg="white").place(
            x=30, y=150)
        lbl_nomproduit = tk.Label(produit_frame, text="Nom", font=("goudy old style", 25), bg="white").place(x=30,
                                                                                                             y=220)
        lbl_prix = tk.Label(produit_frame, text="Prix", font=("goudy old style", 25), bg="white").place(x=30, y=290)
        lbl_quantite = tk.Label(produit_frame, text="Quantite", font=("goudy old style", 25), bg="white").place(x=30,
                                                                                                                y=360)
        lbl_status = tk.Label(produit_frame, text="Status", font=("goudy old style", 25), bg="white").place(x=30, y=430)

        self.cur.execute("select nom from categorie")
        rows = self.cur.fetchall()
        categorie_noms = [row[0] for row in rows]  # Récupération des noms de catégorie

        txt_categorie = ttk.Combobox(produit_frame, values=categorie_noms, textvariable=self.var_cat,state="r", justify=CENTER, font=("goudy old style", 20))
        txt_categorie.place(x=210, y=80, width=250)
        txt_categorie.set("Select")



        self.cur.execute("select nom from fournisseur")
        rows = self.cur.fetchall()
        fournisseur_noms = [row[0] for row in rows]
        txt_fournisseur = ttk.Combobox(produit_frame, values=fournisseur_noms,textvariable=self.var_four, state="r", justify=CENTER,font=("goudy old style", 20))
        txt_fournisseur.place(x=210, y=150, width=250)
        txt_fournisseur.set("Select")

        txt_nom = tk.Entry(produit_frame, font=("goudy old style", 20), textvariable=self.var_nom,bg="lightyellow").place(x=210, y=210, width=250)
        txt_prix = tk.Entry(produit_frame, font=("goudy old style", 20), textvariable=self.var_prix,bg="lightyellow").place(x=210, y=290,width=250)
        txt_quantite = tk.Entry(produit_frame, font=("goudy old style", 20),textvariable=self.var_qte, bg="lightyellow").place(x=210, y=370,width=250)


        txt_status = ttk.Combobox(produit_frame, values=["Active", "Inactive"],textvariable=self.var_status, justify=CENTER ,font=("goudy old style", 20))
        txt_status.place(x=210, y=430, width=250)
        txt_status.current(0)


        ###button
        self.ajouter_btn = tk.Button(produit_frame,text="Ajouter",state="normal",command=self.ajouter,font=("times new roman",20),bg="green",cursor="hand2")
        self.ajouter_btn.place(x=10,y=500,height=50,width=150)

        self.modifier_btn = tk.Button(produit_frame,command=self.modifier, text="Modifier", state="disabled", font=("times new roman", 20), bg="yellow", cursor="hand2")
        self.modifier_btn.place(x=170, y=500, height=50, width=150)

        self.supprimer_btn = tk.Button(produit_frame,command=self.supprimer, text="Supprimer", state="disabled", font=("times new roman", 20),bg="red", cursor="hand2")
        self.supprimer_btn.place(x=330, y=500, height=50, width=150)

        self.reinitialiser_btn = tk.Button(produit_frame,command=self.reini, text="Reinitialiser", font=("times new roman", 20),bg="lightgray", cursor="hand2")
        self.reinitialiser_btn.place(x=490, y=500, height=50, width=150)


        ####frame recherche
        recher_frame = tk.LabelFrame(self.root, text="Rechercher Produit",font=("times new roman",20),bd=2,relief=RIDGE,bg="white")
        recher_frame.place(x=700,y=10,width=660,height=90)


        txt_recher_option = ttk.Combobox(recher_frame, values=["categorie","fournisseur","nom"],textvariable=self.var_recheche_type, state="r", justify=CENTER, font=("goudy old style", 20))
        txt_recher_option.place(x=10, y=10, width=220)
        txt_recher_option.set("Select")

        txt_recher = tk.Entry(recher_frame,font=("goudy old style", 20),textvariable=self.var_recheche_txt, bg="lightyellow").place(x=255, y=10,  width=150)

        rechercher = tk.Button(recher_frame, command=self.rechercher,text="Rechercher",  font=("times new roman", 20), bg="blue",fg="white",cursor="hand2").place(x=420,y=5,height=40)
        tous = tk.Button(recher_frame, command=self.afficher,text="Tous", font=("times new roman", 20), bg="lightgray", cursor="hand2").place(x=575, y=5, height=40)



        ###listes fournisseurs
        listeFrame = tk.Frame(self.root, bd=3, relief=RIDGE)
        listeFrame.place(x=690, y=120, height=400, width=685)

        scroll_y = tk.Scrollbar(listeFrame, orient=VERTICAL)
        scroll_y.pack(side=RIGHT, fill=Y)

        scroll_x = tk.Scrollbar(listeFrame, orient=HORIZONTAL)
        scroll_x.pack(side=BOTTOM, fill=X)

        self.produitliste = ttk.Treeview(listeFrame, columns=("pid", "categorie", "fournisseur", "nom","prix","quantite","status"),
                                             yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        scroll_x.config(command=self.produitliste.xview)
        scroll_y.config(command=self.produitliste.yview)

        self.produitliste.heading("pid", text="ID")
        self.produitliste.heading("categorie", text="categorie")
        self.produitliste.heading("fournisseur", text="fournisseur")
        self.produitliste.heading("nom", text="nom")
        self.produitliste.heading("quantite", text="quantite")
        self.produitliste.heading("status", text="status")

        self.produitliste["show"] = "headings"
        self.produitliste.pack(fill=BOTH, expand=1)
        self.produitliste.bind("<ButtonRelease-1>", self.get_donne)
        self.afficher()


##def liste_four(self):
       ##  self.four_liste.append("vide")
    ##try:
       ## cur.execute("select nom from fournisseur")
        ##four = cur.fetchall()
        ##if len(four)>0:
          ##  del self.four_liste[:]
            ##self.four_liste.append("select")
            ##for i in four:
              ##  self.four_liste.append(i[0])
    ##except Exception as ex:
      ##  messagebox.showerror("Erreur", f"Erreur de connexion {str(ex)}")

    ###methode pour ajouter

    def ajouter(self):
        try:
            if self.var_cat.get() == "Select" or self.var_four.get() == "Select" or self.var_nom.get() == "":
                messagebox.showerror("Erreur", "Saisir les champs obligatoires")
            else:
                self.cur.execute("select * from produit where nom=%s", (self.var_nom.get(),))
                row = self.cur.fetchone()
                if row is not None:
                    messagebox.showerror("Erreur", "le produit existe déjà")
                else:
                    self.cur.execute(
                        "insert into produit (categorie,fournisseur ,nom,prix, quantite, status) values(%s,%s,%s,%s,%s,%s)",
                        (
                            self.var_cat.get(),
                            self.var_four.get(),
                            self.var_nom.get(),
                            self.var_prix.get(),
                            self.var_qte.get(),
                            self.var_status.get(),


                        ))
                    self.con.commit()
                    # Appel de la méthode afficher
                    self.afficher()
                    self.reini()
                    messagebox.showinfo("Succès", "Ajout effectué avec succès")

        except Exception as ex:
            messagebox.showerror("Erreur", f"Erreur de connexion {str(ex)}")

        ##fonction pour afficher

    def afficher(self):
        try:
            self.cur.execute("select * from produit ")
            rows = self.cur.fetchall()
            self.produitliste.delete(*self.produitliste.get_children())
            for row in rows:
                self.produitliste.insert("", END, values=row)

        except Exception as ex:
            messagebox.showerror("Erreur", f"Erreur de connexion {str(ex)}")


###function de configuration
    def get_donne(self, ev):
        self.ajouter_btn.config(state="disabled")
        self.modifier_btn.config(state="normal")
        self.supprimer_btn.config(state="normal")
        r = self.produitliste.focus()
        contenu = self.produitliste.item(r)
        row = contenu["values"]
        self.var_pid.set(row[0])
        self.var_cat.set(row[1])
        self.var_four.set(row[2])
        self.var_nom.set(row[3])
        self.var_prix.set(row[4])
        self.var_qte.set(row[5])
        self.var_status.set(row[6])

        ###fonction pour modifier
    def modifier(self):
            try:

                if self.var_pid.get()=="":
                    messagebox.showerror("Erreur", "Selection un ID ")

                else:
                 self.cur.execute("select * from produit where pid=%s",
                           (
                    self.var_pid.get(),
                ))
                row =self.cur.fetchone()

                if row==None:
                    messagebox.showerror("Erreur", "Veuillez selectionner un produit sur la liste ")
                else:
                 self.cur.execute("update produit set categorie=%s,fournisseur=%s ,nom=%s,prix=%s, quantite=%s, status=%s where pid=%s",(
                     self.var_cat.get(),
                     self.var_four.get(),
                     self.var_nom.get(),
                     self.var_prix.get(),
                     self.var_qte.get(),
                     self.var_status.get(),
                     self.var_pid.get(),
                 ))
                 self.con.commit()
                 self.afficher()
                 self.reini()
                messagebox.showinfo("Succès", "Modification effectuée avec succès")
            except Exception as ex:
                messagebox.showerror("Erreur", f"Erreur de connexion {str(ex)}")

            ###fonction qui permet de supprimer

    def supprimer(self):
        try:
            op = messagebox.askyesno("Confirmer", "Voulez-vous vraiment supprimer?")
            if op == True:
                self.cur.execute("DELETE FROM produit WHERE pid=%s", (self.var_pid.get(),))
                self.con.commit()
                self.afficher()
                self.reini()
                messagebox.showinfo("Succès", "Suppression effectuée avec succès")
        except Exception as ex:
            messagebox.showerror("Erreur", f"Erreur de connexion {str(ex)}")


        ###methode pour reinitialiser
    def reini(self):
            self.ajouter_btn.config(state="normal")
            self.modifier_btn.config(state="disabled")
            self.supprimer_btn.config(state="disabled")

            self.var_pid.set("")
            self.var_cat.set("Select")
            self.var_four.set("Select")
            self.var_nom.set("")
            self.var_prix.set("")
            self.var_qte.set("")
            self.var_status.set("Active")
            self.var_recheche_txt.set("")

 ###fonction permettant de faire des recherches
    def rechercher(self):
        try:
            if self.var_recheche_txt.get() == "":
                messagebox.showerror("Erreur", "Qu'est-ce que vous voulez rechercher?")
            else:
                # Requête SQL dynamique en fonction de l'option de recherche sélectionnée
                if self.var_recheche_type.get() == "categorie":
                    query = "select * from produit where categorie LIKE '%" + self.var_recheche_txt.get() + "%'"
                elif self.var_recheche_type.get() == "fournisseur":
                    query = "select * from produit where fournisseur LIKE '%" + self.var_recheche_txt.get() + "%'"
                elif self.var_recheche_type.get() == "nom":
                    query = "select * from produit where nom LIKE '%" + self.var_recheche_txt.get() + "%'"

                self.cur.execute(query)
                rows = self.cur.fetchall()
                if len(rows) != 0:
                    # Effacer le contenu précédent de la liste
                    self.produitliste.delete(*self.produitliste.get_children())
                    # Ajouter les nouveaux résultats à la liste
                    for row in rows:
                        self.produitliste.insert("", END, values=row)
                else:
                    messagebox.showerror("Erreur", "Aucun résultat trouvé")
        except Exception as ex:
            messagebox.showerror("Erreur", f"Erreur de connexion {str(ex)}")
if __name__ == "__main__":
    root = tk.Tk()
    obj = Produit(root)
    root.mainloop()
