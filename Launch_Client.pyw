#!/usr/bin/python
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
# noinspection PyBroadException
import Serveur

if __name__ == '__main__':
    Serveur.main()
else:
    print("Launch_Serveur shouldn't be called from another module.")
    print("encore un test")
