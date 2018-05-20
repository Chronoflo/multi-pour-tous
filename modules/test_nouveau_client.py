from modules.myTk import *
import socket
import threading
import time

# Variables #
send = ""
recv = ""

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip = ""
port = ""

ssocket = ""

stop_recv_tcp = False
stop_send_tcp = False

### FONCTIONS ###
def syntaxe_console():
    a = str(time.localtime())
    a = a.replace("time.struct_time(","")
    a = a.replace(")","")
    a = a.replace(",","")
    a = a.replace("tm_year=","")
    a = a.replace("tm_mon=","")
    a = a.replace("tm_mday=","")
    a = a.replace("tm_hour=","")
    a = a.replace("tm_min=","")
    a = a.replace("tm_sec=","")
    a = a.replace("tm_wday=","")
    a = a.replace("tm_yday=","")
    a = a.replace("tm_isdst=","")

    a = a.split()

    hour = a[3]
    if len(hour) == 1:
        hour = "0" + hour
    min = a[4]
    if len(min) == 1:
        min = "0" + min
    sec = a[5]
    if len(sec) == 1:
        sec = "0" + sec

    return(hour + ":" + min + ":" + sec + " | ")


def afficher_recv(recv):
    return(syntaxe_console() + ">> " + recv)

def afficher_send(send):
    return(syntaxe_console() + "> " + send)

def afficher_info(info):
    return(syntaxe_console() + "[ " + info + " ]")

# Affichage des fenetres #
def ecran_connexion():
    fenetre_connexion = MyTkApp()
    fenetre_connexion.title("Client")
    fenetre_connexion.resizable(width=False, height=False)
    fenetre_connexion.geometry('{}x{}'.format(450, 432))

    interface_connexion = Fenetre_Connexion(fenetre_connexion)
    interface_connexion.mainloop()

def ecran_serveur_off():
    fenetre_attente_serveur = MyTkApp()
    fenetre_attente_serveur.title("Serveur injoignable")
    fenetre_attente_serveur.resizable(width=False, height=False)
    fenetre_attente_serveur.geometry('{}x{}'.format(200, 70))

    interface_attente_serveur = Fenetre_attente_serveur(fenetre_attente_serveur)
    interface_attente_serveur.mainloop()

def ecran_controle():
    fenetre_controle = MyTkApp()
    fenetre_controle.title("Multi Pour Tous")
    fenetre_controle.resizable(width=False, height=False)

    interface_controle = Fenetre_Controle(fenetre_controle)
    interface_controle.mainloop()


### Threads ###




### Interface de connexion ###
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
        self.HOST.insert(0, '127.0.0.1')
        self.HOST.pack()

        # Creation du Warning "Adresse du serveur" #
        self.warning_adresse_serveur = tk.Label(self.fenetre_connexion, fg="red", text="Veuillez entrer une adresse valide, de la forme : XXX.XXX.XXX.XXX")

        # Creation de la zone de texte "Port du serveur" #
        self.texte_port_serveur = tk.Label(self.fenetre_connexion, text="Port du serveur : ")
        self.texte_port_serveur.pack()

        # Creation de la zone d'ecriture du port du serveur #
        self.PORT = tk.StringVar()
        self.PORT = tk.Entry(self.fenetre_connexion, textvariable=self.PORT, width=6)
        self.PORT.insert(0, '15555')
        self.PORT.pack()

        # Creation du Warning "Port du serveur" #
        self.warning_port_serveur = tk.Label(self.fenetre_connexion, fg="red", text="Veuillez entrer un port valide")

        # Creation du bouton de connexion #
        self.bouton_connexion = MyButton(self.fenetre_connexion, text="Connexion", command= lambda: self.validation_connexion(self.HOST.get(), self.PORT.get()))
        self.bouton_connexion.pack()

    def validation_connexion(self, HOST, PORT): #
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

            if adresse_valide is True and port_valide is True:
                global ip
                ip = HOST

                global port
                port = PORT

        # Tentative de connexion #
        try:
            global tcp
            tcp.connect((ip, port))
            data = "hello"
            data = data.encode()
            tcp.send(data)
            ecran_controle()
        except OSError:
            ecran_serveur_off()


