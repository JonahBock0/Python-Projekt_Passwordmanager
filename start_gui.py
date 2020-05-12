try:
    from passwordmanager.gui import Gui

    gui = Gui()
    gui.mainloop()
except ModuleNotFoundError:
    from tkinter import messagebox

    messagebox.showerror("Modul fehlt", "Das Modul 'cryptography' ist erforderlich, aber nicht installiert")
