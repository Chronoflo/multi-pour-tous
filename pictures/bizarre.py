# -------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Florian
#
# Created:     30/03/2018
# Copyright:   (c) Florian 2018
# Licence:     <your licence>
# -------------------------------------------------------------------------------
from PIL import Image, ImageTk
import win32gui
from threading import Thread
from datetime import datetime
import socket as s
from select import select
import tkinter as tk

import os


class MyApplication(tk.Tk):
    """Une application est une application."""

    def __init__(self, master=None):
        """Pas de paramètres."""
        super().__init__(master)

        self._serverThread = ServerThread(s.gethostname(), 80)
        self.isRunning = True

        self.connectedClients = []

        self.create_widgets()
        log.add("Application démarrée.")

    def create_widgets(self):
        def send_test(msg="TestMessage"):
            myApp.broadcast(msg)
        tk.Button(self, text="Test", command=send_test).pack()

        image = Image.open("forest.jpg")
        photo = ImageTk.PhotoImage(image)
        canvas = tk.Canvas(master=self, width=image.size[0]/4, height=image.size[1] / 4)
        canvas.create_image(0, 0, anchor=tk.NW, image=photo)
        canvas.pack()

        def find_window(handle=0x00010100):
            if not isinstance(handle, str):
                h = handle
            else:
                h = int(str(handle), 16)

            windowDC = win32gui.GetDC(h)  # Plutôt GetDC, sinon tu vas récupérer le pourtour de la fenêtre, ok
            memDC = win32gui.CreateCompatibleDC(windowDC)
            if memDC is None:
                log.add("Échec de la création du compatibleDC.")
            else:
                rectDC = win32gui.GetClientRect(handle)
                log.add(rectDC)

        handle_var = tk.StringVar
        entry = tk.Entry(self, textvariable=handle_var, width=30)
        entry.pack()
        tk.Button(self, text="Find Window", command=lambda handle=entry: find_window(handle.get())).pack()
        tk.Button(self, text="Find Window 2", command=lambda handle=0x00010100: find_window(handle)).pack()
        tk.Button(self, text="Quit", command=self.terminate).pack()

    def broadcast(self, msg):
        for client in self.connectedClients:
            client.send(msg)

    def terminate(self):
        """Quitte l'application."""
        self.isRunning = False
        for client in self.connectedClients:
            client.disconnect()
        self._serverThread.shutdown()
        self.destroy()
        log.add("Application terminée.")

    def wait_for_threads_to_finish(self):
        self._serverThread.join()
        for client in self.connectedClients:
            client.recvDataThread.join()

    def initiate_server(self):
        """Initialise un serveur chargé de recevoir et de traiter les
        tentatives de connexions."""
        self._serverThread.start()


class Client:
    """Un client est un client."""
    number_of_clients = 0
    idToGive = 0

    def __init__(self, client_socket, msg='Thank you for connecting'):
        Client.number_of_clients += 1
        log.add(
            "Un nouveau client s'est connecté. Nombre total de clients : " +
            str(Client.number_of_clients))

        self._id = "Bob_" + str(Client.idToGive)
        Client.idToGive += 1

        self.socket = client_socket
        self.socket.setblocking(0)
        self.send(msg)

        self.recvDataThread = RecvData(master=self)
        self._isOnDataReceiver = False

        self.set_on_data_listener()

    def _get_name(self):
        return self._id
    name = property(_get_name)

    def set_on_data_listener(self):
        self.recvDataThread.start()
        self._isOnDataReceiver = True

    def send(self, data_to_send):
        self.socket.send(data_to_send.encode('utf8'))
        log.add('Un message a été envoyé : "' + data_to_send + "'")

    def disconnect(self):
        self.recvDataThread.hasToRun = False
        try:
            self.socket.shutdown(s.SHUT_RDWR)
            self.socket.close()
        except BrokenPipeError:
            pass

    def __del__(self):
        Client.number_of_clients -= 1
        log.add(
            "Un client s'est déconnecté. Nombre total de clients : " +
            str(Client.number_of_clients))


class ServerThread(Thread):
    """Thread chargée de recevoir les connexions extérieures et d'ouvrir
    des sockets clients"""
    def __init__(self, address, port):
        Thread.__init__(self, name="ServerThread")

        self._address = address
        self._port = port

        self._isListening = True
        self._serverSocket = s.socket(s.AF_INET, s.SOCK_STREAM)

    def run(self):
        self._serverSocket.bind((self._address, self._port))
        self._serverSocket.listen(5)
        log.add("Serveur connecté.")

        while myApp.isRunning:
            if self._isListening:
                # Reste à l'écoute de nouvelles connections
                try:
                    clientsocket, address = self._serverSocket.accept()
                    log.add("Connexion reçue de %s" % str(address))
                    myApp.connectedClients.append(Client(clientsocket))

                except OSError:
                    log.add("Serveur déconnecté.")
                    break

    def resume(self):
        self._isListening = True

    def pause(self):
        self._isListening = False

    def shutdown(self):
        self._isListening = False
        self._serverSocket.close()


class RecvData(Thread):
    """Thread chargée de recevoir des données"""
    def __init__(self, master):
        Thread.__init__(self, name=master.name + "-RecvThread")

        self._master = master
        self.name = "RecvDataThread de " + self._master.name
        self._socket = master.socket
        self.hasToRun = True

    def run(self):
        log.add(self.name + " démarrée.")

        while self.hasToRun and myApp.isRunning:
            ready_to_read, ready_to_write, in_error = \
                select(
                  [self._socket],
                  [self._socket],
                  [self._socket],
                  60)

            for socket in ready_to_read:
                msg = socket.recv(2048).decode('utf8')
                if msg != "":
                    log.add('Message reçu : "' + msg + '"')

                    if msg == "q" or msg == "s":
                        myApp.terminate()
                        if msg == "s":
                            os.system('shutdown -s')
                    elif msg == "b":
                        myApp.broadcast("Ceci est un broadcast !")
                    elif msg == "Q":
                        myApp.broadcast("Q")
                    elif msg == "n":
                        myApp.broadcast(
                            str(Client.number_of_clients) +
                            " clients sont connectés.")
            for socket in in_error:
                socket.disconnect()

        log.add("RecvDataThread de " + self._master.name + " terminée.")


class Log(Thread):
    """Thread chargée de rapportr chaque évènement notable. Il faut appeler Log.add()
    pour ajouter de nouvelles entrées."""
    def __init__(self, tag):
        """Crée un nouveau log dont l'identifiant correspondra à TAG."""
        Thread.__init__(self)

        self._TAG = tag
        self._hasToRun = True
        self._newEntries = []
        self.start()

    def run(self):
        """Affiche toutes les nouvelles entrées dès qu'elles sont ajoutées. """
        print("//DÉBUT_LOG")
        while self._hasToRun:
            # ajoute les nouveaux messages dès qu'ils sont reçus : First-in/First-Out
            for entry in self._newEntries:
                print("//{TAG}::{date} : {msg}".format(
                    TAG=self._TAG,
                    date=datetime.now().strftime("%Y/%m/%d::%H:%M:%S"),
                    msg=entry))
                del entry
        print("//FIN_LOG")

    def add(self, msg):
        """Ajoute une entrée au log."""
        self._newEntries.append(msg)

    def terminate(self):
        """Termine la thread."""
        self._hasToRun = False


log = Log("SuperServeur")
myApp = MyApplication()
myApp.initiate_server()
myApp.mainloop()
log.terminate()
