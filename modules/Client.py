# -*- coding: <utf-8> -*-

# -------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      DELPRAF
#
# Created:     29/03/2018
# Copyright:   (c) DELPRAF 2018
# Licence:     <your licence>
# -------------------------------------------------------------------------------
# TODO : toute la partie réseau est à refaire

import sys
import traceback
from threading import Thread
import socket as sokt
from select import select
from time import time

from modules.const import *

try:
    from modules.myTk import *
    from modules.handyfunctions import *
    from PIL import Image, ImageTk
    from cyordereddict import OrderedDict
    from orderedset import OrderedSet

    if sys.platform == 'win32':
        import win32gui
        import win32api
        from win32con import *
except ImportError:
    from modules.easydependencies import install_requirements
    install_requirements()

    from modules.myTk import *
    from modules.handyfunctions import *
    from PIL import Image, ImageTk
    from cyordereddict import OrderedDict
    from orderedset import OrderedSet

    if sys.platform == 'win32':
        import win32gui
        import win32api
        from win32con import *


entry_hint = "Message"


class Application(MyTkApp):
    """MyApplication est le composant principal d'une application qui hérite de MyTkApp. Il contient plusieurs méthodes
    et attributs généraux."""

    def __init__(self, theme=Themes.dark):
        """Construit une application avec le parent master.
        Attributs:
        -isRunning : Définit si l'application est en train de fonctionner
        -mainFrame : Frame qui englobe tous les autres widgets"""
        super().__init__(theme=theme)
        self.isRunning: bool = True
        self.mainFrame: MyFrame = None
        self.theme: dict = Themes.dark
        self._socket: sokt.socket = sokt.socket(sokt.AF_INET, sokt.SOCK_STREAM)
        self._connectionThread: ConnectionThread = None
        self.recvDataThread = RecvDataThread(main_thread=self)
        self.sendDataThread = SendDataThread(main_thread=self)

        self._key_pressed = OrderedDict()
        import string
        for letter in string.ascii_lowercase:
            self._key_pressed[letter] = 0
        self.bind('<Key>', self.on_key_press)
        self.bind('<KeyRelease>', self.on_key_up)

        self._is_connected = False

        log.add("Application démarrée.")
    # TODO : mieux gérer les appuis touches pour éviter les envois d'informations inutiles

    def on_key_press(self, event):
        if (time() - self._key_pressed[event.keysym]) > 0.1:
            self._key_pressed[event.keysym] = time()
            if self._is_connected:
                self.send_key(event.keysym, KEYPRESS)
                self.on_key_update()

    def on_key_up(self, event):
        if (time() - self._key_pressed[event.keysym]) > 0.1:
            self._key_pressed.remove(event.keysym)
            if self._is_connected:
                self.send_key(event.keysym, KEYUP)
                self.on_key_update()

    def send_key(self, key, keyevent):
        try:
            self._socket.send((KEYMSG + keyevent + key + MSGSEP).encode('utf8'))
        except BrokenPipeError:
            print("Envoi touche impossible, le client n'est pas connecté au serveur.")

    def on_key_update(self):
        print(" | ".join([v for v in self._key_pressed]))

    def on_connected(self):
        self.initiate_talk()
        self._is_connected = True

    def get_socket(self):
        return self._socket

    socket = property(get_socket)

    def initialize_ihm(self):
        """Initialise toute l'IHM."""
        self.title("SuperClient")
        self.bind('<Button-2>', self.recreate_ihm)
        self.bind('<Button-3>', self.recreate_ihm)
        self.configure(background=self.theme['backgroundColor'])
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.mainFrame = IHM(master=self)
        self.mainFrame.grid(sticky='nesw')

    def recreate_ihm(self, event):
        """Recrée l'IHM, ce qui permet donc de changer certains paramètres comme le thème"""
        eventLog.add(event)
        log.add("Requête de changement de thème...")

        if self.theme is Themes.dark:
            self.theme = Themes.allBlue
        elif self.theme is Themes.allBlue:
            self.theme = Themes.dark

        temp = self.mainFrame
        self.mainFrame = IHM(master=self)
        self.mainFrame.grid(sticky='nesw')
        temp.destroy()
        log.add("Changement terminé. Thème: " + self.theme['id'])

    def connect_to_server(self, address=sokt.gethostname(), port=88000):
        if self._connectionThread is None:
            self._connectionThread = ConnectionThread(address, port, main_thread=self,
                                                      on_connected_func=self.on_connected)
        self._connectionThread.start()

    def initiate_talk(self):
        self._socket.setblocking(0)
        self.recvDataThread.start()
        self.sendDataThread.start()

    def send_msg(self, msg):
        if self._socket is not None:
            if isinstance(msg, str):
                ready_to_read, ready_to_write, in_error = \
                    select(
                        [self._socket],
                        [self._socket],
                        [self._socket],
                        60)
                if ready_to_write:
                    if msg != "":
                        self._socket.send(msg.encode('utf8'))
                        log.add(msg + " a été envoyé.")
                else:
                    log.add("Échec envoi message : le serveur est indisponible.")
                if in_error:
                    log.add("Le socket rencontre un problème.")
            else:
                raise TypeError("'msg' devrait être de type str. Type : " + str(type(msg)))
        else:
            log.add("L'application n'a pas de socket.")

    def broadcast(self, msg):
        """
        TODO
        :param msg: message à diffuser
        """
        self.send_msg(msg)

    def terminate(self, event=None):
        """Quitte l'application."""
        if event is not None:
            eventLog.add(event)
        self.isRunning = False
        try:
            self._socket.shutdown(sokt.SHUT_RDWR)
            self._socket.close()
        except OSError:
            pass
        try:
            self.destroy()
        except tk.TclError as err:
            log.add(str(err))
        log.add("Application terminée.")

    def test(self):
        """Montre comment se servir de la méthode after de tkinter pour avoir un appel récurrent avec un certain
        intervalle de temps déterminé."""
        log.add("lol")
        self.after(0, self.test())

    def wait_for_threads_to_finish(self):
        """
        TODO
        """
        self._connectionThread.join()
        try:
            self.sendDataThread.join()
            self.recvDataThread.join()
        except RuntimeError:
            pass


