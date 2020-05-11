# Starten über 'python -m passwordmanager'
__package__ = "passwordmanager"

from .gui import Gui

gui = Gui()
gui.mainloop()
