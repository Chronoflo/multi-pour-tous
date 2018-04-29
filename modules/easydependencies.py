#!/usr/bin/python3
# -*- coding: <utf-8> -*-
"""
Ce module contient des fonctions permettant de facilement gérer les dépendances. L'exécuter lance les processus de
vérification et d'installation.

 • ensure_pip : s'assure que pip est installé
 • pip_install : installe un/des paquets à l'aide de pip
 • pip_uninstall : désinstalle un/des paquets à l'aide de pip
 • pip_check : vérifie que les paquets installés ont des dépendances compatibles
 • pip_command : exécute une commande pip
 • install_requirements : vérifie les dépendances et installent celles qui manquent
 • uninstall_requirements : désinstalle toutes les dépendances
 • get_unsatisfied_reqs : renvoie les dépendances manquantes
 • reqs_to_list : convertit une string, qui suit la convention de pip, en une liste de dépendances
"""
import sys
from os import system
import subprocess
from modules.handyfunctions import to_command, check_vars_types, check_python_version, get_modules_path, get_python, \
    take_part, LEFT, BEFORE


python = get_python()

check_title = "Vérification "
check_success_msg = "Parfait !\nToutes les dépendances sont satisfaites.\nVous pouvez maintenant profitez de ce \
magnifique programme."
check_error_msg = "lol"
install_title = "Installation"
install_start_msg = "Les dépendances manquantes vont maintenant être installées.\n\nAttention, cela peut prendre un long \
 moment (jusqu'à dix minutes). Une autre boîte de dialogue vous avertira de la fin."
install_error_msg = "Diantre :(\nUne erreur est survenue lors de l'installation.\nÊtes-vous sûr que tous les paquets \
listées dans les requirements existent ?\nL'application va maintenant quitter."
install_end_msg = "Processus d'installation terminée. Normalement, tout devrait être bon !"


def ensure_pip():
    """S'assure que pip est installé."""
    try:
        import pip
    except ImportError:
        if sys.platform == 'linux':
            print("Installation", "Pip n'est pas installé et son installation va donc être lancée.")
            system("sudo apt-get --yes --allow-yes=true update && sudo apt-get --yes --force-yes install python3-pip")
        else:
            print("Je sais pas quoi faire :'( ")
        import pip


def ensure_tkinter():
    """S'assure que tkinter est installé."""
    try:
        import tkinter
    except ImportError:
        if sys.platform == 'linux':
            print("Tkinter n'est pas installé et va donc maintenant l'être.")
            system("sudo apt-get --yes --allow-yes=true install python3-tk")
        else:
            print("C'est la hess, JE. SAIS. PAS. QUOI. FAIRE.")
        import tkinter


def ensure_glut():
    """S'assure que glut est installé."""
    if sys.platform == 'linux':
        system("sudo apt-get --yes --allow-yes=true install freeglut3-dev")
    elif sys.platform == 'win32':
        pass  # En théorie glut est installé par défaut sur windows avec pyopengl
    else:
        raise OSError("C'est la galère mec, je sais pas quoi faire sur cet OS")


def pip_install(packages):
    """Installe un/des paquets à l'aide de pip."""
    if isinstance(packages, str):
        packages = packages
    elif isinstance(packages, list):
        for package in packages:
            check_vars_types((package, 'package', str))
        packages = " ".join(packages)

    pip_command("install " + packages + " --retries 1")


def pip_upgrade(packages):
    """Met à jour un/des paquets à l'aide de pip."""
    if isinstance(packages, str):
        packages = packages
    elif isinstance(packages, list):
        for package in packages:
            check_vars_types((package, 'package', str))
        packages = " ".join(packages)
    pip_command("install --upgrade " + packages)


def pip_uninstall(packages):
    """Enlève un/des paquets à l'aide de pip"""
    if isinstance(packages, str):
        packages = packages
    elif isinstance(packages, list):
        for package in packages:
            check_vars_types((package, 'package', str))
        packages = " ".join(packages)

    pip_command("uninstall " + packages)


def pip_check():
    """Vérifie que les paquets installés ont des dépendances compatibles."""
    pip_command("check")


def pip_command(cmd: str):
    """Execute une commande pip."""
    check_vars_types(cmd, 'cmd', str)
    subprocess.check_call(to_command("{python} -m pip {cmd}".format(
        python=python,
        cmd=cmd
    )))


def install_requirements():
    """
    Installe toutes les dépendances requises en fonction de l'OS de l'utilisateur.
    """
    ensure_pip()
    ensure_tkinter()
    ensure_glut()
    from modules.quickTk import warning, info, error
    reqs_not_satisfied = get_unsatisfied_reqs()
    if reqs_not_satisfied:
        check_msg = "Certaines dépendances ne sont pas satisfaites :\n" + "\n".join(
            [' • ' + i for i in reqs_not_satisfied])
        warning(check_title, check_msg)
        print(check_msg)
        info(install_title, install_start_msg)
        print("Installation des paquets manquants, veuillez patienter...")

        try:
            for req in reqs_not_satisfied:
                pip_install(req)
        except subprocess.CalledProcessError:
            print("Une erreur est survenue lors de l'installation. :(")
            error(install_title, install_error_msg)
            sys.exit()
        else:
            print("Terminé.")
            info(install_title, install_end_msg)
            print("Vérification...")
            if not get_unsatisfied_reqs():
                print("O.K.")
                info(check_title, check_success_msg)
            else:
                print("Oh no..")
                error(check_title, check_error_msg)
        finally:
            pip_check()
    else:
        info(check_title, check_success_msg)


def uninstall_requirements():
    """Désinstalle toutes les dépendances"""
    with open('../setup/{reqs}.txt'.format(reqs=sys.platform + '_requirements'), 'r') as f:
        reqs = reqs_to_list(f.read())
    pip_uninstall(reqs)


def get_unsatisfied_reqs():
    """Retourne une liste des dépendances non satisfaites."""
    # Récupère les paquets nécessaires en fonction du système
    with open('{path}/{reqs}.txt'.format(
            path=get_modules_path() + "/../setup",
            reqs=sys.platform + '_requirements'), 'r') as f:
        reqs = reqs_to_list(f.read())

    # Récupère les paquets déjà installés grâce à pip
    satisfied_reqs = subprocess.check_output(to_command("{python} -m pip freeze".format(python=python))).decode()
    satisfied_reqs = reqs_to_list(satisfied_reqs)

    # Compare reqs and satisfied_reqs pour trouver les dépendances non satisfaites
    reqs_not_satisfied = []
    for req in reqs:
        if req not in satisfied_reqs:
            reqs_not_satisfied.append(req)

    return reqs_not_satisfied


def reqs_to_list(reqs: str):
    """Enlève tout ce qui est inutile pour obtenir une liste contenant les noms des modules en minuscules."""
    check_vars_types((reqs, 'reqs', str))
    # Fait une liste en séparant à l'aide de \n, et en enlevant les espaces, les \n, et les éléments vides
    reqs = [i for i in reqs.split("\n") if i not in "\n " and len(i) != 0]

    # Parcourt les différentes dépendances
    for i, req in enumerate(reqs):
        # Ne garde que la partie située avant le égal en partant de la gauche
        reqs[i] = take_part(req, BEFORE, '=', start_from=LEFT)

    # Met tout en minuscule
    reqs = [i.lower() for i in reqs]
    return reqs


check_python_version()
ensure_pip()
ensure_tkinter()
ensure_glut()
if __name__ == '__main__':
    install_requirements()
