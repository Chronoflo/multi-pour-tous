from modules.myTk import *
import socket
import threading


# Variables #
recv = ""


# Threads de connexion # TODO: thread de reception des données + thread d'envoi de données
class Recv_TCP:
    def __init__(self, HOST, PORT, csocket):
        threading.Thread.__init__(self)
        self.ip = HOST
        self.port = PORT
        self.csocket = csocket
    def run(self):
        global recv
        recv = self.csocket.recv(2048)


# Interface de connexion #
class Fenetre_Connexion(MyFrame):
    def __init__(self, fenetre, **kwargs):
        MyFrame.__init__(self, fenetre, **kwargs)
        self.pack(fill='both', expand=1)

        # Creation du cadre du logo #
        self.logo = tk.PhotoImage(file="logo.png")
        self.logo = self.logo.subsample(2)
        self.cadre_logo = tk.Canvas(self)
        self.cadre_logo.create_image(225, 0, image=self.logo, anchor="n")
        self.cadre_logo.pack(fill="both", expand=1, side="top")

        # Creation du cadre de connexion #
        self.fenetre_connexion = MyLabelFrame(self, text=" Connexion ", labelanchor="nw", **kwargs)
        self.fenetre_connexion.place(x=0, y=282, width=450, height=150)

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

    def connexion(self, HOST, PORT): # TODO: Connection TCP
        print(HOST + "\n")
        print(PORT)

        self.warning_adresse_serveur.pack_forget()
        self.warning_port_serveur.pack_forget()

        if HOST != "" and PORT != "":
            adresse_valide = True
            port_valide = True

            HOST = str(HOST)
            HOSTbis = HOST.split(".")

            if len(HOSTbis) == 4: # Une adresse valide possede 4 chaines separes de points
                for element in HOSTbis: # Chaque chaine doit etre un nombre
                    try:
                        int(element)
                    except ValueError:
                        adresse_valide = False

            else:
                adresse_valide = False

            if adresse_valide == False:
                self.warning_adresse_serveur.pack()

            try:
                PORT = int(PORT)
            except ValueError:
                self.warning_port_serveur.pack()
                port_valide = False

            print(adresse_valide, port_valide)
            print(HOST, PORT)

        else:
            pass

#        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#        try:
#            tcp.connect((HOST, PORT))
#        except TimeoutError:
#            pass

# TODO: Ecran de choix de programme + Champ d'envoie de commande
# TODO: Ecran de retour Streaming en UDP






def ecran_connexion():
    fenetre = MyTkApp()
    fenetre.title("Client")
    fenetre.resizable(width=False, height=False)
    fenetre.geometry('{}x{}'.format(450, 432))

    interface = Fenetre_Connexion(fenetre)
    interface.mainloop()


ecran_connexion()