from sys import platform

def tkinter():
    try:
        import tkinter
        return tkinter
    except ImportError:
        if platform == 'linux':
            import os
            os.system("sudo apt-get install python3-tk")
        else:
            print("Je sais pas quoi faire :'( ")