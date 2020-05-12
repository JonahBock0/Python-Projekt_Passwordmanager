# Starten über 'python -m passwordmanager'
__package__ = "passwordmanager"

try:
    from .gui import Gui

    gui = Gui()
    gui.mainloop()
except ModuleNotFoundError as e:
    from tkinter import messagebox

    messagebox.showerror("Modul fehlt",
                         "Das Modul 'cryptography' ist erforderlich, aber nicht installiert\n" + e.what())
