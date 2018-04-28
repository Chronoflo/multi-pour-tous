#!/usr/bin/python3
# -*- coding: <utf-8> -*-
"""
Contient des classes Tk redéfinies pour les besoins de l'application.
"""

from modules.handyfunctions import Themes, configure_columns_rows
import tkinter as tk


class MyTkApp(tk.Tk):
    """MyTkApp hérite de tkinter.Tk en rajoutant comme propriété un thème."""
    def __init__(self, theme=Themes.default(), log=None, event_log=None, screen_name=None, base_name=None,
                 class_name='MyTkApp', use_tk=1, sync=0, use=None):
        """
        Construit un objet MyTkApp.
        :param theme: permet de spécifier un thème si l'on ne souhaite pas utiliser le thème par défaut
        """
        self.theme = theme
        self.log = log
        self.eventLog = event_log
        super().__init__(screen_name, base_name, class_name, use_tk, sync, use)

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