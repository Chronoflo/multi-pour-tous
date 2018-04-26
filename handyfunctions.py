#!/usr/bin/python
# -*- coding: <utf-8> -*-
import traceback
from datetime import datetime
from threading import Timer, Lock
from socket import gethostname
from os import makedirs
import tkinter as tk

ADDRESS = gethostname()
PORT = 90
KEY = 0
GAMEPAD = 1
MOUSE = 2

line_width = len("//SuperServeur::2018/04/06::00:03:48 : Application terminée.") * 3

# log = None
# eventLog = None


class Themes:
    """Classe qui contient différents sets de couleurs afin de facilement configurer l'apparence de l'application"""

    @classmethod
    def default(cls):
        """Définit le thème par défaut."""
        return cls.dark

    dark = {
        "id": 'dark',
        "buttonsColor": '#303035',
        "buttonsFontColor": '#DDDDDD',
        # buttonsFontColor = '#FFAC3F'
        "buttonsBackgroundColor": '#505055',
        "fieldsForegroundColor": '#FFAC3F',
        'fieldsHintColor': 'grey',
        'fieldsBackgroundColor': '#505055',
        'TextCursor': 'red',
        'backgroundColor': '#303035'
    }

    allBlue = {
        "id": 'allBlue',
        "buttonsColor": 'blue',
        "buttonsFontColor": 'white',
        "buttonsBackgroundColor": 'blue',
        "fieldsForegroundColor": 'yellow',
        'fieldsHintColor': 'lightgrey',
        'fieldsBackgroundColor': 'darkcyan',
        'TextCursor': 'lightblue',
        'backgroundColor': 'darkblue'
    }


class ListIterator(object):
    """Itérateur qui renvoie les différents éléments d'une liste, l'un après l'autre"""

    def __init__(self, values: list):
        self.i = -1
        self.nmax = len(values)
        self.values = values

    def __iter__(self):
        return self

    def __next__(self):
        return self.next()

    def next(self):
        if self.i < self.nmax:
            self.i += 1
            return self.values[self.i]
        else:
            raise StopIteration()


class HandyIndexGenerator:
    """Objet facilitant les opérations de placements en fournissant un système d'index relatifs"""

    def __init__(self, first_index: int):
        """
        Construit un HandyGenerator.
         :param first_index: premier index à renvoyer
         """
        if isinstance(first_index, int):
            self._index = first_index - 1
        else:
            raise ValueError("first_term devrait être un entier. Type : " + str(type(first_index)))

    def next(self):
        """Augmente de 1 index et retourne index"""
        self._index += 1
        return self._index

    def same(self):
        """Retourne le même index que le précédent"""
        return self._index

    def get_n_given_ids(self):
        """Retourne le nombre d'index qui ont été fournis"""
        return self._index + 1


class MyTkApp(tk.Tk):
    """MyTkApp hérite de tkinter.Tk en rajoutant comme propriété un thème."""
    def __init__(self, theme=Themes.default(), log=None, event_log=None, screenName=None, baseName=None,
                 className='MyTkApp', useTk=1, sync=0, use=None):
        """
        Construit un objet MyTkApp.
        :param theme: permet de spécifier un thème si l'on ne souhaite pas utiliser le thème par défaut
        """
        self.theme = theme
        self.log = log
        self.eventLog = event_log
        super().__init__(screenName, baseName, className, useTk, sync, use)

    def to_log(self, msg):
        if self.log is not None:
            self.log.add(msg)

    def to_eventlog(self, msg):
        if self.eventLog is not None:
            self.eventLog.add(msg)


class MyWidgets:
    """
    Classe abstraite qui définit les objets widgets. C'est la classe mère de tous les widgets.
    Ses instances ont pour propriétés d'hériter le thème de leurs maîtres si aucun autre n'est spécifié.
    """
    def __init__(self, master, theme_keys, theme, tk_attributes):
        """
        Crée un objet Widgets.
        :param master: doit être un objet tk
        :param theme_keys: sert à spécifier des propriétés de thème
        :param theme: à remplir si le thème ne doit pas être hérité du maître
        :param tk_attributes: sert à accepter tous les paramètres tk usuels
        """
        if theme is not None:
            self.theme = theme
        else:
            self.theme = master.theme
        if theme_keys is not None:
            if isinstance(theme_keys, dict):
                for k, v in theme_keys.items():
                    tk_attributes[k] = self.theme[v]
            else:
                raise TypeError("theme_keys should be dict. Current : " + str(type(theme_keys)))


