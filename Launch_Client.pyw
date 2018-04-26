#!/usr/bin/python
# -*- coding: <utf-8> -*-
# -------------------------------------------------------------------------------
# Name:        Launch_Client
# Purpose:     lancer le client
#
# Author:      Florian
#
# Created:     30/03/2018
# Copyright:   (c) Florian 2018
# Licence:     <your licence>
# -------------------------------------------------------------------------------
import Client

if __name__ == '__main__':
    Client.main()
else:
    print("Launch_Client ne devrait pas être appelés depuis un autre module.")
