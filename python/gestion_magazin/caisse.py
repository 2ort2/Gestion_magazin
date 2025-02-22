import tempfile
import time
import tkinter as tk
from tkinter import messagebox, TOP, X, LEFT, BOTTOM
from tkinter import ttk
from tkinter.constants import RIDGE, RIGHT, VERTICAL, Y, HORIZONTAL, BOTH, END

import mysql.connector
from PIL import Image, ImageTk
import datetime
import os


class Caisse:
    def __init__(self, root, GRDOVE=None):
        self.root = root
        root.title("Caisse")
        root.geometry("1300x700+800+400")
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


        self.cart_list = []
        self.tk_print = 0
        ###title
        # Load icon image
        icon_path = r"C:\Users\ACER\Desktop\python\gestion_magazin\images\icon.png"
        icon_image = Image.open(icon_path)
        new_size = (25, 25)
        icon_image = icon_image.resize(new_size)
        self.icon_title = ImageTk.PhotoImage(icon_image)

        # Create icon label
        icon_label = tk.Label(root, image=self.icon_title,text="Caisse Magasin",
                              font=("times new roman", 25, "bold"), bg="cyan",
                              anchor="w", padx=25, pady=20, width=1300, compound=tk.LEFT)
        icon_label.grid(row=0, column=0, columnspan=8)

        # Disconnect button
        disconnect_button = tk.Button(root, text="Deconnecter", command=self.deconnecter,
                                      font=("times new roman", 15, "bold"), cursor="hand2", bg="orange")
        disconnect_button.grid(row=0, column=6, sticky="e")

        # Time label
        self.time_label = tk.Label(root, text=f"Bienvenu chez rinoStore!\t\t Date : {datetime.date.today().strftime('%d-%m-%Y')}\t\t Heure : {datetime.datetime.now().strftime('%H:%M:%S')}",
        font=("times new roman", 15), fg="white", bg="black")
        self.time_label.place(x=0, y=80, relwidth=1, height=40)
        self.modifier_heure()



        ####produit

        self.var_recherche = tk.StringVar()

        ProduitFrame1 = tk.Frame(self.root, bd=4, relief=RIDGE, bg="white")
        ProduitFrame1.place(x=10,y=130,width=608,height=565)


        ptitre = tk.Label(ProduitFrame1, text="Tous les produits", font=("goudy old style", 20, "bold"), bg="cyan", bd=3, relief=RIDGE).pack(side=TOP, fill=X)



        ProduitFrame2= tk.Frame(self.root, bd=4, relief=RIDGE, bg="white")
        ProduitFrame2.place(x=18, y=183, width=593, height=150)


        lbl_recherche = tk.Label(ProduitFrame2, text="Recherche Produit | Par Nom", font=("goudy old style",20,"bold"),bg="green",fg="white",bd=3,relief=RIDGE).place(x=2,y=20)
        lbl_nom = tk.Label(ProduitFrame2, text="Nom Produit",  font=("goudy old style", 20, "bold"), bg="white").place(x=2, y=80)


        txt_recherche =tk.Entry(ProduitFrame2,textvariable=self.var_recherche,font=("goudy old style",20),bg="lightyellow").place(x=160,y=80,width=150)
        recherche_btn = tk.Button(ProduitFrame2,command=self.rechercher,text="Recherche",font=("times new roman",20),bg="green",cursor="hand2").place(x=320,y=80,width=120,height=35)
        tous_btn = tk.Button(ProduitFrame2,command=self.afficher,text="Tous",font=("times new roman",20),bg="lightgray",cursor="hand2").place(x=450,y=80,width=120,height=35)


        ###listes produits
        produitFrame3 = tk.Frame(ProduitFrame1, bd=3, relief=RIDGE)
        produitFrame3.place(x=2, y=200, height=320, width=600)

        scroll_y = tk.Scrollbar(produitFrame3, orient=VERTICAL)
        scroll_y.pack(side=RIGHT, fill=Y)

        scroll_x = tk.Scrollbar(produitFrame3, orient=HORIZONTAL)
        scroll_x.pack(side=BOTTOM, fill=X)

        self.produit_table = ttk.Treeview(produitFrame3, columns=(
        "pid", "nom", "prix", "quantite", "status"),
                                         yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        scroll_x.config(command=self.produit_table.xview)
        scroll_y.config(command=self.produit_table.yview)

        self.produit_table.heading("pid", text="ID",anchor="w")
        self.produit_table.heading("nom", text="nom",anchor="w")
        self.produit_table.heading("prix", text="prix",anchor="w")
        self.produit_table.heading("quantite", text="quantite",anchor="w")
        self.produit_table.heading("status", text="status",anchor="w")

        self.produit_table["show"] = "headings"
        self.produit_table.pack(fill=BOTH, expand=1)
        self.produit_table.bind("<ButtonRelease-1>", self.get_donne)
        self.afficher()

        lbl_note =tk.Label(ProduitFrame1, text="Note : 'Entrer la quantité pour retirer le produit du panier'",anchor="w",font=("times new roman",15),bg="white",fg="red").pack(side=BOTTOM,fill=X)

        ########Frame Client
        self.var_cname = tk.StringVar()
        self.var_contact = tk.StringVar()

        Client_frame = tk.Frame(self.root, bd=4,relief=RIDGE,bg="white")
        Client_frame.place(x=622,y=130,width=464,height=90)

        ctitle =tk.Label(Client_frame,text="Détails du Client",font=("goudy old style",15),bg="lightgray",bd=3,relief=RIDGE).pack(side=TOP,fill=X)

        lbl_nom = tk.Label(Client_frame, text="Nom", font=("goudy old style", 15), bg="black").place(x=20,y=40)
        txt_nom = tk.Entry(Client_frame,textvariable=self.var_cname,font=("goudy old style",15),bg="lightgray").place(x=55,y=40,width=170)

        lbl_contact = tk.Label(Client_frame,text="Tél", font=("goudy old style", 15), bg="white").place(x=245, y=40)
        txt_contact = tk.Entry(Client_frame,textvariable=self.var_contact, font=("goudy old style", 15), bg="lightgray").place(x=280, y=40, width=170)


        ####calculatrice
        self.var_cal_input = tk.StringVar()

        Calcul_cart_frame = tk.Frame(self.root,bd=4,relief=RIDGE,bg="white")
        Calcul_cart_frame.place(x=622,y=208,width=464,height=360)

        Calculframe = tk.Frame(Calcul_cart_frame ,bd=4, relief=RIDGE, bg="white")
        Calculframe.place(x=10, y=10, width=248, height=320)

        self.txt_cal_input = tk.Entry(Calculframe, textvariable=self.var_cal_input,font=("arial",15,"bold"),justify=RIGHT,bg="lightyellow",bd=10,relief=GRDOVE,state="readonly")
        self.txt_cal_input.grid(row=0,columnspan=4)


        self.btn_7 = tk.Button(Calculframe,text="7",font=("arial",12,"bold"),bg="gray",cursor="hand2",width=5,pady=14,command=lambda:self.get_input(7)).grid(row=1,column=0)
        self.btn_8 = tk.Button(Calculframe, text="8", font=("arial", 12, "bold"), bg="gray", cursor="hand2", width=5,pady=14,command=lambda :self.get_input(8)).grid(row=1, column=1)
        self.btn_9 = tk.Button(Calculframe, text="9", font=("arial", 12, "bold"), bg="gray", cursor="hand2", width=5, pady=14,command=lambda :self.get_input(9)).grid(row=1, column=2)
        self.btn_add = tk.Button(Calculframe, text="+", font=("arial", 12, "bold"), bg="gray", cursor="hand2", width=5,pady=14,command=lambda :self.get_input("+")).grid(row=1, column=3)

        self.btn_4 = tk.Button(Calculframe, text="4", font=("arial", 12, "bold"), bg="gray", cursor="hand2", width=5, pady=14,command=lambda :self.get_input(4)).grid(row=2, column=0)
        self.btn_5 = tk.Button(Calculframe, text="5", font=("arial", 12, "bold"), bg="gray", cursor="hand2", width=5, pady=14,command=lambda :self.get_input(5)).grid(row=2, column=1)
        self.btn_6 = tk.Button(Calculframe, text="6", font=("arial", 12, "bold"), bg="gray", cursor="hand2", width=5, pady=14,command=lambda :self.get_input(6)).grid(row=2, column=2)
        self.btn_soust = tk.Button(Calculframe, text="-", font=("arial", 12, "bold"), bg="gray", cursor="hand2", width=5,pady=14,command=lambda :self.get_input("-")).grid(row=2, column=3)

        self.btn_1 = tk.Button(Calculframe, text="1", font=("arial", 12, "bold"), bg="gray", cursor="hand2", width=5,  pady=14,command=lambda :self.get_input(1)).grid(row=3, column=0)
        self.btn_2 = tk.Button(Calculframe, text="2", font=("arial", 12, "bold"), bg="gray", cursor="hand2", width=5, pady=14,command=lambda:self.get_input(2)).grid(row=3, column=1)
        self.btn_3 = tk.Button(Calculframe, text="3", font=("arial", 12, "bold"), bg="gray", cursor="hand2", width=5,pady=14,command=lambda :self.get_input(3)).grid(row=3, column=2)
        self.btn_mult = tk.Button(Calculframe, text="*", font=("arial", 12, "bold"), bg="gray", cursor="hand2", width=5, pady=14,command=lambda :self.get_input("*")).grid(row=3, column=3)

        self.btn_0 = tk.Button(Calculframe, text="0", font=("arial", 12, "bold"), bg="gray", cursor="hand2", width=5,pady=14,command=lambda :self.get_input(0)).grid(row=4, column=0)
        self.btn_C = tk.Button(Calculframe, text="C", font=("arial", 12, "bold"), bg="gray", cursor="hand2", width=5,pady=14,command=self.clear_call).grid(row=4, column=1)
        self.btn_egal = tk.Button(Calculframe, text="=", font=("arial", 12, "bold"), bg="gray", cursor="hand2", width=5,pady=14,command=self.resultat).grid(row=4, column=2)
        self.btn_div = tk.Button(Calculframe, text="/", font=("arial", 12, "bold"), bg="gray", cursor="hand2", width=5,pady=14,command=lambda :self.get_input("/")).grid(row=4, column=3)

        cart_frame = tk.Frame(Calcul_cart_frame,bd=5,relief=RIDGE)
        cart_frame.place(x=260,y=10,height=340,width=200)

        self.ctitle = tk.Label(cart_frame, text="Produit \n Total du Panier :[0]", font=("goudy old style", 15), bg="lightyellow", bd=3,relief=RIDGE)
        self.ctitle.pack(side=TOP, fill=X)



        ###scroll
        cart_frame = tk.Frame(Calcul_cart_frame, bd=3, relief=RIDGE)
        cart_frame.place(x=262, y=72, height=256, width=192)

        scroll_y = tk.Scrollbar(cart_frame, orient=VERTICAL)
        scroll_y.pack(side=RIGHT, fill=Y)

        scroll_x = tk.Scrollbar(cart_frame, orient=HORIZONTAL)
        scroll_x.pack(side=BOTTOM, fill=X)

        self.cartTable = ttk.Treeview(cart_frame, columns=(
            "pid", "nom", "prix", "quantite", "status"),
               yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        scroll_x.config(command=self.cartTable.xview)
        scroll_y.config(command=self.cartTable.yview)

        self.cartTable.heading("pid", text="ID", anchor="w")
        self.cartTable.heading("nom", text="nom", anchor="w")
        self.cartTable.heading("prix", text="prix", anchor="w")
        self.cartTable.heading("quantite", text="quantite", anchor="w")
        self.cartTable.heading("status", text="status", anchor="w")

        self.cartTable["show"] = "headings"
        self.cartTable.pack(fill=BOTH, expand=1)

        self.cartTable.bind("<ButtonRelease-1>", self.get_donne_cart)
        


        ###Ajouter Button cart(ajout du panier)
        self.var_pid = tk.StringVar()
        self.var_pname = tk.StringVar()
        self.var_prix = tk.StringVar()
        self.var_qte = tk.StringVar()
        self.var_stock = tk.StringVar()

        Button_Frame = tk.Frame(self.root,bd=4,relief=RIDGE,bg="white")
        Button_Frame.place(x=622,y=570,width=467,height=123)

        lbl_p_nom= tk.Label(Button_Frame,text="Nom Produit",font=("goudy old style",15),bg="white").place(x=5,y=5)
        txt_p_nom= tk.Entry(Button_Frame,font=("goudy old style",15),textvariable=self.var_pname,bg="lightyellow",state="readonly").place(x=10,y=35,width=120,height=20)

        lbl_p_prix = tk.Label(Button_Frame, text="Prix Produit", font=("goudy old style", 15), bg="white").place(x=150, y=5)
        txt_p_prix = tk.Entry(Button_Frame, font=("goudy old style", 15), textvariable=self.var_prix, bg="lightyellow",state="readonly").place(x=150, y=35, width=120, height=20)

        lbl_p_qte = tk.Label(Button_Frame, text="Quantite", font=("goudy old style", 15), bg="white").place(x=298,y=5)
        txt_p_qte = tk.Entry(Button_Frame, font=("goudy old style", 15), textvariable=self.var_qte, bg="lightyellow").place(x=295, y=35, width=120, height=20)

        self.lbl_p_stock = tk.Label(Button_Frame, text="En Stock", font=("goudy old style", 15), bg="white")
        self.lbl_p_stock.place(x=5, y=60)

        btn_clear_cart = tk.Button(Button_Frame,text="Reinitialiser",command=self.clear_card,cursor="hand2",font=("times new roman",14),bg="lightgray").place(x=140,y=79)
        btn_ajout_cart = tk.Button(Button_Frame,command=self.ajout_modifier, text="Ajouter | Modifier", cursor="hand2", font=("times new roman", 14),bg="orange").place(x=270, y=79)


        ####facturation
        FactureFrame = tk.Frame(self.root,bd=4,relief=RIDGE,bg="white")
        FactureFrame.place(x=1094,y=130,width=260,height=438)

        ctitle = tk.Label(FactureFrame,text="Zone de facture \n client",font=("goudy old style",15),bg="lightblue",bd=3,relief=RIDGE).pack(side=TOP,fill=X)

        scroll_y = tk.Scrollbar(FactureFrame, orient=VERTICAL)
        scroll_y.pack(side=RIGHT, fill=Y)

        self.txt_espace_facture = tk.Text(FactureFrame,yscrollcommand=scroll_y.set)
        self.txt_espace_facture.pack(fill=BOTH, expand=1)
        scroll_y.config(command=self.txt_espace_facture.yview)


        ### Button
        FactureMenuFrame = tk.Frame(self.root,bd=4,relief=RIDGE,bg="white")
        FactureMenuFrame.place(x=1094,y=570,width=259,height=121)


        self.lbl_montant_facture = tk.Label(FactureMenuFrame,text="M.Facture \n [0]",font=("goudy old style",10),bg="#3f51b5",fg="white")
        self.lbl_montant_facture.place(x=5,y=5,width=75,height=40)

        self.lbl_remise_facture = tk.Label(FactureMenuFrame, text="Remise \n [0]", font=("goudy old style", 10),  bg="#8bc34a", fg="white")
        self.lbl_remise_facture.place(x=91, y=5, width=75, height=40)

        self.lbl_net_payer = tk.Label(FactureMenuFrame, text="N.à payer \n [0]", font=("goudy old style", 10),  bg="#607d8d", fg="white")
        self.lbl_net_payer.place(x=175, y=5, width=75, height=40)


        self.btn_imprimer= tk.Button(FactureMenuFrame,text="Imprimer",command=self.imprimer_facture, font=("goudy old style",15),bg="lightgreen").place(x=85,y=60,width=77,height=40)
        self.btn_reini= tk.Button(FactureMenuFrame, text="Réinitialiser",command=self.clear_all, font=("goudy old style", 15),bg="lightgray").place(x=165, y=60, width=86, height=40)
        self. btn_generer= tk.Button(FactureMenuFrame, text="Générer",command=self.generer_facture , font=("goudy old style", 15),bg="yellow").place(x=5, y=60, width=77, height=40)



        ######fonction
    def get_input(self, num):
        xnum = self.var_cal_input.get()+str(num)
        self.var_cal_input.set(xnum)

    def clear_call(self):
        self.var_cal_input.set("")

    def resultat(self):
        resultat = self.txt_cal_input.get()
        self.var_cal_input.set(eval(resultat))

        ##fonction pour afficher

    def afficher(self):
        try:
            # Assuming self.cur is connected to your database
            self.cur.execute("select pid, nom,prix, quantite, status from produit where status ='Active'")
            rows = self.cur.fetchall()
            self.produit_table.delete(*self.produit_table.get_children())
            for row in rows:
                self.produit_table.insert("", END, values=row)

        except Exception as ex:
            messagebox.showerror("Erreur", f"Erreur de connexion {str(ex)}")



        ###fonction permettant de faire des recherches
    def rechercher(self):

        try:
            if self.var_recherche.get() == "":
                messagebox.showerror("Erreur", "Saisir le produit à rechercher?")
            else:
               self.cur.execute("select pid, nom,prix, quantite, status from produit where nom LIKE '%"+self.var_recherche.get()+"%'and  status ='Active' ")
               rows= self.cur.fetchall()
            if len(rows) != 0:
                    # Effacer le contenu précédent de la liste
                    self.produit_table.delete(*self.produit_table.get_children())
                    # Ajouter les nouveaux résultats à la liste
                    for row in rows:
                         self.produit_table.insert("", END, values=row)
            else:
                    messagebox.showerror("Erreur", "Aucun résultat trouvé")
        except Exception as ex:
            messagebox.showerror("Erreur", f"Erreur de connexion {str(ex)}")

    def get_donne(self, ev):
        r = self.produit_table.focus()
        contenu = self.produit_table.item(r)
        row = contenu["values"]
        self.var_pid.set(row[0])
        self.var_pname.set(row[1])
        self.var_prix.set(row[2])
        self.var_qte.set(row[3])
        self. lbl_p_stock .config(text=f"En Stock [{str(row[3])}]")
        self.var_stock.set(row[3])


    def get_donne_cart(self, ev):
        r = self.cartTable.focus()
        contenu = self.cartTable.item(r)
        row = contenu["values"]
        self.var_pid.set(row[0])
        self.var_pname.set(row[1])
        self.var_prix.set(row[2])
        self.lbl_p_stock.config(text=f"En Stock [{str(row[3])}]")
        self.var_stock.set(row[3])
        self.var_qte.set(row[3])

    def ajout_modifier(self):
        # Vérification si un produit est sélectionné
        if self.var_pid.get() == "":
            messagebox.showerror("Erreur", "Sélectionnez un produit")
        # Vérification si la quantité est saisie
        elif self.var_qte.get() == "":
            messagebox.showerror("Erreur", "Entrez la quantité")
        # Vérification si la quantité est un nombre entier
        elif not self.var_qte.get().isdigit():
            messagebox.showerror("Erreur", "La quantité doit être un nombre entier")
        # Vérification si la quantité demandée est disponible en stock
        elif int(self.var_qte.get()) > int(self.var_stock.get()):
            messagebox.showerror("Erreur", "La quantité n'est pas disponible")
        else:
            # Récupération des données du produit sélectionné
            prix_cal = self.var_prix.get()
            cart_donne = [self.var_pid.get(), self.var_pname.get(), self.var_prix.get(), self.var_qte.get(),
                          self.var_stock.get()]

            # Vérification si le produit est déjà présent dans le panier
            present = False  # Flag pour indiquer si le produit est déjà présent
            index_ = 0  # Indice du produit dans le panier
            for row in self.cart_list:
                if self.var_pid.get() == row[0]:  # Vérification de l'ID du produit
                    present = True  # Le produit est déjà présent dans le panier
                    break  # Sortie de la boucle dès qu'un produit correspondant est trouvé

                index_ += 1  # Incrément de l'indice pour suivre le produit actuel

            # Si le produit est déjà présent dans le panier
            if present:
                # Demande à l'utilisateur s'il souhaite modifier ou supprimer le produit existant
                op = messagebox.askyesno("Confirmer",
                                         "Le produit est déjà présent.\nVoulez-vous modifier ou supprimer de la liste?")
                if op:  # Si l'utilisateur choisit de modifier le produit
                    if self.var_qte.get() == "0":
                        # Si la quantité est réduite à zéro, supprime le produit du panier
                        self.cart_list.pop(index_)
                    else:
                        # Sinon, met à jour la quantité du produit dans le panier
                        self.cart_list[index_][3] = self.var_qte.get()
            else:
                # Si le produit n'est pas déjà présent dans le panier, l'ajoute
                self.cart_list.append(cart_donne)

            # Actualise l'affichage du panier
            self.afficher_cart()
            # Actualise l'affichage de la facture
            self.facture_modifier()

    def afficher_cart(self):
        try:
            self.cartTable.delete(*self.cartTable.get_children())
            for row in self.cart_list:
                self.cartTable.insert("", END, values=row)
        except Exception as ex:
            messagebox.showerror("Erreur", f"Erreur de connexion {str(ex)}")

    def facture_modifier(self):
        self.montant_facture = 0
        self.net_payer = 0
        self.remise = 0
        for row in self.cart_list:
            self.montant_facture += float(row[2]) * int(row[3])

        self.remise = (self.montant_facture * 5) / 100
        self.net_payer = self.montant_facture - self.remise

        # Mettre à jour l'affichage des étiquettes
        self.lbl_montant_facture.config(text=f"M.Facture \n [{str(self.montant_facture)}]")
        self.lbl_net_payer.config(text=f"N.à payer \n [{str(self.net_payer)}]")
        self.lbl_remise_facture.config(text=f"Remise \n [{str(self.remise)}]")
        self.ctitle.config(text=f"Produit \n Total du Panier : {str(len(self.cart_list))}")



    def generer_facture(self):
        if self.var_cname.get()=="":
            messagebox.showerror("Erreur","Saisir le nom du client")
        elif len(self.cart_list)==0:
            messagebox.showerror("Erreur","Ajouter des produits dans le panier")
        else:

             self.entete_facture()
             self.corp_facture()
             self.footer_facture()
             fp = open(fr"C:\Users\ACER\Desktop\python\gestion_magazin\factures\{str(self.facture)}.txt","w")
             fp.write(self.txt_espace_facture.get("1.0",END))
             fp.close
             messagebox.showinfo("Sauvegarder","Enregistrement/Générer effectué avec succèss")
             self.ck_print = 1


    def entete_facture(self):
        self.facture = int(time.strftime("%H%M%S"))+int(time.strftime("%d%m%Y"))
        facture_entete = f'''
   Magasin Rhinostore  
\tTel:+22897759232 \n Adresse Adidogomé Sagbado
{str("=" * 57)}
Nom du client : {self.var_cname.get()}
Tel du client : {self.var_contact.get()}
Numéro Facture : {str(self.facture)} 
Date: {time.strftime("%d/%m/%Y")}
{str("=" * 57)}
Nom Prod \tQuant \tPrix
{str("=" * 57)}
    '''


        self.txt_espace_facture.delete("1.0",END)
        self.txt_espace_facture.insert("1.0",facture_entete)

    def corp_facture(self):
        try:
            self.con = mysql.connector.connect(
                host="localhost",
                port=3307,
                user="root",
                password="",
                database="gestion_magazin"
            )
            self.cur = self.con.cursor()

            for row in self.cart_list:
                pid = row[0]
                nom = row[1]
                quantite = int(row[4]) - int(row[3])
                if int(row[3]) == int(row[4]):
                    status = "Inactive"
                else:
                    status = "Active"

                prix = float(row[2]) * float(row[3])
                prix = str(prix)
                self.txt_espace_facture.insert(END, "\n\t" + nom + "\t\t\t" + row[3] + "\t\t" + prix)
                self.cur.execute("UPDATE produit SET quantite=%s, status=%s WHERE pid=%s", (
                    quantite,
                    status,
                    pid,
                ))
                self.con.commit()
            messagebox.showinfo("Succès", "Facture générée avec succès!")
        except mysql.connector.Error as err:
            messagebox.showerror("Erreur", f"Erreur MySQL: {err}")
        finally:
            if self.con.is_connected():
                self.cur.close()
                self.con.close()

    def footer_facture(self):
        facture_footer = f'''
    {str("=" * 57)}
    Montant Facture : \t\t\t\t{self.montant_facture}
    Remise : \t\t\t\t{self.remise}  
    Net à Payer : \t\t\t\t{self.net_payer} 
    {str("=" * 57)}
            '''
        self.txt_espace_facture.insert(END, facture_footer)



    def clear_card(self):
        self.var_pid.set("")
        self.var_pname.set("")
        self.var_prix.set("")
        self.var_qte.set("")
        self.lbl_p_stock.config(text=f"En Stock")
        self.var_stock.set("")


    def modifier_heure(self):
            heure_ = (time.strftime("%H:%M:%S"))
            date_  = (time.strftime("%d-%m-%Y"))
            self.time_label.config(text=f"Bienvenu chez rinoStore!\t\t Date : {str(date_)}\t\t Heure : {str(heure_)}")
            self.time_label.after(200,self.modifier_heure)

    def imprimer_facture(self):
        if self.ck_print == 1:
            try:
                # Créer un répertoire "factures" s'il n'existe pas déjà
                os.makedirs("factures", exist_ok=True)

                # Créer le chemin du fichier de la facture
                fichier = os.path.join("factures", f"{self.facture}.txt")

                # Écrire la facture dans le fichier
                with open(fichier, "w") as f:
                    f.write(self.txt_espace_facture.get("1.0", END))

                # Imprimer le fichier
                os.system("notepad /p " + fichier)
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de l'impression de la facture : {str(e)}")
        else:
            messagebox.showerror("Erreur", "Veuillez générer la facture")

    def deconnecter(self):
            self.root.destroy()
            self.obj = os.system("python C:/Users/ACER/Desktop/python/gestion_magazin/login.py")

    def clear_all(self):
        try:
            self.con = mysql.connector.connect(
                host="localhost",
                port=3307,
                user="root",
                password="",
                database="gestion_magazin"
            )
            self.cur = self.con.cursor()

            self.cart_list = []  # Supprime la liste elle-même
            self.var_cname.set("")
            self.var_contact.set("")
            self.txt_espace_facture.delete("1.0", END)
            self.ctitle.config(text="Produit \n Total du Panier :[0]")
            self.var_recherche.set("")
            self.ck_print = 0
            self.clear_card()  # Appel de la méthode pour réinitialiser les données du panier
            self.afficher()  # Actualise l'affichage des produits
            self.afficher_cart()  # Actualise l'affichage du panier
        except Exception as ex:
            messagebox.showerror("Erreur", f"Erreur lors de la réinitialisation : {str(ex)}")


if __name__ == "__main__":
    root = tk.Tk()
    obj = Caisse(root)
    root.mainloop()