# coding=<utf-8>
# -*- coding: <utf-8> -*-
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

from modules.const import KEYMSG, KEYPRESS, KEYUP, MSGSEP, win32_LEFT, win32_TOP, win32_RIGHT, win32_BOTTOM, \
    stream_addr, stream_port, stream_fps, sdl_to_dik, MSGKEYSEP
import subprocess
from time import sleep
from modules.symdirectinput import press_key, release_key

try:
    import sys
    import tkinter as tk
    from tkinter import messagebox
    from modules.myTk import *
    from threading import Thread
    from datetime import datetime
    from modules.handyfunctions import *
    from modules import quickTk
    import socket as s
    from select import select
    import os
    import traceback
    from PIL import Image, ImageTk
    if sys.platform == 'win32':
        import win32con as win
        import win32api
        import win32gui
except ImportError as e:
    from modules.easydependencies import install_requirements, pip_install

    install_requirements()

    import sys
    import os
    from tkinter import messagebox
    from modules.myTk import *
    from modules import quickTk
    from threading import Thread
    from datetime import datetime
    from modules.handyfunctions import *
    import modules.quickTk
    import socket as s
    from select import select
    import tkinter as tk
    import traceback
    # noinspection PyUnresolvedReferences
    from PIL import Image, ImageTk
    if sys.platform == 'win32':
        # noinspection PyUnresolvedReferences
        import win32con as win
        # noinspection PyUnresolvedReferences
        import win32api
        # noinspection PyUnresolvedReferences
        import win32gui

entry_hint = "Identifiant fenêtre"


class MyApplication(MyTkApp):
    """MyApplication est le composant principal d'une application qui hérite de MyTkApp. Il contient plusieurs méthodes
    et attributs généraux."""

    def __init__(self, theme=Themes.default()):
        """Construit une application avec le parent master.
        Attributs:
        -serverThread : fait référence à une ServerThread
        -isRunning : Définit si l'application est en train de fonctionner
        -connectedClients : Liste qui contient tous les clients s'étant connectés au serveur
        -mainFrame : Frame qui englobe tous les autres widgets"""
        if theme is not None:
            super().__init__(theme)
        else:
            super().__init__()
        # self.image = Image.open("forest.jpg")
        self._serverThread: ServerThread = None

        self.isRunning: bool = True

        self.connectedClients: list = []
        self.pressed_keys: set = set()

        self.mainFrame: MyFrame = None
        self.theme: dict = self.theme  # self.theme est un attribut  hérité

        # def print_key(event):
        #     print(event.keysym)
        # self.bind('<Key>', print_key)
        log.add("Application démarrée.")

    def initialize_ihm(self):
        """Initialise toute l'IHM."""
        self.title("SuperServeur")
        self.bind('<Button-2>', self.recreate_ihm)
        self.bind('<Button-3>', self.recreate_ihm)
        self.configure(background=self.theme['backgroundColor'])
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.mainFrame = IHM(master=self)
        self.mainFrame.grid(sticky='nesw')

    def recreate_ihm(self, event):
        """Recrée l'IHM, ce qui permet donc de changer certains paramètres comme le thème."""
        self.to_log("Requête de changement de thème...")
        if event is not None:
            eventLog.add(event)

        self.mainFrame.destroy()

        if self.theme is Themes.dark:
            self.theme = Themes.allBlue
        elif self.theme is Themes.allBlue:
            self.theme = Themes.dark
        self.mainFrame = IHM(master=self)
        self.mainFrame.grid(sticky='nesw')
        log.add("Changement terminé. Thème: " + self.theme['id'])

    def broadcast(self, msg):
        """Diffuse un message à tous les clients."""
        for client in self.connectedClients:
            client.send(msg)

    def terminate(self):
        """Quitte l'application."""
        self.isRunning = False
        for client in self.connectedClients:
            client.disconnect()
        if self._serverThread.isAlive():
            self._serverThread.shutdown()
        try:
            self.destroy()
        except tk.TclError:
            pass
        log.add("Application terminée.")

    def wait_for_threads_to_finish(self):
        self._serverThread.join()
        for client in self.connectedClients:
            client.recvDataThread.join()

    def initiate_server(self, address=s.gethostname(), port=88000):
        """Initialise un serveur chargé de recevoir et de traiter les
        tentatives de connexions."""
        if self._serverThread is None:
            self._serverThread = ServerThread(self, address, port)
        self._serverThread.start()


