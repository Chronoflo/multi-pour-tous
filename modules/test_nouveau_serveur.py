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
        self.pack(fill='both', expand=1)

        # Creation du cadre de selection
        self.fenetre_selection = MyLabelFrame(self, text=" Programmes enregistrés", labelanchor="nw", width=50, **kwargs)
        self.fenetre_selection.pack(fill='both', expand=1)

        # Creation de la liste des programmes #
        self.liste_prgm = tk.Listbox(self.fenetre_selection, height=10)
        programmes = ['programme 1', 'programme 2', 'programme 3', 'programme 4', 'programme 5', 'programme 6', 'programme 7']
        for element in programmes:
            self.liste_prgm.insert(tk.END, element)

        # Creation de la scrollbar de la liste des programmes #
        scrollbar = tk.Scrollbar(self.fenetre_selection)
        scrollbar.pack(side='right', fill='y')
        self.liste_prgm.config(yscrollcommand=scrollbar.set)
        self.liste_prgm.pack(fill='both', padx=5, pady=10)
        scrollbar.config(command=self.liste_prgm.yview)

        # Creation du cadre d'ajout #
        self.fenetre_ajout = MyLabelFrame(self, text=" Ajout ", labelanchor="nw", **kwargs)
        self.fenetre_ajout.pack(fill='both', expand=1)

        # Creation de la zone d'ecriture du chemin du programme a ajouter #
        self.nouveau_programme = tk.StringVar()
        self.nouveau_programme = tk.Entry(self.fenetre_ajout, textvariable=self.nouveau_programme, width=30)
        self.nouveau_programme.grid(column=0, row=0, padx=5, pady=5)

        # Creation du bouton de suppression #
        self.bouton_ajout = MyButton(self.fenetre_ajout, text="Ajouter", command= lambda: self.suppression(self.nouveau_programme.get()))
        self.bouton_ajout.grid(column=1, row=0, padx=5, pady=5)

        # Creation du bouton d'ajout #
        self.bouton_ajout = MyButton(self.fenetre_ajout, text="Ajouter", command= lambda: self.verification_ajout(self.nouveau_programme.get()))
        self.bouton_ajout.grid(column=1, row=0, padx=5, pady=5)

        # Creation du bouton de validation #
        self.bouton_valider = MyButton(self.fenetre_ajout, text="Ok", command= lambda: self.demarrage())
        self.bouton_valider.grid(column=0, row=1, columnspan=99, padx=5, pady=5)

    def verification_ajout(self, path):
        self.path = path
        chemin_valide = False
        if self.path != "":
            try:
                with open(self.path):
                    chemin_valide = True
            except IOError:
                chemin_valide = False
        if chemin_valide is True:
            self.liste_prgm.insert(tk.END, self.path)


# Affichage de la fenetre de selection des programmes #
def ecran_selection():
    fenetre_selection = MyTkApp()
    fenetre_selection.title("Selection")
    fenetre_selection.resizable(width=False, height=False)

    interface_selection = Fenetre_Config(fenetre_selection)
    interface_selection.mainloop()


### CODE PUR ###
ecran_selection()

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp.settimeout(None)
tcp.bind(('',15555))

while True:
    tcp.listen(1)
    (client, (ip, port)) = tcp.accept()
    recvThread = Recv(ip, port, client)
    recvThread.start()

tcp.close()