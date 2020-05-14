try:
    from passwordmanager.gui import Gui

    gui = Gui()
    gui.mainloop()
except ModuleNotFoundError as e:
    from tkinter import messagebox

    messagebox.showerror("Modul fehlt", f"Das Modul {e.name} fehlt, bitte mit 'pip install {e.name}' installieren")
