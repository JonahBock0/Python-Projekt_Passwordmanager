from tkinter import *
from tkinter import messagebox, filedialog

from cryptography.exceptions import InvalidSignature
from cryptography.fernet import InvalidToken

from .manager import open_manager_from_file, save_manager_to_file, Manager


class Gui:
    passwordsymbol = "•"

    def __init__(self):
        self._manager = None
        self._password = None
        self._filename = None
        self.entry_selected = None
        self.root = Tk()
        self.setup_root()
        self.add_menu()
        self.show_password = BooleanVar()
        self.entry_list = None
        self.add_elements()

    def setup_root(self):
        self.root.title("Passwortmanager")
        self.root.minsize(400, 100)
        self.root.protocol("WM_DELETE_WINDOW", self.close)

    def add_menu(self):
        menu = Menu(self.root)
        self.root.config(menu=menu)
        menu_db = Menu(menu)
        menu.add_cascade(label="Datenbank", menu=menu_db)
        menu_db.add_command(label="Neu", command=self.new)
        menu_db.add_command(label="Speichern", command=self.save)
        menu_db.add_command(label="Speichern unter...", command=self.save_as)
        menu_db.add_command(label="Öffnen", command=self.open)
        menu_db.add_separator()
        menu_db.add_command(label="Speichern und Beenden", command=self.close)

    def add_elements(self):
        self.entry_list = Listbox(selectmode=BROWSE)
        entry_list = self.entry_list
        entry_list.grid(row=0, rowspan=5, sticky=N + S + W + E)
        entry_list.bind("<<ListboxSelect>>", self.selection_changed)

        entry_scrollbar = Scrollbar(orient=VERTICAL)
        entry_list.config(yscrollcommand=entry_scrollbar.set)
        entry_scrollbar.config(command=entry_list.yview)
        entry_scrollbar.grid(row=0, column=1, rowspan=5, sticky=N + S + W)

        label_name = Label(text="Name:")
        label_name.grid(row=0, column=2, sticky=W)
        text_name = Entry()
        text_name.grid(row=0, column=3, sticky=W + E)
        Grid.rowconfigure(self.root, 0, pad=3)

        label_user = Label(text="Benutzername:")
        label_user.grid(row=1, column=2, sticky=W)
        text_user = Entry()
        text_user.grid(row=1, column=3, sticky=W + E)
        Grid.rowconfigure(self.root, 1, pad=3)

        label_password = Label(text="Passwort:")
        label_password.grid(row=2, column=2, sticky=W)
        text_password = Entry(show=Gui.passwordsymbol)
        text_password.grid(row=2, column=3, sticky=W + E)
        Grid.rowconfigure(self.root, 2, pad=3)

        checkbox_showpassword = Checkbutton(text="Passwort zeigen", variable=self.show_password,
                                            command=lambda: text_password.config(
                                                show='' if self.show_password.get() else Gui.passwordsymbol))
        checkbox_showpassword.grid(row=3, column=3, sticky=W)
        Grid.rowconfigure(self.root, 3, pad=3)

        label_notes = Label(text="Notizen:")
        label_notes.grid(row=4, column=2, sticky=N + W)
        text_notes = Text(cnf={"height": 3})
        text_notes.grid(row=4, column=3, sticky=N + S + W + E, pady=3)
        Grid.rowconfigure(self.root, 4, pad=3)

        label_attributes = Label(text="Attribute:")
        label_attributes.grid(row=5, column=2, sticky=N + W)
        text_attributes = Text(cnf={"height": 3})
        text_attributes.grid(row=5, column=3, sticky=N + S + W + E, pady=3)
        Grid.rowconfigure(self.root, 5, pad=3)

        row_weights = [0, 0, 0, 0, 1, 1]
        for row, weight in enumerate(row_weights):
            Grid.rowconfigure(self.root, row, weight=weight)
        col_weights = [1, 0, 0, 2]
        for col, weight in enumerate(col_weights):
            Grid.columnconfigure(self.root, col, weight=weight)
        mincolsizes = {0: 100, 2: 100}
        for col, minsize in mincolsizes.items():
            Grid.columnconfigure(self.root, col, minsize=minsize)

        self.update_list()
        # for i in range(100):
        #     self.entry_list.insert(END, "Eintrag " + str(i))

    def mainloop(self):
        self.root.mainloop()

    def update_list(self):
        if not self._manager:
            return
        self.entry_list.delete(0, END)
        for entry in self._manager.get_entries():
            self.entry_list.insert(END, entry.name)

    def selection_changed(self, evt):
        if not self._manager:
            return
        index = evt.widget.curselection()[0] if evt.widget.curselection() else -1
        if index >= 0:
            self.entry_selected = self._manager.get_entries()[index]

    def close(self):
        if self._manager:
            answer = messagebox.askyesnocancel("Beenden", "Datenbank speichern?")
            if answer is None:
                return
            elif answer:
                self.save()
        self.root.destroy()

    def save(self, password=None):
        if self._manager:
            if self._filename:
                if self._password:
                    save_manager_to_file(self._manager, filename=self._filename, password=self._password)
                elif password:
                    save_manager_to_file(self._manager, filename=self._filename, password=password)
                else:
                    self.password_input(self.save)
            else:
                self.save_as()

    def save_as(self):
        filename = filedialog.asksaveasfilename()
        if filename:
            self._filename = filename
            if self._password and messagebox.askyesno("Neues Passwort?", "Neues Passwort festlegen?"):
                self._password = None
            self.save()

    def open(self, password=None):
        if password and self._filename:
            try:
                self._manager = open_manager_from_file(self._filename, password=password)
                self.update_list()
            except FileNotFoundError:
                messagebox.showerror("Fehler!", "Datei nicht gefunden!")
            except (InvalidSignature, InvalidToken):
                messagebox.showerror("Fehler!",
                                     "Fehler beim Entschlüsseln! Falsches Passwort (oder falsche Salt-Datei)")
            except Exception as e:
                messagebox.showerror("Fehler!", str(e))
        else:
            filename = filedialog.askopenfilename()
            if filename:
                self._filename = filename
                self.password_input(self.open)

    def password_input(self, callback, create=False):
        dialog = Toplevel(self.root)
        dialog.minsize(200, 150)
        title = "Passwort" + (" erstellen:" if create else ":")
        dialog.title(title)
        label = Label(dialog, text=title)
        label.pack()
        pw_entry = Entry(dialog, show=Gui.passwordsymbol)
        pw_entry2 = Entry(dialog, show=Gui.passwordsymbol) if create else None
        pw_entry.pack()
        if pw_entry2:
            pw_entry2.pack()
        button = Button(dialog, text="Ok", command=lambda: [callback(
            password=pw_entry.get() if not pw_entry2
            else pw_entry2.get() if pw_entry.get() == pw_entry2.get() else None), dialog.destroy()])
        button.pack()

    def new(self):
        self._manager = Manager()
        self.update_list()
