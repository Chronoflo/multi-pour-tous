#!/usr/bin/python
# -*- coding: <utf-8> -*-
try:
    import tkinter as tk
except ImportError:
    from modules.easydependencies import ensure_tkinter
    ensure_tkinter()
    import tkinter as tk
import traceback
from datetime import datetime
from threading import Timer, Lock
from inspect import currentframe, getfile
from socket import gethostname
from os import makedirs

ADDRESS = gethostname()
PORT = 3400

KEY = 0
GAMEPAD = 1
MOUSE = 2

BEFORE = 1
AFTER = -1
LEFT = 1
RIGHT = -1

line_width = len("C:/Users/Florian>aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\
aaaaaaaaaaaaaaaaaaa")
user_names = ['Robert', 'Sartres', 'Oui-Oui', 'Jean-Phillipe', 'Gros Jean', 'Martine', 'La Grosse Bertha']


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
        """Sauvegarde tous les logs crées."""
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
        check_vars_types(
            (tag, 'tag', str),
            (should_print, 'should_print', bool),
            (file_path, 'file_path', str, True),
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
                                  + make_line('~', end='\n\n'))
                    is_final_save_successful = True
                    print("//SAUVEGARDE FINALE '{}'".format(self.name))
                except PermissionError:
                    print("//ÉCHEC SAUVEGARDE. NOUVEL ESSAI...")


def check_vars_types(*var_tuples, internal_check=False):
    """
    Vérifie le type des variables passées en paramètres.

    Les variables doivent être présentées sous la forme de tuples (var, var_name, var_type, none_ok: optionnel)
    var : la variable
    var_name : son nom
    var_type : le type à vérifier
    none_ok : spécifie si les variables nulles sont acceptées

    :param var_tuples: les différentes variables à vérifier
    :param internal_check: spécifie si la fonction est appelé de manière interne à elle-même, ne pas utiliser en dehors
    """
    leng = len(var_tuples)
    # Test si les variables ont été passés sous forme de tuples
    if isinstance(var_tuples[0], tuple):
        # les tuples sont rangés dans une liste
        var_tuples = list(var_tuples)
    # Test si une seule variables a été passée sous la forme de plusieurs arguments
    elif leng == 3 or leng == 4:
        # Ces arguments sont rassemblés en un tuple et mis dans la liste var_tuples
        var_tuples = [tuple(var_tuples)]
    else:
        raise ValueError("")  # TODO : faire un message plus cool

    for index, var_tuple in enumerate(var_tuples):
        # Ajoute Faux par défault s'il n'y a pas les quatres paramètres
        if len(var_tuple) == 3:
            var_tuple = var_tuple + (False,)
            var_tuples[index] = var_tuple
        elif len(var_tuple) > 4:
            print(var_tuple)
            raise ValueError("check_vars_types n'accepte pas plus de 4 arguments par variable")
        elif len(var_tuple) < 3:
            raise ValueError("check_vars_types n'accepte pas moins de trois arguments par variable.")

    for var, var_name, var_type, none_ok in var_tuples:
        if not internal_check:
            check_vars_types(
                (var_name, 'var_name', str),
                (var_type, 'var_type', type),
                (none_ok, 'none_ok', bool),
                internal_check=True
            )
        if var is None and not none_ok or not isinstance(var, var_type) and var is not None:
            print(var)
            print(none_ok)
            print(var is None and not none_ok)
            print(not isinstance(var, var_type))
            raise TypeError("'{}' devrait être de type {} mais est de type {}.".format(var_name, var_type, type(var)))


# TODO : check_vars_values


def is_slash(char: str):
    """Retourne Vrai si char est un slash."""
    char = str(char)
    if len(char) == 1:
        return char == '/' or char == '\\'
    else:
        raise ValueError("char should be a single character.")


