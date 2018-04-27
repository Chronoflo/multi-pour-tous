# -*- coding: <utf-8> -*-
"""Ce fichier sert à lancer Client en mode fenêtré uniquement, et permet d'en générer du python compilé."""

import Client

if __name__ == '__main__':
    Client.main()
else:
    print("Launch_Client ne devrait pas être appelés depuis un autre module.")