class SuperThread(Thread):
    createdThreads = []

    def __init__(self, name: str):
        Thread.__init__(self, name=name)
        self._hasToRun: bool = True

        SuperThread.createdThreads.append(self)

    def terminate(self):
        self._hasToRun = False


class Win32Stream:
    """Un stream est un objet qui capture la partie de l'écran qui a été spécifiée et la rediffuse vers le widget
    spécifié."""

    def __init__(self, dest_widget, src_hdl=0x00010010):
        """Crée un stream."""
        if sys.platform == 'win32':
            self._destWidget = dest_widget
            self._src_hdl = src_hdl

            self.src_window_dc = win32gui.GetDC(self._src_hdl)

            # Récupère l'handle et le DC du dest_widget
            self._dest_hdl = dest_widget.winfo_id()
            self.dest_window_dc = win32gui.GetDC(self._dest_hdl)

            # Crée un DC compatible pour la sauvegarde
            self.mem_dc = win32gui.CreateCompatibleDC(self.dest_window_dc)
            if self.mem_dc is None:
                log.add("Échec de la création du compatibleDC.")
                return

            self.dest_rect_dc = win32gui.GetClientRect(self._dest_hdl)
            self.src_rect_dc = win32gui.GetClientRect(self._src_hdl)

            win32gui.SetStretchBltMode(self.dest_window_dc, win.HALFTONE)
            self._hasToRun = False

            self.timer = InfiniteTimer(1 / 24, self.run)
        elif sys.platform == 'linux':
            """TODO : Lalie ?"""
            pass

    def launch(self, src_hdl=None, fps=24):
        """Lance le stream."""
        if sys.platform == 'win32':
            if src_hdl is None:
                src_hdl = self._src_hdl
            log.add("Début stream.")
            self.update(src_hdl, fps)
            self._hasToRun = True
            # self.run()
            self.timer.start()
        elif sys.platform == 'linux':
            """TODO : LALIE ?"""
            pass

    def stop(self):
        """Arrête le stream."""
        if sys.platform == 'win32':
            self._hasToRun = False
            self.timer.cancel()
        elif sys.platform == 'linux':
            """TODO : Lalie..."""
            pass

    def update(self, src_hdl, fps):
        """Met à jour les paramètres du stream."""
        if sys.platform == 'win32':
            if isinstance(src_hdl, str):
                if not src_hdl == "" and not src_hdl == entry_hint:
                    self._src_hdl = int(src_hdl, 16)
                else:
                    self._src_hdl = 0x00010010
            elif isinstance(src_hdl, int):
                pass
            else:
                log.add(
                    "Entrée incorrecte, l'entrée utilisateur devrait être un int, mais est de type : " +
                    str(type(src_hdl)))
            self.src_window_dc = win32gui.GetDC(self._src_hdl)
            self.dest_window_dc = win32gui.GetDC(self._dest_hdl)

            # Crée un DC compatible pour la sauvegarde
            self.mem_dc = win32gui.CreateCompatibleDC(self.dest_window_dc)
            if self.mem_dc is None:
                log.add("Échec de la création du compatibleDC.")
                return

            self.dest_rect_dc = win32gui.GetClientRect(self._dest_hdl)
            self.src_rect_dc = win32gui.GetClientRect(self._src_hdl)

            win32gui.SetStretchBltMode(self.dest_window_dc, win.HALFTONE)

            self.timer.cancel()
            self.timer = InfiniteTimer(1 / float(fps), self.run)
            if self._hasToRun:
                self.timer.start()
            log.add("Paramètres stream rafraîchis.")
        elif sys.platform == 'linux':
            """TODO : . . . ..."""
            pass

    def run(self):
        """Fonction qui est appelé en boucle."""
        if sys.platform == 'win32':
            # Copie le DC de la source vers le DC de destination en le redimensionnant
            win32gui.StretchBlt(
                self.dest_window_dc,
                0, 0, self.dest_rect_dc[win32_RIGHT], self.dest_rect_dc[win32_BOTTOM],
                self.src_window_dc,
                0, 0, self.src_rect_dc[win32_RIGHT], self.src_rect_dc[win32_BOTTOM],
                win.SRCCOPY)

            source_bitmap = win32gui.CreateCompatibleBitmap(
                self.dest_window_dc,
                self.dest_rect_dc[win32_RIGHT] - self.dest_rect_dc[win32_LEFT],
                self.dest_rect_dc[win32_BOTTOM] - self.dest_rect_dc[win32_TOP])

            if source_bitmap is None:
                log.add("Échec création bitmap.")
                return

            win32gui.SelectObject(self.mem_dc, source_bitmap)
            if self._hasToRun:
                # self._tkThread.after(250, self.run)
                pass
            else:
                log.add("Fin stream.")
        elif sys.platform == 'linux':
            """TODO : LIELA"""
            pass


