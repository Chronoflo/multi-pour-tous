from modules.myTk import *
import socket

# Interface de creation d'utilisateur #
class Fenetre_Connexion(MyFrame):
    def __init__(self, **kwargs):
        MyFrame.__init__(self, fenetre, **kwargs)
        self.pack(fill='both', expand="yes")

        # Creation du cadre principal #
        self.fenetre_connexion = MyLabelFrame(self, text=" Connexion ", labelanchor="nw", padx=20, pady=20, **kwargs)
        self.fenetre_connexion.pack(fill='both', expand="yes")

        # Creation de la zone de texte "Adresse du serveur" #
        self.texte_adresse_serveur = tk.Label(self.fenetre_connexion, text="Adresse IP du serveur : ")
        self.texte_adresse_serveur.pack()

        # Creation de la zone d'ecriture de l'adresse du serveur #
        self.HOST = tk.StringVar()
        self.HOST = tk.Entry(self.fenetre_connexion, textvariable=self.HOST, width=15)
        self.HOST.pack()

        # Creation du Warning "Adresse du serveur" #
        self.warning_adresse_serveur = tk.Label(self.fenetre_connexion, fg="red", text="Veuillez entrer une adresse valide, de la forme : XXX.XXX.XXX.XXX")

        # Creation de la zone de texte "Port du serveur" #
        self.texte_port_serveur = tk.Label(self.fenetre_connexion, text="Port du serveur : ")
        self.texte_port_serveur.pack()

        # Creation de la zone d'ecriture du port du serveur #
        self.PORT = tk.StringVar()
        self.PORT = tk.Entry(self.fenetre_connexion, textvariable=self.PORT, width=6)
        self.PORT.pack()

        # Creation du Warning "Port du serveur" #
        self.warning_port_serveur = tk.Label(self.fenetre_connexion, fg="red", text="Veuillez entrer un port valide")

        # Creation du bouton de connexion #
        self.bouton_connexion = MyButton(self.fenetre_connexion, text="Connexion", command= lambda: self.connexion(self.HOST.get(), self.PORT.get()))
        self.bouton_connexion.pack()

    def connexion(self, HOST, PORT):
        print(HOST + "\n")
        print(PORT)

        self.warning_adresse_serveur.pack_forget()
        self.warning_port_serveur.pack_forget()

        if HOST != "" and PORT != "":
            try:
                HOST = str(HOST)
            except ValueError:
                self.warning_adresse_serveur.pack()
            try:
                PORT = int(PORT)
            except ValueError:
                self.warning_port_serveur.pack()
        else:
            pass

#        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#        try:
#            tcp.connect((HOST, PORT))
#        except TimeoutError:
#            pass



fenetre = MyTkApp()
fenetre.title("Client v0.1a")

interface = Fenetre_Connexion()
interface.mainloop()