class Fields(MyWidgets):
    """Classe abstraite qui définit les objets de types champ. (SpinBox, Field...)"""
    def __init__(self, master, theme_keys, theme, tk_attributes):
        """
        Crée un objet Fields.
        :param master: doit être un objet tk
        :param theme_keys: sert à spécifier des propriétés de thème
        :param theme: à remplir si le thème ne doit pas être hérité du maître
        :param tk_attributes: sert à accepter tous les paramètres tk usuels
        """
        if theme_keys is not None:
            theme_keys.update({'fg': 'fieldsForegroundColor'},
                              {'bg': 'fieldsBackgroundColor'})
        else:
            theme_keys = {'fg': 'fieldsForegroundColor',
                          'bg': 'fieldsBackgroundColor'}
        super().__init__(master, theme_keys, theme, tk_attributes)


class MyFrame(MyWidgets, tk.Frame):
    """Hérite de tk.Frame afin d'en faire un widget plus intelligent qui hérite son thème de son maître, si
    aucun autre n'est spécifié."""
    def __init__(self, master, theme_keys: dict=None, theme=None, **tk_attributes):
        """
        Crée un objet frame.
        :param master: doit être un objet tkinter
        :param theme_keys: sert à spécifier des propriétés définies dans un thème
        :param theme: à remplir si le thème ne doit pas être hérité du maître
        :param tk_attributes: sert à accepter tous les paramètres tk usuels
        """
        MyWidgets.__init__(self, master, theme_keys, theme, tk_attributes)  # complète tk_attributes
        tk.Frame.__init__(self, master=master, cnf=tk_attributes)


class MyButton(MyWidgets, tk.Button):
    """Un bouton personalisé équipé d'un thème et d'un log d'évènement."""
    def __init__(self, master, text="", command=None, event_log=None, theme_keys=None, theme=None, **tk_attributes):
        """
        Construit un objet MyButton.
        :param master: doit être un objet tk
        :param text: texte à afficher
        :param command: commande à exécuter
        :param event_log: log dans lequel rapporter les évènements
        :param theme_keys: sert à spécifier des propriétés de thème
        :param theme: à remplir si le thème ne doit pas être hérité du maître
        :param tk_attributes: sert à accepter tous les paramètres tk usuels
        """
        def scommand():
            if event_log is not None:
                event_log.add("<Button '{}' pressed>".format(text))
            if command is not None:
                command()
        MyWidgets.__init__(self, master, theme_keys, theme, tk_attributes)
        if 'fg' not in tk_attributes:
            tk_attributes['fg'] = self.theme['buttonsFontColor']
        if 'bg' not in tk_attributes:
            tk_attributes['bg'] = self.theme['buttonsColor']
        tk.Button.__init__(self, master, text=text, command=scommand, cnf=tk_attributes)


class FieldLabel(MyWidgets, tk.Label):
    """
    Un label qui accompagne un champ, par exemple pour servir de hint.
    Son thème est hérité de son maître.
    """
    def __init__(self, field_master, **kwargs):
        """Crée un FieldLabel."""
        tk.Label.__init__(self, field_master, bg=field_master['bg'], cnf=kwargs)


class HintedUserEntry(Fields, tk.Entry):
    """Une Entry équipée d'un hint (qui n'apparait que quand le champ est vide),
     et d'une fonction passé en paramètre qui est appelé lors d'un appui sur la touche 'Retour'"""

    def __init__(self, master, hint=None, onreturn_func=None, event_log=None, theme_keys=None, theme=None, **kwargs):
        """
        Crée une HintedUserEntry.
        :param master: doit être un objet tk
        :param hint: hint à afficher (aucun par défaut)
        :param onreturn_func:
        :param event_log:
        :param theme_keys:
        :param theme:
        :param kwargs:
        """
        Fields.__init__(self, master, theme_keys, theme, tk_attributes=kwargs)
        self._entry_wndHandle_stringVar = tk.StringVar()
        tk.Entry.__init__(self, master=master, textvariable=self._entry_wndHandle_stringVar, cnf=kwargs)

        self._name = self._name  # self._name correspond à l'identifiant hérité du widget
        self._eventLog = event_log

        self['fg'] = self.theme['fieldsHintColor']
        self._hint = hint
        self.bind("<FocusIn>", self._on_focus_in)
        self.bind("<FocusOut>", self._on_focus_out)
        if onreturn_func is not None:
            self.bind("<Return>", onreturn_func)
        if event_log is not None:
            self._eventLog = event_log
        self._entry_wndHandle_stringVar.set(hint)

    def _on_focus_in(self, event):
        """Appelée quand le focus est porté sur l'objet."""
        if self._hint is not None:
            if self._entry_wndHandle_stringVar.get() == self._hint:
                self._entry_wndHandle_stringVar.set("")
                self['fg'] = self.theme['fieldsForegroundColor']
        self._add_event(event)

    def _on_focus_out(self, event):
        """Appelée quand l'objet perd le focus."""
        if self._entry_wndHandle_stringVar.get() == "":
            self['fg'] = self.theme['fieldsHintColor']
            self._entry_wndHandle_stringVar.set(self._hint)
        self._add_event(event)

    def _add_event(self, event):
        """Ajoute une entrée dans le log d'évènements."""
        if self._eventLog is not None:
            if self._hint is not None:
                self._eventLog.add("<" + self._name + " '" + self._hint + "' : " + str(event) + ">")
            else:
                self._eventLog.add(event)


