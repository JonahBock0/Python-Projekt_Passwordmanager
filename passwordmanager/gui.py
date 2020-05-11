from tkinter import *
from tkinter import messagebox, filedialog, simpledialog

from cryptography.exceptions import InvalidSignature
from cryptography.fernet import InvalidToken

from .entry import Entry as PEntry
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
        self.var_name = StringVar()
        self.var_user = StringVar()
        self.var_password = StringVar()
        self.text_notes = None
        self.var_attributes = dict()
        self.list_attributes = None
        self.var_attr_key = StringVar()
        self.var_attr_val = StringVar()
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
        entry_list.grid(row=0, rowspan=6, sticky=N + S + W + E)
        entry_list.bind("<<ListboxSelect>>", self.selection_changed)

        entry_scrollbar = Scrollbar(orient=VERTICAL)
        entry_list.config(yscrollcommand=entry_scrollbar.set)
        entry_scrollbar.config(command=entry_list.yview)
        entry_scrollbar.grid(row=0, column=1, rowspan=6, sticky=N + S + W)

        label_name = Label(text="Name:")
        label_name.grid(row=0, column=2, sticky=W)
        text_name = Entry(textvariable=self.var_name)
        text_name.grid(row=0, column=3, sticky=W + E)
        Grid.rowconfigure(self.root, 0, pad=3)

        label_user = Label(text="Benutzername:")
        label_user.grid(row=1, column=2, sticky=W)
        text_user = Entry(textvariable=self.var_user)
        text_user.grid(row=1, column=3, sticky=W + E)
        Grid.rowconfigure(self.root, 1, pad=3)

        label_password = Label(text="Passwort:")
        label_password.grid(row=2, column=2, sticky=W)
        text_password = Entry(show=Gui.passwordsymbol, textvariable=self.var_password)
        text_password.grid(row=2, column=3, sticky=W + E)
        Grid.rowconfigure(self.root, 2, pad=3)

        checkbox_showpassword = Checkbutton(text="Passwort zeigen", variable=self.show_password,
                                            command=lambda: text_password.config(
                                                show='' if self.show_password.get() else Gui.passwordsymbol))
        checkbox_showpassword.grid(row=3, column=3, sticky=W)
        Grid.rowconfigure(self.root, 3, pad=3)

        label_notes = Label(text="Notizen:")
        label_notes.grid(row=4, column=2, sticky=N + W)
        self.text_notes = Text(cnf={"height": 3})
        self.text_notes.grid(row=4, column=3, sticky=N + S + W + E, pady=3)
        Grid.rowconfigure(self.root, 4, pad=3, minsize=30, weight=1)

        label_attributes = Label(text="Attribute:")
        label_attributes.grid(row=5, column=2, sticky=N + W)
        frame_attributes = Frame(self.root)
        self.list_attributes = Listbox(frame_attributes, selectmode=BROWSE)
        self.list_attributes.bind("<<ListboxSelect>>", self.attributes_selection_changed)
        self.list_attributes.grid(row=0, column=0, columnspan=2, sticky=N + S + W + E)
        text_attr_key = Entry(frame_attributes, textvariable=self.var_attr_key)
        text_attr_key.grid(row=1, column=0, sticky=W + E)
        text_attr_val = Entry(frame_attributes, textvariable=self.var_attr_val)
        text_attr_val.grid(row=1, column=1, sticky=W + E)
        button_attr_add = Button(frame_attributes, text="Hinzufügen/Aktualisieren", command=self.attribute_apply)
        button_attr_add.grid(row=2, column=0, sticky=E)
        button_attr_add = Button(frame_attributes, text="Entfernen", command=self.attribute_remove)
        button_attr_add.grid(row=2, column=1, sticky=W)
        frame_attributes.grid_columnconfigure(0, weight=2)
        frame_attributes.grid_columnconfigure(1, weight=3)
        frame_attributes.grid_rowconfigure(0, weight=1)
        frame_attributes.grid(row=5, column=3, sticky=N + S + W + E, pady=3)
        Grid.rowconfigure(self.root, 5, pad=3, weight=1)

        button_add_entry = Button(text="Eintrag hinzufügen", command=self.new_entry)
        button_add_entry.grid(row=6, column=0)
        button_add_entry = Button(text="Eintrag löschen", command=self.delete_entry)
        button_add_entry.grid(row=6, column=1, columnspan=2)
        Grid.rowconfigure(self.root, 6, pad=3)

        col_weights = [1, 0, 0, 2]
        for col, weight in enumerate(col_weights):
            Grid.columnconfigure(self.root, col, weight=weight)
        mincolsizes = {0: 100, 2: 100}
        for col, minsize in mincolsizes.items():
            Grid.columnconfigure(self.root, col, minsize=minsize)

        self.update_list()

    def mainloop(self):
        self.root.mainloop()

    def update_list(self):
        if not self._manager:
            return
        if self.entry_selected:
            self.update_entry()
        self.entry_list.delete(0, END)
        for entry in self._manager.get_entries():
            self.entry_list.insert(END, entry.name)

    def selection_changed(self, evt):
        if not self._manager:
            return
        if self.entry_selected:
            self.update_entry()
        index = evt.widget.curselection()[0] if evt.widget.curselection() else -1
        if index >= 0:
            self.entry_selected = self._manager.get_entries()[index]
            self.update_elements()

    def update_elements(self):
        if not self.entry_selected:
            return
        e = self.entry_selected
        self.var_name.set(e.name)
        self.var_user.set(e.user)
        self.var_password.set(e.password)
        self.var_attributes = e.attributes
        self.update_attribute_list()
        self.text_notes.delete("1.0", END)
        self.text_notes.insert(END, e.notes)

    def update_entry(self):
        if not self.entry_selected:
            return
        e = self.entry_selected
        name = self.var_name.get()
        name_changed = e.name != name
        e.name = name
        e.user = self.var_user.get()
        e.password = self.var_password.get()
        e.attributes = self.var_attributes
        e.notes = self.text_notes.get("1.0", "end-1c")  # Text aus Textfeld auslesen, zusätzliche Newline entfernen
        if name_changed:  # Liste aktualisieren, wenn sich der Name geändert hat
            self.update_list()

    def new_entry(self):
        if not self._manager:
            return
        entry = PEntry(name="Neuer Eintrag")
        self._manager.add_entry(entry)
        self.update_list()
        self.entry_list.select_set(END, END)
        self.entry_selected = entry
        self.update_elements()

    def delete_entry(self):
        if self._manager and self.entry_selected:
            if messagebox.askyesno("Löschen?", f"Wirklich '{self.entry_selected.name}' löschen?"):
                self._manager.remove_entry(self.entry_selected)
                self.update_list()

    def update_attribute_list(self):
        self.list_attributes.delete(0, END)
        for key, val in self.var_attributes.items():
            self.list_attributes.insert(END, f"{key}: \t{val}")

    def attribute_apply(self):
        if self.var_attr_val.get():
            self.var_attributes[self.var_attr_key.get()] = self.var_attr_val.get()
            self.update_attribute_list()

    def attribute_remove(self):
        if self.var_attr_val.get():
            del self.var_attributes[self.var_attr_key.get()]
            self.update_attribute_list()

    def attributes_selection_changed(self, evt):
        if not self._manager or not self.entry_selected:
            return
        index = evt.widget.curselection()[0] if evt.widget.curselection() else -1
        if index >= 0:
            selected_attribute = list(self.entry_selected.attributes.items())[index]
            self.var_attr_key.set(selected_attribute[0])
            self.var_attr_val.set(selected_attribute[1])

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
                if self.entry_selected:
                    self.update_entry()
                if self._password:
                    save_manager_to_file(self._manager, filename=self._filename, password=self._password)
                elif password:
                    save_manager_to_file(self._manager, filename=self._filename, password=password)
                else:
                    password = self.password_input(create=True)
                    if password:
                        self.save(password=password)
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
                self._password = password
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
                self.open(self.password_input())

    def password_input(self, create=False):
        prompt = "Passwort" + (" erstellen:" if create else ":")
        pw = simpledialog.askstring("Passwort", prompt, show=Gui.passwordsymbol)
        if pw:
            if create:
                pw2 = simpledialog.askstring("Passwort", "Passwort wiederholen:", show=Gui.passwordsymbol)
                if pw2 and pw == pw2:
                    self._password = pw
                    return pw
            else:
                self._password = pw
                return pw
        else:
            return None

    def new(self):
        self._manager = Manager()
        self.update_list()