### Interface d'attente du serveur ###
class Fenetre_attente_serveur(MyFrame):
    def __init__(self, fenetre, **kwargs):
        MyFrame.__init__(self, fenetre, **kwargs)
        self.pack(fill='both', expand=1)

        # Creation du cadre de connexion #
        self.fenetre_connexion = MyLabelFrame(self, text=" Connexion ", labelanchor="nw", **kwargs)
        self.fenetre_connexion.place(width=200, height=75)

        # Creation de la zone de texte "En attente du serveur" #
        self.texte_attente_serveur = tk.Label(self.fenetre_connexion, text="Le serveur n'est pas\njoignable, veuillez\nreessayer", fg="red")
        self.texte_attente_serveur.pack()

### Interface de controle ###
class Fenetre_Controle(MyFrame):
    def __init__(self, fenetre, **kwargs):
        MyFrame.__init__(self, fenetre, **kwargs)
        self.pack(fill='both', expand=1)

        # Creation du cadre de selection
        self.fenetre_selection = MyLabelFrame(self, text=" Programmes ", labelanchor="nw", **kwargs)
        self.fenetre_selection.pack(fill='both', expand=1)

        # Creation de la liste des programmes # TODO: gerer la reception des programmes disponibles et les mettre dans la liste "programmes"
        self.liste_prgm = tk.Listbox(self.fenetre_selection, height=5)
        programmes = ['programme 1', 'programme 2', 'programme 3', 'programme 4', 'programme 5', 'programme 6', 'programme 7']
        for element in programmes:
            self.liste_prgm.insert(tk.END, element)

        # Creation de la scrollbar de la liste des programmes #
        scrollbar = tk.Scrollbar(self.fenetre_selection)
        scrollbar.pack(side='right', fill='y')
        self.liste_prgm.config(yscrollcommand=scrollbar.set)
        self.liste_prgm.pack(fill='both', padx=5, pady=10)
        scrollbar.config(command=self.liste_prgm.yview)

        # Creation du cadre de commande #
        self.fenetre_controle = MyLabelFrame(self, text=" Console ", labelanchor="nw", **kwargs)
        self.fenetre_controle.pack(fill='both', expand=1)

        # Creation de la zone d'ecriture des commandes #
        self.commande = tk.StringVar()
        self.commande = tk.Entry(self.fenetre_controle, textvariable=self.commande, width=30)
        self.commande.grid(column=0, row=0, padx=5, pady=5)

        # Creation du bouton d'envoi #
        self.bouton_envoi = MyButton(self.fenetre_controle, text="Envoyer", command= lambda: self.envoi_tcp(self.commande.get()))
        self.bouton_envoi.grid(column=1, row=0, padx=5, pady=5)

        # Creation de la zone d'affichage des reponses serveur (console) #
        self.console = tk.Listbox(self.fenetre_controle, height=3, width=40, bg='#2d2d2d', fg='#e8e8e8')
        self.console.insert(tk.END, afficher_info("Bienvenue dans la console"))

        # Creation de la scrollbar verticale de la console #
        scrollbar_console = tk.Scrollbar(self.fenetre_controle, orient='vertical')
        scrollbar_console.grid(column=3, row=1, sticky='e')
        scrollbar_console.config(command=self.console.yview)
        self.console.grid(row=1, columnspan=2, padx=5, pady=10, sticky='w')
        self.console.config(yscrollcommand=scrollbar_console.set)

    def envoi_tcp(self, data):
        if data != "":
            self.console.insert(tk.END, afficher_send(data))
            data = data.encode()
            tcp.send(data)
            self.commande.delete(first=0, last=999)



# TODO: Ecran de retour Streaming en UDP
# TODO: Continuer Threads


### PARTIE CODE PUR ###

ecran_connexion()

afficher_recv("ok")
time.sleep(1)
afficher_send("test")

try:
    tcp.close()
except NameError:
    pass