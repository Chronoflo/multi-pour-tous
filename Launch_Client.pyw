#!usr/bin/python3.6
# -*- coding: <utf-8> -*-
"""Ce fichier sert à lancer Client en mode fenêtré uniquement, et permet d'en générer du python compilé."""

from modules import Client
from modules.handyfunctions import check_python_version


check_python_version()
if __name__ == '__main__':
    Client.main()
else:
    print("Launch_Client ne devrait pas être appelés depuis un autre module.")
gezgez