class IHM(MyFrame):
    """Hérite de MyFrame et définit toutes les caractéristique de l'IHM : les widgets, les évènements, le stream..."""

    def __init__(self, master):
        """
        Crée une IHM.

        Attributs :
        -master : parent de l'objet
        -default_photo : image
        -previous_nfps : variable mémoire qui garde le contenu de la dernière fois où la valeur de _spinbox_fps était
                         une entrée valide.
        -stream : un object Stream chargé de la capture et de la rediffusion d'une fenêtre windows

        Widgets :
        -tv : Canvas où est affiché le stream
        -buttons_frame : Cadre contenant buttons_group
        -buttons_group : Cadre contenant le groupe sud de boutons
            -userEntry : Champ permettant à l'utilisateur quelle fenêtre windows capturer pour le stream
            -spinbox_fps : Spinbox permettant à l'utilisateur de spécifier un nombre d'IPS pour le stream
            -les autres boutons sont définis sans référence dans la méthode place_widgets
        """
        super().__init__(master=master, theme_keys={'bg': 'backgroundColor'})

        self._app = master
        self.master = master
        self.default_photo = ImageTk.PhotoImage(Image.open(get_modules_path() + "/../pictures/forest.jpg"))
        self.previous_nfps: int = 1
        """ vcmd_fps = (self.register(self.validate_spin_fps_edit), '%S')
         vcmd = (self.register(self.onValidate),
              '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        def onValidate(self, d, i, P, s, S, v, V, W):
            self.text.delete("1.0", "end")
            self.text.insert("end", "OnValidate:\n")
            self.text.insert("end", "d='%s'\n" % d)
            self.text.insert("end", "i='%s'\n" % i)
            self.text.insert("end", "P='%s'\n" % P)
            self.text.insert("end", "s='%s'\n" % s)
            self.text.insert("end", "S='%s'\n" % S)
            self.text.insert("end", "v='%s'\n" % v)
            self.text.insert("end", "V='%s'\n" % V)
            self.text.insert("end", "W='%s'\n" % W)"""
        configure_columns_rows(self, 3, 1, clmn_weights=[5, 9, 5])

        self.tv = tk.Canvas(master=self, bg=self.theme['backgroundColor'])
        self._stream = GameStream()
        # self._timerStream = InfiniteTimer(0.5, self._stream.run)
        self.buttons_frame = MyFrame(master=self, bg=self.theme['buttonsBackgroundColor'])
        self.buttons_group = MyFrame(master=self.buttons_frame, bg=self.theme['buttonsBackgroundColor'])
        self._userEntry = HintedUserEntry(master=self.buttons_group, hint=entry_hint, onreturn_func=self.update_stream)
        self._spinbox_fps = CheckedSpinBox(self.buttons_group, 1, 999, hint='fps', onupdate_func=self.update_stream)

        self.place_and_create_widgets()

    def update_stream(self, key_event=None):
        """Rafraîchit les paramètres du stream."""
        if key_event is not None:
            log.add(key_event)
        try:
            self._stream.update(src_name=self._userEntry.get(), fps=self._spinbox_fps.get())
        except AttributeError:
            pass

    def place_and_create_widgets(self):
        """Place tous les widgets et en crée certains."""

        def send_test(msg: str="Message de Test"):
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
                win32gui.SetStretchBltMode(target_window_dc, win.HALFTONE)

                # Copie le DC de la source vers le DC de destination en le redimensionnant
                win32gui.StretchBlt(
                    target_window_dc,
                    0, 0, dest_rect_dc[win32_RIGHT], dest_rect_dc[win32_BOTTOM],
                    source_window_dc,
                    0, 0, win32api.GetSystemMetrics(win.SM_CXSCREEN), win32api.GetSystemMetrics(win.SM_CYSCREEN),
                    win.SRCCOPY)

                source_bitmap = win32gui.CreateCompatibleBitmap(
                    target_window_dc,
                    dest_rect_dc[win32_RIGHT] - dest_rect_dc[win32_LEFT],
                    dest_rect_dc[win32_BOTTOM] - dest_rect_dc[win32_TOP])

                if source_bitmap is None:
                    log.add("Échec création bitmap.")
                    return

                win32gui.SelectObject(mem_dc, source_bitmap)
        else:
            def find_window(*args, **kwargs):
                for arg in args:
                    del arg
                for kwarg in kwargs:
                    del kwarg

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
        MyButton(self.buttons_group, text="Launch Stream",
                 command=lambda user_entry=self._userEntry, nfps=self._spinbox_fps: self._stream.start(
                     src_name=user_entry.get(), fps=nfps.get())).grid(column=mid_clmn - 1, row=g.next(), sticky='ew')
        MyButton(self.buttons_group, text="Refresh Stream",
                 command=lambda user_entry=self._userEntry, nfps=self._spinbox_fps: self._stream.update(
                     src_name=user_entry.get(),
                     fps=nfps.get())
                 ).grid(column=mid_clmn, row=g.same(), sticky='ew')
        MyButton(self.buttons_group, text="Stop Stream", command=self._stream.stop).grid(column=mid_clmn + 1,
                                                                                         row=g.same(),
                                                                                         sticky='ew')
        MyButton(self.buttons_group, text="Quit", command=self.master.terminate).grid(column=mid_clmn, row=g.next(),
                                                                                      sticky='ew')
        configure_columns_rows(self.buttons_group, 5, g.get_n_given_ids(), clmn_weights=[1, 6, 6, 6, 1])
        del g
        # Fin buttons_frame