class CheckedSpinBox(Fields, tk.Spinbox):
    """Une tk.SpinBox qui vérifie son contenu et peut afficher un hint sur le côté."""
    def __init__(self, master, from_, to, name: str="", hint: str =None, onupdate_func=None, event_log=None,
                 theme_keys=None, theme=None, **tk_attributes):
        """
        Crée une CheckedSpinBox.
        :param master: doit être un objet tk
        :param from_: minimum
        :param to: maximum
        :param name: nom à afficher dans le log
        :param hint: indice à afficher (aucun par défaut)
        :param onupdate_func: fonction qui doit être appelée à chaque mise à jour valide de la SpinBox
        :param event_log: journal dans lequel rapporter les évènements
        :param theme_keys: sert à spécifier des propriétés de thèmes
        :param theme: sert à spécifier un thème (hérite du maître par défaut)
        :param tk_attributes: sert à accepter les paramètres tk usuels
        """
        Fields.__init__(self, master, theme_keys, theme, tk_attributes)
        self._SpinBoxValue = tk.StringVar()
        tk.Spinbox.__init__(self, master, textvariable=self._SpinBoxValue, from_=from_, to=to, cnf=tk_attributes)

        self._event_log = event_log
        self._SpinBoxValue.trace_add('write', self.on_spin_changed)
        self._name = name
        self._hint: str = hint
        self._onUpdate_func = onupdate_func
        self._previous_n = 0

        # Configuration étiquette indice
        if self._hint is not None:
            self._label = FieldLabel(field_master=self.master, text=self._hint, fg='darkgray', font=('Helvetica', 7))
            self._label['fg'] = self.theme['fieldsHintColor']

    def grid(self, column: int, row: int, **kwargs):
        """Surcharge la méthode grid pour ajouter un label au même endroit que la spinbox."""
        tk.Spinbox.grid(self, column=column, row=row, cnf=kwargs)
        # Configuration petit texte sur le côté droit
        if self._hint is not None:
            self.columnconfigure(0, weight=1)
            self._label.grid(column=column, row=row, padx='10p', sticky='e')

    def on_spin_changed(self, a, b, c):
        """Vérifie ce qu'entre l'utilisateur dans la spinbox_fps quand son état change, puis
         met à jour les paramètres du stream si l'entrée est valide.
            Les entrées refusées sont celles:
                - qui ne sont pas des réels positifs
                - qui comportent plus de 8 caractères
                - qui sont supérieures à 999"""
        if self._event_log is not None:
            self._event_log.add("<CheckedSpinBox '{}' : state changed>".format(self._name))
            del a
            del b
            del c
        var = self._SpinBoxValue
        nfps = var.get()
        if len(nfps) <= 8:
            # enlève les espaces
            nfps = "".join([i for i in nfps if i != " "])
            # Vérifie l'entrée en tentant une conversion
            try:
                temp = float(nfps)
                if temp <= 0 or temp > 999:
                    raise ValueError
            except ValueError:
                var.set(self._previous_n)
            else:
                self._previous_n = nfps
                var.set(nfps)
                # Met à jour le stream
                if self._onUpdate_func is not None:
                    self._onUpdate_func()
        else:
            var.set(self._previous_n)


