# -*- coding: <utf-8> -*-
"""Ce module contient des fonctions permettant de facilement gérer les dépendances. L'exécuter lance les processus de
vérification et d'installation."""

import sys
import subprocess
from modules.handyfunctions import cmd, check_vars_types
from modules.quickTk import warning, info, error

check_title = "Dépendances-Vérification "
check_success_msg = "Parfait !\nToutes les dépendances sont satisfaites.\nVous pouvez maintenant profitez de ce \
magnifique programme."
check_error_msg = "lol"
install_title = "Dépendances-Installation"
install_start_msg = "Les dépendances manquantes vont maintenant être installés. Attention, cela peut prendre un long \
 moment (jusqu'à dix minutes). Une autre boîte de dialogue vous avertira de la fin."
install_error_msg = "Diantre :(\nUne erreur est survenue lors de l'installation. L'application va maintenant quitter."
install_end_msg = "Processus d'installation terminée. Normalement, tout devrait être bon !"


def pip_install(package_name: str):
    """Installe un paquet à l'aide de pip."""
    check_vars_types(package_name, 'package_name', str)
    subprocess.check_call(cmd("{python} -m pip install {package}".format(
        python=sys.executable,
        package=package_name
    )))


def install_requirements():
    """
    Installe toutes les dépendances requises en fonction de l'OS de l'utilisateur.
    """
    reqs_not_satisfied = get_not_satisfied_reqs()
    print(reqs_not_satisfied)
    if reqs_not_satisfied:
        check_msg = "Certaines dépendances ne sont pas satisfaites :\n" + "\n".join(
            [' • ' + i for i in reqs_not_satisfied])
        warning(check_title, check_msg)
        print(check_msg)
        warning(install_title, install_start_msg)
        print("Installation des paquets manquants, veuillez patienter...")

        try:
            subprocess.check_call(cmd("{python} -m pip install -r {packages}".format(
                python=sys.executable,
                packages=" ".join(reqs_not_satisfied)
            )))
        except subprocess.CalledProcessError:
            print("Une erreur est survenue lors de l'installation. :(")
            error(install_title, install_error_msg)
            sys.exit(2)
        else:
            print("Terminé.")
            info(install_title, install_end_msg)
        finally:
            print("Vérification...")
            if get_not_satisfied_reqs():
                error(check_title, check_error_msg)
            else:
                info(check_title, check_success_msg)
    else:
        info(check_title, check_success_msg)


def get_not_satisfied_reqs():
    """Retourne une liste des dépendances non satisfaites."""
    # Récupère les paquets nécessaires en fonction du système
    with open('../setup/{reqs}.txt'.format(reqs=sys.platform + '_requirements'), 'r') as f:
        reqs = reqs_to_list(f.read())

    # Récupère les paquets déjà installés grâce à pip
    satisfied_reqs = subprocess.check_output(cmd("{python} -m pip freeze".format(python=sys.executable))).decode()
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
    for i, req in enumerate(reqs):
        if req in "\n " or len(req) == 0:
            del reqs[i]
        else:
            for j, letter in enumerate(req):
                if letter == '=':
                    reqs[i] = req[:j]
                    break
    # Met tout en minuscule
    reqs = [i.lower() for i in reqs]
    return reqs


if __name__ == '__main__':
    install_requirements()