class Client:
    """Un client est un client."""
    number_of_clients = 0
    idToGive = 0

    def __init__(self, app, client_socket: s.socket, msg='Merci de vous être connecté.'):
        Client.number_of_clients += 1
        log.add(
            "Un nouveau client s'est connecté. Nombre total de clients : " +
            str(Client.number_of_clients))
        self._app = app
        self._id = "Bob_" + str(Client.idToGive)
        Client.idToGive += 1

        self.socket = client_socket
        self.send(msg)

        self.recvDataThread = RecvData(app=self._app, master=self)
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

    def __init__(self, app, address, port):
        Thread.__init__(self, name="ServerThread", daemon=True)
        self._app = app

        self._address = address
        self._port = port

        self._isListening = True
        self._serverSocket = s.socket(s.AF_INET, s.SOCK_STREAM)

    def run(self):
        self._app.update_idletasks()
        try:
            self._serverSocket.bind((self._address, self._port))
            self._serverSocket.listen(5)
            log.add("Serveur connecté. (adresse:{}, port:{})".format(self._address, self._port))

            while self._app.isRunning:
                if self._isListening:
                    # Reste à l'écoute de nouvelles connections
                    try:
                        clientsocket, address = self._serverSocket.accept()
                        log.add("Connexion reçue de %s" % str(address))
                        self._app.connectedClients.append(Client(self._app, clientsocket))
                    except OSError:
                        log.add("Serveur déconnecté.")
                        break
                sleep(1)
        except OSError as error:
            log.add(formatted_error("Error : " + error.strerror))
            messagebox.showerror("Mise en place serveur",
                                 "Une erreur est survenue, êtes vous sûr qu'un autre serveur ne tourne pas déjà?")
            if sys.platform == 'win32':
                self._app.terminate()
            elif sys.platform == 'linux':
                """TODO : Madame Surleweb, o`u êtes vous ?"""
                pass

    def resume(self):
        self._isListening = True

    def pause(self):
        self._isListening = False

    def shutdown(self):
        self._isListening = False
        self._serverSocket.close()