class InfiniteTimer:
    """A Timer class that does not stop, unless you want it to. Celle-là je l'ai copiée."""
    createdThreads = []

    @classmethod
    def kill_threads(cls):
        for thread in cls.createdThreads:
            thread.cancel()

    def __init__(self, seconds, target, name=None):
        self._should_continue = False
        self.is_running = False
        self.seconds = seconds
        self.target = target
        self.thread = None
        self._name = name
        InfiniteTimer.createdThreads.append(self)

    def _handle_target(self):
        self.is_running = True
        self.target()
        self.is_running = False
        self._start_timer()

    def _start_timer(self):
        if self._should_continue:  # Code could have been running when cancel was called.
            self.thread = Timer(self.seconds, self._handle_target)
            if self._name is not None:
                self.thread.name = self._name
            self.thread.start()

    def start(self):
        if not self._should_continue and not self.is_running:
            self._should_continue = True
            self._start_timer()
        else:
            print("Timer already started or running, please wait if you're restarting.")

    def cancel(self):
        if self.thread is not None:
            self._should_continue = False  # Just in case thread is running and cancel fails.
            self.thread.cancel()
        else:
            pass


class Log:
    """Thread chargée de rapporter chaque évènement notable. Il faut appeler .add()
    pour ajouter de nouvelles entrées."""
    _created_logs = list()
    _started_logs = list()
    _used_ids: set = set()

    @classmethod
    def save_all(cls):
        """Sauvegarde tous les logs crées. TODO : c'est nul"""
        for log in cls._created_logs:
            log.save()

    @classmethod
    def final_save_all(cls):
        """Sauvegarde finale de tous les logs crées."""
        for log in cls._created_logs:
            log.final_save()
        for log in cls._created_logs:
            print("//FIN_LOG '{}'".format(log.name))

    def __init__(self, tag: str, should_print: bool=True, file_path: str=None, n_entries_before_save: int=20):
        """
        Crée un Log.
        :param tag: identifiant du log (doit être unique)
        :param should_print:
        :param file_path:
        :param n_entries_before_save:
        """
        check_var_types(
            (tag, 'tag', str),
            (should_print, 'should_print', bool),
            (file_path, 'file_path', str),
            (n_entries_before_save, 'n_entries_before_save', int)
        )

        if tag in Log._used_ids:
            raise ValueError('Ce tag est déjà utilisé.')
        else:
            Log._used_ids.add(tag)
        self.name = "Log_" + tag
        self._TAG: str = tag
        self._shouldPrint: bool = should_print

        self._filePath: str = file_path
        if self._filePath is not None:
            write_to_file(self._filePath, make_line('~'))

        self._hasToRun: bool = True
        self.entriesOnMem: list = []
        self.nEntriesBeforeSave: int = n_entries_before_save
        self._lock = Lock()
        Log._created_logs.append(self)
        print("//DÉBUT_LOG '{}'".format(self.name))

    def add(self, msg):
        """Ajoute une entrée au log."""
        with self._lock:
            line = "//{TAG}::{date} : {msg}".format(TAG=self._TAG,
                                                    date=datetime.now().strftime("%Y/%m/%d::%H:%M:%S"),
                                                    msg=str(msg))
            if self._shouldPrint:
                print(line)
            self.entriesOnMem.append(line)
            if len(self.entriesOnMem) >= self.nEntriesBeforeSave and self._filePath is not None:
                self.save(lock_already_acquired=True)

    def save(self, lock_already_acquired=False):
        """Sauvegarde toutes les entrées contenues dans entriesOnMem"""
        if self._filePath is not None:
            if lock_already_acquired:
                self._try_to_save()
            else:
                with self._lock:
                    self._try_to_save()

    def _try_to_save(self):
        try:
            write_to_file(self._filePath, "".join([entry + "\n" for entry in self.entriesOnMem]))
            self.entriesOnMem.clear()
            print("//SAUVEGARDE '{}'".format(self.name))
        except PermissionError:
            print("//ÉCHEC SAUVEGARDE")

    def final_save(self):
        if self._filePath is not None:
            is_final_save_successful = False
            while not is_final_save_successful:
                try:
                    write_to_file(self._filePath,
                                  "".join([entry + "\n" for entry in self.entriesOnMem])
                                  + make_line('~', end='\n'))
                    is_final_save_successful = True
                    print("//SAUVEGARDE FINALE '{}'".format(self.name))
                except PermissionError:
                    print("//ÉCHEC SAUVEGARDE. NOUVEL ESSAI...")


