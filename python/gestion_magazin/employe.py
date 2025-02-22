import tkinter as tk
from tkinter import messagebox, ttk
from tkinter.constants import RIDGE, CENTER, VERTICAL, HORIZONTAL, RIGHT, Y, BOTTOM, X, BOTH, END

import mysql.connector


class Employe:
    def __init__(self, root):
        self.root = root
        root.title("Employe")
        root.geometry("1200x700+300+500")
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
        self.var_recherche_type = tk.StringVar()
        self.var_recherche_txt = tk.StringVar()
        self.var_emplo_id = tk.StringVar()
        self.var_sexe = tk.StringVar()
        self.var_contact = tk.StringVar()
        self.var_nom = tk.StringVar()
        self.var_naissance = tk.StringVar()
        self.var_adhesion = tk.StringVar()
        self.var_email = tk.StringVar()
        self.var_password = tk.StringVar()
        self.var_type = tk.StringVar()
        self.var_salaire = tk.StringVar()

        # Frame recherche
        reche_frame = tk.LabelFrame(self.root, text="Recherche Employé", font=("goudy old style", 20, "bold"), bd=2,
                                    relief=RIDGE, bg="white")
        reche_frame.place(x=230, y=20, width=750, height=90)

        # Option de recherche
        reche_option = ttk.Combobox(reche_frame, textvariable=self.var_recherche_type,
                                    values=("nom", "prenom", "email", "contact"), font=("times new roman", 20),
                                    state="r", justify=CENTER)
        reche_option.set("Selection")
        reche_option.place(x=10, y=10, width=200)

        reche_txt = tk.Entry(reche_frame, textvariable=self.var_recherche_txt, font=("times new roman", 20),
                             bg="lightyellow").place(x=235, y=10, width=200)
        recherche = tk.Button(reche_frame,command=self.recherche, text="Recherche", font=("times new roman", 20), cursor="hand2", bg="blue",
                              fg="white").place(x=450, y=5, height=40)
        tous = tk.Button(reche_frame, command=self.afficher, text="Tous", font=("times new roman", 20), cursor="hand2",
                         bg="lightgray").place(x=600, y=5, height=40)

        # Titre
        titre = tk.Label(self.root, text="Formulaire Employé", font=("times new roman", 20), cursor="hand2", bg="cyan")
        titre.place(x=0, y=150, relwidth=1)

        # Contenu

        # 1ère ligne
        lbl_empId = tk.Label(self.root, text="ID Employe", font=("goudy old style", 20), bg="white").place(x=10, y=220,
                                                                                                           width=150)
        lbl_sexe = tk.Label(self.root, text="Sexe", font=("goudy old style", 20), bg="white").place(x=400, y=220,
                                                                                                    width=150)
        lbl_contact = tk.Label(self.root, text="Contact", font=("goudy old style", 20), bg="white").place(x=770, y=220,
                                                                                                          width=150)

        self.txt_empId = tk.Entry(self.root, textvariable=self.var_emplo_id, font=("goudy old style", 20),
                                  bg="lightyellow")
        self.txt_empId.place(x=160, y=220, width=250)
        txt_sexe = ttk.Combobox(self.root, textvariable=self.var_sexe, values=("homme", "femme"),
                                font=("goudy old style", 20), state="r", justify=CENTER)
        txt_sexe.set("Selection")
        txt_sexe.place(x=530, y=220, width=250)
        txt_contact = tk.Entry(self.root, textvariable=self.var_contact, font=("goudy old style", 20),
                               bg="lightyellow").place(x=920, y=220, width=250)

        # 2ème ligne
        lbl_nom = tk.Label(self.root, text="Nom", font=("goudy old style", 20), bg="white").place(x=15, y=290,
                                                                                                  width=150)
        lbl_naissance = tk.Label(self.root, text="Birthdate", font=("goudy old style", 20), bg="white").place(x=400,
                                                                                                              y=290,
                                                                                                              width=150)
        lbl_adhesion = tk.Label(self.root, text="Signindate", font=("goudy old style", 20), bg="white").place(x=770,
                                                                                                              y=290,
                                                                                                              width=150)

        txt_nom = tk.Entry(self.root, textvariable=self.var_nom, font=("goudy old style", 20), bg="lightyellow").place(
            x=160, y=290, width=250)
        txt_naissance = tk.Entry(self.root, textvariable=self.var_naissance, font=("goudy old style", 20),
                                 bg="lightyellow").place(x=530, y=290, width=250)
        txt_adhesion = tk.Entry(self.root, textvariable=self.var_adhesion, font=("goudy old style", 20),
                                bg="lightyellow").place(x=920, y=290, width=250)

        # 3ème ligne
        lbl_email = tk.Label(self.root, text="Email", font=("goudy old style", 20), bg="white").place(x=15, y=360,
                                                                                                      width=150)
        lbl_password = tk.Label(self.root, text="Password", font=("goudy old style", 20), bg="white").place(x=400,
                                                                                                            y=360,
                                                                                                            width=150)
        lbl_type = tk.Label(self.root, text="Type", font=("goudy old style", 20), bg="white").place(x=770, y=360,
                                                                                                    width=150)

        txt_email = tk.Entry(self.root, textvariable=self.var_email, font=("goudy old style", 20),
                             bg="lightyellow").place(x=160, y=360, width=250)
        txt_password = tk.Entry(self.root, textvariable=self.var_password, font=("goudy old style", 20),
                                bg="lightyellow").place(x=530, y=360, width=250)
        txt_type = ttk.Combobox(self.root, textvariable=self.var_type, values=("Admin", "Employe"),
                                font=("goudy old style", 20), state="r", justify=CENTER)
        txt_type.set("Selection")
        txt_type.place(x=920, y=360, width=250)

        # 4ème ligne
        lbl_adresse = tk.Label(self.root, text="Adresse", font=("goudy old style", 20), bg="white").place(x=15, y=430,
                                                                                                          width=150)
        lbl_salaire = tk.Label(self.root, text="Salaire", font=("goudy old style", 20), bg="white").place(x=400, y=430,
                                                                                                          width=150)

        self.txt_adresse = tk.Text(self.root, font=("goudy old style", 20), bg="lightyellow")
        self.txt_adresse.place(x=160, y=430, width=250, height=115)
        txt_salaire = tk.Entry(self.root, textvariable=self.var_salaire, font=("goudy old style", 20),
                               bg="lightyellow").place(x=530, y=430, width=250)

        # Boutons d'action
        self.ajout_btn = tk.Button(self.root, command=self.ajouter, state="normal", text="Ajouter",
                                   font=("times new roman", 20, "bold"), cursor="hand2", bg="green")
        self.ajout_btn.place(x=450, y=500, height=48)
        self.modifier_btn = tk.Button(self.root, command=self.modifier, text="Modifier", state="disabled",
                                      font=("times new roman", 20, "bold"), cursor="hand2", bg="yellow")
        self.modifier_btn.place(x=620, y=500, height=48)
        self.supprimer_btn = tk.Button(self.root, command=self.supprimer, text="Supprimer", state="disabled",
                                       font=("times new roman", 20, "bold"), cursor="hand2", bg="red")
        self.supprimer_btn.place(x=800, y=500, height=48)
        reini_btn = tk.Button(self.root,command=self.reini, text="Reinitialiser", font=("times new roman", 20, "bold"), cursor="hand2",
                              bg="lightgray").place(x=1000, y=500, height=48)

        # Liste des employés
        listeFrame = tk.Frame(self.root, bd=3, relief=RIDGE)
        listeFrame.place(x=0, y=550, height=150, relwidth=1)

        scroll_y = tk.Scrollbar(listeFrame, orient=VERTICAL)
        scroll_y.pack(side=RIGHT, fill=Y)

        scroll_x = tk.Scrollbar(listeFrame, orient=HORIZONTAL)
        scroll_x.pack(side=BOTTOM, fill=X)

        self.employeliste = ttk.Treeview(listeFrame, columns=(
            "id", "nom", "email", "sexe", "contact", "naissance", "adhesion", "password", "type", "adresse",
            "salaire"), yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set, selectmode="browse")
        scroll_x.config(command=self.employeliste.xview)
        scroll_y.config(command=self.employeliste.yview)

        self.employeliste.heading("id", text="ID")
        self.employeliste.heading("nom", text="Nom")
        self.employeliste.heading("email", text="Email")
        self.employeliste.heading("sexe", text="Sexe")
        self.employeliste.heading("contact", text="Contact")
        self.employeliste.heading("naissance", text="Naissance")
        self.employeliste.heading("adhesion", text="Adhesion")
        self.employeliste.heading("password", text="Password")
        self.employeliste.heading("type", text="Type")
        self.employeliste.heading("adresse", text="Adresse")
        self.employeliste.heading("salaire", text="Salaire")

        self.employeliste["show"] = "headings"
        self.employeliste.bind("<ButtonRelease-1>", self.get_donne)

        self.employeliste.pack(fill=BOTH, expand=1)
        # Appel de la méthode afficher
        self.afficher()

        # Scrollbar horizontal
        self.employeliste.configure(xscrollcommand=scroll_x.set)

    # Méthode pour ajouter un employé
    def ajouter(self):
        try:
            if self.var_emplo_id.get() == "" or self.var_password.get() == "" or self.var_type.get() == "":
                messagebox.showerror("Erreur", "Veuillez mettre un ID, un mot de passe et un type")
            else:
                self.cur.execute("select * from employe where id=%s", (self.var_emplo_id.get(),))
                row = self.cur.fetchone()
                if row is not None:
                    messagebox.showerror("Erreur", "L'ID employé existe déjà")
                else:
                    self.cur.execute(
                        "insert into employe (id, nom, email, sexe, contact, naissance, adhesion, password, type, adresse, salaire) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                        (
                            self.var_emplo_id.get(),
                            self.var_nom.get(),
                            self.var_email.get(),
                            self.var_sexe.get(),
                            self.var_contact.get(),
                            self.var_naissance.get(),
                            self.var_adhesion.get(),
                            self.var_password.get(),
                            self.var_type.get(),
                            self.txt_adresse.get("1.0", END),
                            self.var_salaire.get()
                        ))
                    self.con.commit()
                    # Appel de la méthode afficher
                    self.afficher()
                    self.reini()
                    messagebox.showinfo("Succès", "Ajout effectué avec succès")

        except Exception as ex:
            messagebox.showerror("Erreur", f"Erreur de connexion {str(ex)}")

    # Méthode pour afficher la liste des employés
    def afficher(self):
        try:
            self.cur.execute("select * from employe ")
            rows = self.cur.fetchall()
            self.employeliste.delete(*self.employeliste.get_children())
            for row in rows:
                self.employeliste.insert("", END, values=row)

        except Exception as ex:
            messagebox.showerror("Erreur", f"Erreur de connexion {str(ex)}")

    def get_donne(self, ev):
        self.ajout_btn.config(state="disabled")
        self.modifier_btn.config(state="normal")
        self.supprimer_btn.config(state="normal")
        self.txt_empId.config(state="readonly")
        r = self.employeliste.focus()
        contenu = self.employeliste.item(r)
        row = contenu["values"]

        if row:
            self.var_emplo_id.set(row[0])
            self.var_nom.set(row[1])
            self.var_email.set(row[2])
            self.var_sexe.set(row[3])
            self.var_contact.set(row[4])
            self.var_naissance.set(row[5])
            self.var_adhesion.set(row[6])
            self.var_password.set(row[7])
            self.var_type.set(row[8])
            self.txt_adresse.delete("1.0", END)
            self.txt_adresse.insert(END, row[9])
            self.var_salaire.set(row[10])
    # Méthode pour modifier un employé
    def modifier(self):
        try:
            self.cur.execute("""
                UPDATE employe 
                SET nom=%s, email=%s, sexe=%s, contact=%s, naissance=%s, adhesion=%s, password=%s, type=%s, adresse=%s, salaire=%s 
                WHERE id=%s
            """, (
                self.var_nom.get(),
                self.var_email.get(),
                self.var_sexe.get(),
                self.var_contact.get(),
                self.var_naissance.get(),
                self.var_adhesion.get(),
                self.var_password.get(),
                self.var_type.get(),
                self.txt_adresse.get("1.0", END),
                self.var_salaire.get(),
                self.var_emplo_id.get(),
            ))
            self.con.commit()
            self.afficher()
            self.reini()
            messagebox.showinfo("Succès", "Modification effectuée avec succès")
        except Exception as ex:
            messagebox.showerror("Erreur", f"Erreur de connexion {str(ex)}")

    # Méthode pour supprimer un employé
    def supprimer(self):
        try:
            op = messagebox.askyesno("Confirmer", "Voulez-vous vraiment supprimer?")
            if op == True:
                self.cur.execute("DELETE FROM employe WHERE id=%s", (self.var_emplo_id.get(),))
                self.con.commit()
                self.afficher()
                self.reini()
                messagebox.showinfo("Succès", "Suppression effectuée avec succès")
        except Exception as ex:
            messagebox.showerror("Erreur", f"Erreur de connexion {str(ex)}")

    ###methode pour reinitialiser
    def reini(self):
        self.txt_empId.config(state="normal")
        self.ajout_btn.config(state="normal")
        self.modifier_btn.config(state="disabled")
        self.supprimer_btn.config(state="disabled")
        self.var_nom.set(""),
        self.var_email.set(""),
        self.var_sexe.set("Selection"),
        self.var_contact.set(""),
        self.var_naissance.set(""),
        self.var_adhesion.set(""),
        self.var_password.set(""),
        self.var_type.set("Selection"),
        self.txt_adresse.delete("1.0", END),
        self.var_salaire.set(""),
        self.var_emplo_id.set(""),
        self.var_recherche_txt.set(""),
        self.var_recherche_type.set("nom")


    ##methode pour recherche
    def recherche(self):
        try:
            if self.var_recherche_txt.get() == "":
                messagebox.showerror("Erreur", "Veillez saisir dans le champ recherche")
            else:
                self.cur.execute(
                    "SELECT * FROM employe WHERE " + self.var_recherche_type.get() + " LIKE '%" + self.var_recherche_txt.get() + "%'")
                rows = self.cur.fetchall()
                if len(rows) != 0:
                    self.employeliste.delete(*self.employeliste.get_children())
                    for row in rows:
                        self.employeliste.insert("", END, values=row)
                else:
                    messagebox.showerror("Erreur", "Aucun resultat trouvé")

        except Exception as ex:
            messagebox.showerror("Erreur", f"Erreur de connexion {str(ex)}")


if __name__ == "__main__":
    root = tk.Tk()
    obj = Employe(root)
    root.mainloop()
