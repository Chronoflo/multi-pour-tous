from modules.myTk import *
import socket
import threading

class Recv(threading.Thread):
    def __init__(self, ip, port, client):
        threading.Thread.__init__(self)
        self.IP = str(ip)
        self.PORT = str(port)
        self.CLIENT = client
        print("[+] Nouveau Thread de reception pour " + self.IP, self.PORT)
    def run(self):
        print("[-] Connexion de " + self.IP, self.PORT)
        while True:
            self.msg = self.CLIENT.recv(2048)
            self.msg = self.msg.decode()
            if self.msg != "":
                print(self.msg)

# Fenetre de configuration des programmes #
class Fenetre_Config(MyFrame):
    def __init__(self, fenetre, **kwargs):
        MyFrame.__init__(self, fenetre, **kwargs)
        self.fenetre_config = fenetre
        self.pack(fill='both', expand=1)

        # Creation du cadre de selection
        self.fenetre_selection = MyLabelFrame(self, text=" Programmes enregistrés", labelanchor="nw", width=50, **kwargs)
        self.fenetre_selection.pack(fill='both', expand=1)

        # Creation de la liste des programmes #
        self.liste_prgm = tk.Listbox(self.fenetre_selection, height=10)
        self.programmes = []
        try: # Importation du fichier de configuration s'il y en a un
            self.fichier_config = open("liste_programmes.txt", 'r')
            for line in self.fichier_config:
                self.programmes.append(line)
        except:
            pass
        for element in self.programmes:
            self.liste_prgm.insert(tk.END, element)

        # Creation de la scrollbar de la liste des programmes #
        scrollbar = tk.Scrollbar(self.fenetre_selection)
        scrollbar.pack(side='right', fill='y')
        self.liste_prgm.config(yscrollcommand=scrollbar.set)
        self.liste_prgm.pack(fill='both', padx=5, pady=5)
        scrollbar.config(command=self.liste_prgm.yview)

        # Creation du bouton de suppression #
        self.bouton_ajout = MyButton(self.fenetre_selection, text="Supprimer", command= lambda: self.suppression(self.liste_prgm.curselection()))
        self.bouton_ajout.pack(padx=5, pady=5)

        # Creation du cadre d'ajout #
        self.fenetre_ajout = MyLabelFrame(self, text=" Ajout ", labelanchor="nw", **kwargs)
        self.fenetre_ajout.pack(fill='both', expand=1)

        # Creation de la zone d'ecriture du chemin du programme a ajouter #

        self.nouveau_programme = tk.StringVar()
        self.nouveau_programme = tk.Entry(self.fenetre_ajout, textvariable=self.nouveau_programme, width=30)
        self.nouveau_programme.bind("<Return>", lambda e: self.ajout(self.nouveau_programme.get()))
        self.nouveau_programme.grid(column=0, row=0, padx=5, pady=5)

        # Creation du bouton d'ajout #
        self.bouton_ajout = MyButton(self.fenetre_ajout, text="Ajouter", command= lambda: self.ajout(self.nouveau_programme.get()))
        self.bouton_ajout.grid(column=1, row=0, padx=5, pady=5)

        # Creation du bouton de validation #
        self.bouton_valider = MyButton(self.fenetre_ajout, text="Ok", command= lambda: self.validation())
        self.bouton_valider.grid(column=0, row=1, columnspan=99, padx=5, pady=5)

    def ajout(self, path):
        self.path = path
        chemin_valide = False
        if self.path != "":
            try:
                with open(self.path): # Chemin existant
                    chemin_valide = True
            except IOError:
                chemin_valide = False
                print("chemin inexistant")

        if chemin_valide is True:
            self.programmes = self.liste_prgm.get(0, tk.END)
            self.programmes = list(self.programmes)
            if str(self.path) in self.programmes: # Deja dans la liste ?
                print('Deja dans la liste')
            else:
                self.liste_prgm.insert(tk.END, self.path)
                self.programmes.append(self.path)
                self.nouveau_programme.delete(first=0, last=99999)
                try:
                    open("liste_programmes.txt")
                    self.fichier_config = open("liste_programmes.txt", 'a')
                    if len(self.programmes) == 1:
                        self.fichier_config.write(self.path)
                    else:
                        self.fichier_config.write("\n" + self.path)
                    self.fichier_config.close()
                except:
                    self.fichier_config = open("liste_programmes.txt", 'x')
                    self.fichier_config.write(self.path)
                    self.fichier_config.close()

    def suppression(self, element):
        element = str(element)
        element = element.replace("(", "")
        element = element.replace(")", "")
        element = element.replace(",", "")
        if element != "":
            element = int(element)
            self.liste_prgm.delete(element)
            del self.programmes[element]
            self.fichier_config = open("liste_programmes.txt", 'w')
            if self.programmes != []:
                for stuff in self.programmes:
                    self.fichier_config.write(stuff + "\n")
            else:
                self.fichier_config.write("")
            self.fichier_config.close()

    def validation(self):
        if len(self.programmes) >= 1:
            self.fenetre_config.destroy()
            ecran_reduit()
        else:
            print("Veuillez definir des programmes")

### Interface reduite ###
class Fenetre_reduite(MyFrame):
    def __init__(self, fenetre, **kwargs):
        MyFrame.__init__(self, fenetre, **kwargs)
        self.pack(fill='both', expand=1)

        # Creation du cadre principal #
        self.fenetre_connexion = MyLabelFrame(self, text=" En cours ", labelanchor="nw", **kwargs)
        self.fenetre_connexion.place(width=200, height=70)

        # Creation de la zone de texte "En attente du serveur" #
        self.texte_attente_serveur = tk.Label(self.fenetre_connexion, text="Serveur en cours\nd'execution")
        self.texte_attente_serveur.pack()



# Affichage de la fenetre de selection des programmes #
def ecran_selection():
    fenetre_selection = MyTkApp()
    fenetre_selection.title("Selection")
    fenetre_selection.resizable(width=False, height=False)

    interface_selection = Fenetre_Config(fenetre_selection)
    interface_selection.mainloop()

def ecran_reduit():
    fenetre_reduite = MyTkApp()
    fenetre_reduite.title("Multi pour tous")
    fenetre_reduite.resizable(width=False, height=False)
    fenetre_reduite.geometry('{}x{}'.format(200, 70))

    interface_reduite = Fenetre_reduite(fenetre_reduite)
    interface_reduite.mainloop()

def demarrage():
    ecran_selection()

    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp.settimeout(None)
    tcp.bind(('', 15555))

    while True:
        tcp.listen(1)
        (client, (ip, port)) = tcp.accept()
        recvThread = Recv(ip, port, client)
        recvThread.start()


### CODE PUR ###
ecran_selection()
tcp.close()