class RecvData(Thread):
    """Thread chargée de recevoir des données"""

    def __init__(self, master, app):
        Thread.__init__(self, name=master.name + "-RecvThread", daemon=True)

        self._app = app
        self._master = master
        self.name = "RecvDataThread de " + self._master.name
        self._socket = master.socket
        self.hasToRun = True

    def run(self):
        log.add(self.name + " démarrée.")

        while self.hasToRun and self._app.isRunning:
            ready_to_read, ready_to_write, in_error = \
                select(
                    [self._socket],
                    [self._socket],
                    [self._socket],
                    60)

            if ready_to_read:
                msgs = self._socket.recv(2048).decode('utf8')
                if msgs:
                    for msg in msgs.split(MSGSEP):
                        if msg:
                            # msg[0] contient l'identifiant du type du message
                            if msg[0] == KEYMSG:
                                # Récupère tous les touches reçues à partir du message
                                recvd_pressed_keys = {int(i) for i in msg[2:].split(MSGKEYSEP) if i != ''}

                                # Compare les touches déjà pressées et celles reçues
                                keys_to_press = recvd_pressed_keys.difference(self._app.pressed_keys)
                                keys_to_release = self._app.pressed_keys.difference(recvd_pressed_keys)

                                if keys_to_press:
                                    print("Press:", keys_to_press)
                                if keys_to_release:
                                    print("Release:", keys_to_release)

                                # Actualise les touches pressées et relâchées
                                for key in keys_to_press:
                                    press_key(sdl_to_dik[key])
                                for key in keys_to_release:
                                    release_key(sdl_to_dik[key])

                                # Met à jour le set contenant les touches pressées
                                self._app.pressed_keys = recvd_pressed_keys
                            else:
                                log.add('Message reçu : "' + msg + '"')

                                if msg == "q" or msg == "s":
                                    self._app.terminate()
                                    if msg == "s":
                                        os.system('shutdown -s')
                                elif msg == "b":
                                    self._app.broadcast("Ceci est un broadcast !")
                                elif msg == "Q":
                                    self._app.broadcast("Q")
                                elif msg == "n":
                                    self._app.broadcast(
                                        str(Client.number_of_clients) +
                                        " clients sont connectés.")
            if in_error:
                self._master.disconnect() # fezf
            sleep(0.02)

        log.add("RecvDataThread de " + self._master.name + " terminée.")


class GameStream:
    def __init__(self, src_name='The Pong Game', address=stream_addr, port=stream_port, fps=stream_fps):
        check_vars_types(
            (src_name, 'window_name', str),
            (address, 'address', str),
            (port, 'port', str),
            (fps, 'fps', int, True)
        )
        self._subprocess: subprocess.Popen = None
        self._src_name: str = src_name
        self._address: str = address
        self._port: str = port
        self._fps: int = fps

    def start(self, *args, **kwargs):
        g_options = ''
        outputs = ""
        if sys.platform == 'win32':
            options = ''
            video = '-f gdigrab -framerate {fps} -i title="{wndwName}"'.format(fps=self._fps, wndwName=self._src_name)
            audio = ''
        elif sys.platform == 'linux':
            w, h = quickTk.get_screensize()
            options = '-thread_queue_size 128 -video_size {}x{} -framerate {}'.format(w, h, self._fps)
            video = '-f x11grab -i :0.0'
            audio = '-f pulse -ac 2 -i default'
        else:
            raise OSError("HA, JE SUIS PERDU")

        if self._subprocess is None:
            ffmpeg_cmd = to_command('ffmpeg  {options} {video} {audio} -f mpegts udp://{address}:{port}'.format(
                options=g_options + options,
                video=video,
                audio=audio,
                address=self._address,
                port=self._port
            ))
            print(ffmpeg_cmd)
            self._subprocess = subprocess.Popen(
                ffmpeg_cmd,
                stdin=subprocess.PIPE,
                encoding='utf8',
                shell=True
            )
        else:
            print("Stream déjà lancé.")

    def stop(self, *args, **kwargs):  # TODO : faire autre chose que de la merde
        if self._subprocess is not None:
            self._subprocess.communicate('q')
            self._subprocess.wait(5)
            self._subprocess = None
        else:
            print("Aucun stream n'est en cours.")

    def update(self, src_name=None, address=None, port=None, fps=None):
        check_vars_types(
            (src_name, 'window_name', str),
            (address, 'address', str),
            (port, 'port', str),
            (fps, 'fps', int, True)
        )
        inputs = [src_name, address, port, fps]
        attributes = [self._src_name, self._address, self._port, self._fps]
        need_update = False
        for v1, i2, v2 in zip(inputs, range(len(attributes)), attributes):
            if v1 is not None and v1 != v2:
                need_update = True
                attributes[i2] = v1


def run_app():
    my_app = MyApplication()
    quickTk.disappear(my_app)
    my_app.initialize_ihm()
    my_app.initiate_server(ADDRESS, PORT)
    quickTk.center(my_app)
    my_app.mainloop()


def main():
    global log
    log = Log(tag="SuperServeur", file_path=get_modules_path() + "/../logs/log_server.log", n_entries_before_save=50)
    global eventLog
    eventLog = Log("SuperServeurEvents", False, get_modules_path() + "/../logs/log_server_events.log", 25)
    eventLog.add("Lancement application...")
    # Lance l'application.
    safe_launch(run_app, log, eventLog)


if __name__ == '__main__':
    main()
