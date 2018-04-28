from sys import platform


try:
    import tkinter
except ImportError:
    if platform == 'linux':
        import os
        os.system("sudo apt-get install python3-tk")
    else:
        print("Je sais pas quoi faire :'( ")
    import tkinter
