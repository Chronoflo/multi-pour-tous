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
        self.fenetre_selection = MyLabelFrame(self, text=" Programmes enregistrés", labelanchor="nw", **kwargs)
        self.fenetre_selection.pack(fill='both', expand=1)

        # Creation de la liste des programmes #
        self.liste_prgm = tk.Listbox(self.fenetre_selection, height=15)
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



tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp.settimeout(None)
tcp.bind(('',15555))

while True:
    tcp.listen(1)
    (client, (ip, port)) = tcp.accept()
    recvThread = Recv(ip, port, client)
    recvThread.start()

client.close()
tcp.close()