class IHM(MyFrame):
    """Hérité de MyFrame et définit toutes les caractéristique de l'IHM : les widgets, les évènements, le stream..."""

    def __init__(self, master):
        """
        Crée une IHM.

        Attributs :
        -master : parent de l'objet
        -default_photo : image
        -previous_nfps : variable mémoire qui garde le contenu de la dernière fois où la valeur de _spinbox_fps était
                         une entrée valide.

        Widgets :
        -tv : Canvas où est affiché le stream
        -buttons_frame : Cadre contenant buttons_group
        -buttons_group : Cadre contenant le groupe sud de boutons
            -userEntry : Champ permettant à l'utilisateur quelle fenêtre windows capturer pour le stream
            -spinbox_fps : Spinbox permettant à l'utilisateur de spécifier un nombre d'IPS pour le stream
            -les autres boutons sont définis sans référence dans la méthode place_widgets
        """
        self._app = master
        self.theme = master.theme
        super().__init__(master=master, bg=self.theme['backgroundColor'])
        self.master = master
        self.default_photo = ImageTk.PhotoImage(Image.open("{path}/../pictures/forest.jpg".format(
            path=get_modules_path())))
        self.previous_nfps: int = 1

        configure_columns_rows(self, 3, 1, clmn_weights=[5, 9, 5])

        self.tv = tk.Canvas(master=self, bg=self.theme['backgroundColor'])

        self.buttons_frame = MyFrame(master=self, bg=self.theme['buttonsBackgroundColor'])
        self.buttons_group = MyFrame(master=self.buttons_frame, bg=self.theme['buttonsBackgroundColor'])
        self._userEntry_StrV = tk.StringVar()
        self._userEntry = HintedUserEntry(master=self.buttons_group, hint=entry_hint, textvariable=self._userEntry_StrV,
                                          onreturn_func=self.send_msg, event_log=eventLog)
        self._userEntry.bind('<Return>', self.send_msg)
        self._spinbox_fps = CheckedSpinBox(self.buttons_group, 1, 999, "SpinBox_fps",
                                           hint='fps', event_log=eventLog)

        self.place_and_create_widgets()

    def send_msg(self, event):
        eventLog.add(event)
        text = self._userEntry.get()
        if text != "":
            self.master.send_msg(text)
            self._userEntry.delete(0, 'end')
        else:
            pass

    def place_and_create_widgets(self):
        """Place tous les widgets et en crée certains sans références."""

        def send_test(msg: str = "Message de Test"):
            self._app.broadcast(msg)

        if sys.platform == 'win32':
            def find_window(source_handle=0x00010100, dest_widget=self.tv):
                """Trouve la fenêtre spécifiée à l'aide de source_handle puis la copie sur le DC de dest_widget."""
                if isinstance(source_handle, str):
                    if source_handle != "" and source_handle != entry_hint:
                        source_handle = int(str(source_handle), 16)
                    else:
                        source_handle = None
                source_window_dc = win32gui.GetDC(source_handle)
                target_handle = dest_widget.winfo_id()
                target_window_dc = win32gui.GetDC(target_handle)

                mem_dc = win32gui.CreateCompatibleDC(target_window_dc)
                if mem_dc is None:
                    log.add("Échec de la création du compatibleDC.")
                    return

                dest_rect_dc = win32gui.GetClientRect(target_handle)
                print(dest_rect_dc)
                win32gui.SetStretchBltMode(target_window_dc, HALFTONE)

                # Copie le DC de la source vers le DC de destination en le redimensionnant
                win32gui.StretchBlt(
                    target_window_dc,
                    0, 0, dest_rect_dc[win32_RIGHT], dest_rect_dc[win32_BOTTOM],
                    source_window_dc,
                    0, 0, win32api.GetSystemMetrics(SM_CXSCREEN), win32api.GetSystemMetrics(SM_CYSCREEN),
                    SRCCOPY)

                source_bitmap = win32gui.CreateCompatibleBitmap(
                    target_window_dc,
                    dest_rect_dc[win32_RIGHT] - dest_rect_dc[win32_LEFT],
                    dest_rect_dc[win32_BOTTOM] - dest_rect_dc[win32_TOP])

                if source_bitmap is None:
                    log.add("Échec création bitmap.")
                    return

                win32gui.SelectObject(mem_dc, source_bitmap)
        else:
            """TODO"""

            def find_windows(*args, **kwargs):
                pass

        self.tv.grid(column=0, row=0, columnspan=3, sticky="nesw")
        self.tv.create_image(0, 0, image=self.default_photo, anchor='nw')

        self.buttons_frame.grid(column=1, row=1, sticky='ews')
        configure_columns_rows(self.buttons_frame, 3, 1, clmn_weights=[1, 20, 1])
        self.buttons_group.grid(column=1, padx='5p', sticky='ews')

        # Début buttons_group
        g = HandyIndexGenerator(0)
        mid_clmn = 2
        MyButton(self.buttons_group, text="Test connexion", command=send_test).grid(column=mid_clmn, row=g.next(),
                                                                                    sticky='ew')
        self._userEntry.grid(column=mid_clmn, row=g.next(), sticky='ew')
        MyButton(self.buttons_group, text="Find Window", command=lambda handle=self._userEntry: find_window(
            handle.get())).grid(column=mid_clmn - 1, row=g.next(), sticky='ew')
        self._spinbox_fps.grid(column=mid_clmn, row=g.same(), sticky='ew')
        MyButton(self.buttons_group, text="Find Window 2", command=lambda handle=0x00010100: find_window(handle)).grid(
            column=mid_clmn + 1, row=g.same(), sticky='ew')
        MyButton(self.buttons_group, text="Launch Stream").grid(column=mid_clmn - 1, row=g.next(), sticky='ew')
        MyButton(self.buttons_group, text="Refresh Stream").grid(column=mid_clmn, row=g.same(), sticky='ew')
        MyButton(self.buttons_group, text="Stop Stream").grid(column=mid_clmn + 1,
                                                              row=g.same(),
                                                              sticky='ew')
        MyButton(self.buttons_group, text="Quit", command=self.master.terminate).grid(column=mid_clmn, row=g.next(),
                                                                                      sticky='ew')
        configure_columns_rows(self.buttons_group, 5, g.get_n_given_ids(), clmn_weights=[1, 6, 6, 6, 1])
        del g
        # Fin buttons_frame