def check_var_types(*args):
    """
    Vérifie le type des variables passées en paramètres.

    Les variables doivent être présentées sous la forme de tuples avec (la variable, son nom, et le type à vérifier).
    """
    for var, var_name, var_type in args:
        if not isinstance(var, var_type):
            raise TypeError("'{}' devrait être de type {} mais est de type {}.".format(var_name, var_type, type(var)))


def is_slash(char: str):
    """Retourne Vrai si char est un slash."""
    char = str(char)
    if len(char) == 1:
        return char == '/' or char == '\\'
    else:
        raise ValueError("char should be a single character.")


def check_path(path):
    """Vérifie que le chemin existe et crée les dossiers nécessaires le cas échéant."""
    path = str(path)
    path_to_check = ""
    # Récupère le chemin jusqu'au dernier slash
    for i, letter in enumerate(path[::-1]):
            if is_slash(letter):
                path_to_check = path[:-i]
                break
    # Crée les dossiers correspondants s'ils n'existent pas déjà.
    if path_to_check:
        makedirs(path_to_check, exist_ok=True)
    else:
        print("Il n'y avait pas de dossiers à vérifier.")


def write_to_file(path, data):
    """Écrit data dans le fichier spécifié."""
    if path is not None:
        check_path(path)
        with open(path, 'a') as f:
            f.write(data)
        return True
    else:
        return False


def configure_columns_rows(tk_obj, n_columns: int, n_rows: int, clmn_weights: list = None, row_weights: list = None):
    """"Facilite la configuration des colonnes et des lignes de grid d'un objet Tk."""
    if clmn_weights is not None:
        weights_clmn_iter = ListIterator(clmn_weights)
        for i in range(n_columns):
            tk_obj.columnconfigure(index=i, weight=next(weights_clmn_iter))
    else:
        for i in range(n_columns):
            tk_obj.columnconfigure(index=i, weight=1)

    if row_weights is not None:
        weights_row_iter = ListIterator(row_weights)
        for i in range(n_rows):
            tk_obj.rowconfigure(index=i, weight=next(weights_row_iter))
    else:
        for i in range(n_rows):
            tk_obj.rowconfigure(index=i, weight=1)


def pip_install(package_name: str):
    """Installe un paquet à l'aide de pip."""
    if isinstance(package_name, str):
        import pip
        pip.main(['install', package_name])
    else:
        raise TypeError("package_name should be a string.")


def make_line(char, end='\n'):
    """Retourne une ligne faite à partir de char et de end"""
    char = str(char)
    if len(char) == 1:
        return "".join([char for i in range(line_width)]) + end
    else:
        raise ValueError("char should be a single character.")


def formatted_error(error):
    """Retourne une erreur encadrée par des lignes de points."""
    return ('\n'
            + make_line('.')
            + error
            + make_line('.', end=""))


def safe_launch(func, log, event_log):
    # noinspection PyBroadException
    try:
        func()
    except Exception:
        log.add(formatted_error(traceback.format_exc()))
        Log.save_all()
    finally:
        event_log.add("Fin application.")
        InfiniteTimer.kill_threads()
        Log.final_save_all()


def _create_main_frame(master):
    """Fonction de démonstration, à ne pas utiliser à de vraies fins."""
    frame = MyFrame(master=master, bg='blue')
    frame.grid(ipadx='4p', ipady='4p', sticky='nesw')
    configure_columns_rows(frame, 1, 4)
    # Début frame
    tk.Label(frame, text='Démonstration HandyFunctions', font=('Helvetica', 36)).grid(sticky='nesw')
    MyButton(frame, text='Changement de thème', command=lambda x=master, y=frame: _switch_theme(x, y)).grid()
    MyButton(frame, text='lol', fg='purple', bg='lightblue').grid(sticky='nesw')
    MyButton(frame, text='Quitter', command=master.destroy).grid(sticky='nesw')
    # Fin frame


def _switch_theme(root, main_frame):
    """Fonction de démonstration, à ne pas utiliser pour de vraies fins."""
    ExampleLog.add("Changement de thème...")
    if root.theme is Themes.dark:
        root.theme = Themes.allBlue
    elif root.theme is Themes.allBlue:
        root.theme = Themes.dark
    _create_main_frame(root)
    main_frame.destroy()
    ExampleLog.add("Terminé.")


def main():
    root = MyTkApp(theme=Themes.dark)
    configure_columns_rows(root, 1, 1)
    _create_main_frame(root)
    root.mainloop()


if __name__ == '__main__':
    ExampleLog = Log('ExampleLog')
    main()
    Log.final_save_all()
