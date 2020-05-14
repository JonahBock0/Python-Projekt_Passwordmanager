# Starten über 'python -m passwordmanager'
__package__ = "passwordmanager"

try:
    from sys import argv

    mode = argv[1] if len(argv) > 1 else "gui"
    if mode == "gui":
        from .gui import Gui

        gui = Gui()
        gui.mainloop()
    elif mode == "cli":
        from .cli import cli

        cli()
    else:
        print("'gui' oder 'cli' angeben")
except ModuleNotFoundError as e:
    message = f"Das Modul {e.name} fehlt, bitte mit 'pip install {e.name}' installieren"
    print(message)
    from tkinter import messagebox

    messagebox.showerror("Modul fehlt", message)