class ConnectionThread(Thread):
    def __init__(self, target_address, target_port, main_thread, on_connected_func):
        Thread.__init__(self, daemon=True)

        self._mainThread = main_thread
        self._socket = main_thread.socket
        self._targetAddress = target_address
        self._targetPort = target_port
        self._onConnected_func = on_connected_func

        self.isRunning = False

    def run(self):
        self.isRunning = True

        is_connected = False
        while not is_connected and self._mainThread.isRunning:
            log.add("Essai connection..")
            try:
                self._socket.connect((self._targetAddress, self._targetPort))
                log.add("Réussite.")
                is_connected = True
                self._onConnected_func()

            except ConnectionRefusedError:
                if self._mainThread.isRunning:
                    log.add(
                        "Connection refusée, peut-être le serveur est-il \
surchargé ou non connecté.")
        log.add("ConnectionThread terminée.")

        self.isRunning = False


class RecvDataThread(Thread):
    def __init__(self, main_thread):
        super().__init__(daemon=True)

        self._mainThread = main_thread
        self._socket = main_thread.socket
        self.hasToRun = True

    def run(self):
        log.add("RecvDataThread démarrée.")
        while self._mainThread.isRunning:
            ready_to_read, ready_to_write, in_error = \
                select(
                    [self._socket],
                    [self._socket],
                    [self._socket],
                    60)

            if ready_to_read:
                msg = self._socket.recv(2048).decode('utf8')
                log.add('Message reçu : "' + msg + '"')
                if msg == "q":
                    self._mainThread.terminate()
        log.add("RecvDataThread terminée.")


class SendDataThread(Thread):
    def __init__(self, main_thread):
        Thread.__init__(self, daemon=True)

        self._mainThread = main_thread
        self._socket = main_thread.socket

    def run(self):
        log.add("SendDataThread démarrée.")
        msg = ""
        while msg != "q" and self._mainThread.isRunning:
            ready_to_read, ready_to_write, in_error = \
                select(
                    [self._socket],
                    [self._socket],
                    [self._socket],
                    60)
            if ready_to_write:
                if msg != "":
                    self._socket.send(msg.encode('utf8'))
                    log.add(msg + " a été envoyé.")
        log.add("SendDataThread terminée")


def run_app():
    app = Application()
    app.initialize_ihm()
    app.connect_to_server(ADDRESS, PORT)

    app.mainloop()
    sys.exit()


def main():
    global log
    log = Log("SuperClient", True, get_modules_path() + "/../logs/log_client.log", 20, save=False)
    global eventLog
    eventLog = Log("SuperClientEvents", False, get_modules_path() + "/../logs/log_client_events.log", 25)
    eventLog.add("Lancement application...")
    # Lance l'application.
    safe_launch(run_app, log, eventLog)


if __name__ == '__main__':
    main()