def take_part(string: str, side: int, sep_chars: str, start_from: int, no_mods_chars: str = "", take_sep_char=False):
    """
    Retourne une partie d'une chaîne de caractères à partir du premier séparateur trouvé. Si aucun n'est trouvé, cette
    chaîne de caractères est renvoyée tel quel.
    :param string: la chaîne de caractères à couper
    :param side: le côté à garder à partir du séparateur trouvé
    :param sep_chars: les caractères qui sont des séparateurs
    :param start_from: le côté du quel partir
    :param no_mods_chars: si un de ces caractères est trouvé en premier, string n'est pas modifié
    :param take_sep_char: si la partie de string renvoyée doit inclure le séparateur trouvé
    :return: string ou une partie de string
    """
    check_vars_types(
        (string, 'path', str),
        (side, 'side', int),
        (sep_chars, 'sep_chars', str),
        (start_from, 'start_from', int),
        (no_mods_chars, 'no_mods_chars', str)
    )
    # TODO : ajouter une vérification des valeurs de side et start_from
    for v in sep_chars:
        if v in no_mods_chars:
            raise ValueError("Un caractère se trouve à la fois dans sep_chars et no_mods_chars.")
    for i, v in enumerate(string[::start_from]):
        if v in sep_chars:
            if side == AFTER and start_from == RIGHT:
                return string[-i - take_sep_char:]
            elif side == BEFORE and start_from == RIGHT:
                return string[: - i - 1 + take_sep_char]
            elif side == AFTER and start_from == LEFT:
                return string[i + 1 - take_sep_char:]
            elif side == BEFORE and start_from == LEFT:
                return string[: i + take_sep_char]
        if v in no_mods_chars:
            break

    return string


def get_python():
    from sys import executable
    return take_part(executable, BEFORE, '.', start_from=RIGHT, no_mods_chars='/\\')


def get_folder_path(frame_obj):
    """ le chemin du dossier dans lequel se trouve un fichier."""
    check_vars_types(frame_obj, 'frame_obj', type(currentframe()))

    full_path = getfile(frame_obj)
    folder_path = take_part(full_path, BEFORE, "/\\", start_from=RIGHT)
    return folder_path


def get_modules_path():
    """Retourne le chemin absolu du dossier modules."""
    # Récupère le chemin du dossier contenant handyfunctions.py
    folder_path = get_folder_path(currentframe())

    # Récupère le nom de ce dossier
    folder_name = take_part(folder_path, AFTER, '/\\', start_from=RIGHT)

    # Vérifie que le nom de ce dossier est bien module
    if folder_name != 'modules' or folder_name is None:
        raise Exception("Le dossier dans lequel se trouve handyfunctions.py n'est pas modules.")

    return folder_path


def check_path(path):
    """Vérifie que le chemin existe et crée les dossiers nécessaires le cas échéant."""
    check_vars_types(path, 'path', str)

    # Récupère le chemin jusqu'au dernier slash
    path_to_check = take_part(path, BEFORE, '/\\', start_from=RIGHT)

    # Crée les dossiers correspondants s'ils n'existent pas déjà.
    if path_to_check is not None:
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


def command(cmd: str):
    """Retourne une commande écrite comme une phrase sous la forme d'une liste. (ex : sert pour subprocess)"""
    return [i for i in cmd.split(" ") if i != " "]


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


def make_line(char, end='\n'):
    """Retourne une ligne faite à partir de char et de end"""
    char = str(char)
    if len(char) == 1:
        return "".join([char for i in range(line_width)]) + end
    else:
        raise ValueError("char should be a single character.")


def formatted_error(error=traceback.format_exc()):
    """Retourne une erreur encadrée par des lignes de points."""
    # Ajoute un retour à la ligne à la fin de error s'il n'y en a pas déjà un
    if error[-1:] != '\n':
        error += '\n'
    return ('\n'
            + make_line('.')
            + error
            + make_line('.', end=""))


def check_python_version():
    """Vérifie que la version de python utilisée est bien la 3."""
    from sys import version_info

    if version_info[0] < 3:
        raise Exception("Python 3 ou une version plus récente est requise.")


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
    from modules.quickTk import disappear, center
    root = MyTkApp(theme=Themes.dark)
    disappear(root)
    configure_columns_rows(root, 1, 1)
    _create_main_frame(root)
    center(root)
    root.mainloop()


if __name__ == '__main__':
    ExampleLog = Log('ExampleLog')
    main()
    Log.final_save_all()

