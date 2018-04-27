# -*- coding: <utf-8> -*-
"""Ce module contient des fonctions permettant de facilement gérer les dépendances."""

from sys import platform
import pip
from quickTk import warning, info

install_title = "Installing dependencies"
install_start_msg = "Les paquets manquants vont maintenant être installés. Attention, cela peut prendre un long moment \
(jusqu'à dix minutes). Une autre boîte de dialogue vous avertira de la fin."
install_end_msg = "Processus d'installation terminée. Normalement, tout devrait être bon !"


def pip_install(package_name: str):
    """Installe un paquet à l'aide de pip."""
    if isinstance(package_name, str):
        import pip
        pip.main(['setup', package_name])
    else:
        raise TypeError("package_name should be a string.")


def install_requirements():
    """
    Installe toutes les dépendances requises en fonction de l'OS de l'utilisateur.
    """
    print("Installing missing modules, please wait..")
    warning(install_title, install_start_msg)

    if platform == 'win32':
        pip.main(['install', '-r', 'setup/win_requirements.txt'])
    elif platform == 'linux':
        pip.main(['install', '-r', 'setup/linux_requirements.txt'])  # TODO : linux_requirements.txt

    print("Finished")
    info(install_title, install_end_msg)
