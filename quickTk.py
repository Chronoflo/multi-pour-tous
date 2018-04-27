# -*- coding: <utf-8> -*-
"""Ce module permet de réaliser rapidement et simplement certaines opérations avec tkinter."""
import tkinter as tk
from tkinter import messagebox


def dialog(msg_box):
    tmp_root = tk.Tk()
    tmp_root.geometry('0x0')
    make_invisible(tmp_root)
    msg_box()
    tmp_root.destroy()


def warning(title, msg):
    dialog(lambda t=title, m=msg: messagebox.showwarning(t, m))


def info(title, msg):
    dialog(lambda t=title, m=msg: messagebox.showinfo(t, m))


def make_invisible(win: tk.Tk):
    """Rend une fenêtre Tk invisible.
    :param win: Une fenêtre Tk.
    TODO: Il faudrait peut-être améliorer l'expression pour qu'elle marche dans tous les cas"""
    win.geometry("0x0+{}+{}".format(win.winfo_screenwidth() * 2, win.winfo_screenheight() * 2))


def center(win):
    """
    Centre une fenêtre Tk.
    :param win: the root or Toplevel window to center
    """
    win.update_idletasks()
    width = win.winfo_width()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width
    height = win.winfo_height()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = win.winfo_screenheight() // 2 - win_height // 2
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    win.deiconify()


if __name__ == '__main__':
    warning("lol", "lol")
    info("meh", "meh")
