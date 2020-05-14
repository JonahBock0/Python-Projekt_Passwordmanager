from tkinter import *
from tkinter import messagebox, filedialog, simpledialog

from cryptography.exceptions import InvalidSignature
from cryptography.fernet import InvalidToken

from . import crypt
from .entry import Entry as PEntry
from .files import read_file, write_file, check_file
from .generator import generate_password
from .manager import open_manager_from_file, save_manager_to_file, Manager


class Gui:
    passwordsymbol = "•"

    def __init__(self):
        self.list_menu = [("[Neue Datenbank]", self.new),  # Menü für die Liste, wenn keine Datenbank geöffnet ist
                          ("[Datenbank öffnen]", self.open),
                          ("[Beenden]", self.quit),
                          ("", lambda: self.list_entries.selection_clear(END))]
        self._manager = None
        self._password = None
        self._filename = None
        self.entry_selected = None
        self.root = Tk()
        self.show_password = BooleanVar()
        self.list_entries = None
        self.var_name = StringVar()
        self.var_user = StringVar()
        self.var_password = StringVar()
        self.text_notes = None
        self.var_attributes = dict()
        self.list_attributes = None
        self.button_new = None
        self.var_attr_key = StringVar()
        self.var_attr_val = StringVar()
        self.setup_root()
        self.setup_menu()
        self.setup_elements()
        self.update_list()
        crypt.callback_salt_created = lambda x: messagebox.showinfo("Salt-Datei", x)

    def setup_root(self):
        self.root.title("Passwortmanager")
        self.root.minsize(500, 300)
        self.root.geometry("800x500")
        self.root.protocol("WM_DELETE_WINDOW", self.quit)

    def setup_menu(self):
        menu = Menu(self.root)
        self.root.config(menu=menu)
        menu_db = Menu(menu)
        menu.add_cascade(label="Datenbank", menu=menu_db)
        menu_db.add_command(label="Neu", command=self.new)
        menu_db.add_command(label="Öffnen", command=self.open)
        menu_db.add_command(label="Speichern", command=self.save)
        menu_db.add_command(label="Speichern unter...", command=self.save_as)
        menu_db.add_separator()
        menu_db.add_command(label="Datenbank schließen", command=self.close)
        menu_db.add_command(label="Speichern und Beenden", command=lambda: self.quit(save=True))
        menu_saltfile = Menu(menu)
        menu.add_cascade(label="Salt-Datei", menu=menu_saltfile)
        menu_saltfile.add_command(label="Importieren", command=import_saltfile)
        menu_saltfile.add_command(label="Exportieren", command=export_saltfile)

    def setup_elements(self):
        root = self.root
        frame_list = Frame(root)
        entry_list = self.list_entries = Listbox(frame_list, selectmode=BROWSE, exportselection=0)
        entry_list.grid(row=0, column=0, sticky=N + S + W + E)
        entry_list.bind("<<ListboxSelect>>", self.selection_changed)

        entry_scrollbar = Scrollbar(frame_list, orient=VERTICAL, command=entry_list.yview)
        entry_list.config(yscrollcommand=entry_scrollbar.set)
        entry_scrollbar.grid(row=0, column=1, sticky=N + S + W + E)
        frame_list.rowconfigure(0, weight=1)
        frame_list.columnconfigure(0, weight=1)
        frame_list.grid(row=0, column=0, rowspan=6, sticky=N + S + W + E)

        Label(text="Name:").grid(row=0, column=1, sticky=W)
        Entry(textvariable=self.var_name).grid(row=0, column=2, sticky=W + E)
        root.rowconfigure(0, pad=3)

        Label(text="Benutzername:").grid(row=1, column=1, sticky=W)
        Entry(textvariable=self.var_user).grid(row=1, column=2, sticky=W + E)
        root.rowconfigure(1, pad=3)

        Label(text="Passwort:").grid(row=2, column=1, sticky=W)
        text_password = Entry(show=Gui.passwordsymbol, textvariable=self.var_password)
        text_password.grid(row=2, column=2, sticky=W + E)
        root.rowconfigure(2, pad=3)
        frame_password = Frame(root)
        Checkbutton(frame_password, text="Passwort zeigen", variable=self.show_password,
                    command=lambda: text_password.config(show='' if self.show_password.get() else Gui.passwordsymbol)
                    ).grid(row=0, column=0)
        Button(frame_password, text="Passwort kopieren", command=self.copy_password).grid(row=0, column=1)
        Button(frame_password, text="Passwortgenerator", command=self.generate_password).grid(row=0, column=2)
        frame_password.grid(row=3, column=2, sticky=W)
        root.rowconfigure(3, pad=3)

        Label(text="Notizen:").grid(row=4, column=1, sticky=N + W)
        self.text_notes = Text(height=3)
        self.text_notes.grid(row=4, column=2, sticky=N + S + W + E, pady=3)
        root.rowconfigure(4, pad=3, minsize=30, weight=1)

        Label(text="Attribute:").grid(row=5, column=1, sticky=N + W)
        frame_attr = Frame(root)
        self.list_attributes = Listbox(frame_attr, height=3, selectmode=BROWSE, exportselection=0)
        self.list_attributes.bind("<<ListboxSelect>>", self.attributes_selection_changed)
        self.list_attributes.grid(row=0, column=0, columnspan=2, sticky=N + S + W + E)
        Entry(frame_attr, textvariable=self.var_attr_key).grid(row=1, column=0, sticky=W + E)
        Entry(frame_attr, textvariable=self.var_attr_val).grid(row=1, column=1, sticky=W + E)
        Button(frame_attr, text="Hinzufügen/Aktualisieren", command=self.attribute_apply
               ).grid(row=2, column=0, sticky=E)
        Button(frame_attr, text="Entfernen", command=self.attribute_remove).grid(row=2, column=1, sticky=W)
        frame_attr.columnconfigure(0, weight=2)
        frame_attr.columnconfigure(1, weight=3)
        frame_attr.rowconfigure(0, weight=1, minsize=30)
        frame_attr.rowconfigure(1, minsize=30)
        frame_attr.rowconfigure(2, minsize=30)
        frame_attr.grid(row=5, column=2, sticky=N + S + W + E, pady=3)
        root.rowconfigure(5, pad=3, weight=1)

        self.button_new = Button(text="Eintrag hinzufügen", command=self.new_entry)
        self.button_new.grid(row=6, column=0)
        Button(text="Eintrag löschen", command=self.delete_entry).grid(row=6, column=1)
        root.rowconfigure(6, pad=3)

        col_weights = [1, 0, 2]
        for col, weight in enumerate(col_weights):
            root.columnconfigure(col, weight=weight)
        root.columnconfigure(0, minsize=130)

    def mainloop(self):
        self.root.mainloop()

    def update_list(self):
        """Liste mit Einträgen auffüllen, oder mit dem Listenmenü, wenn keine Datenbank geöffnet ist"""
        self.list_entries.delete(0, END)
        if self._manager:
            if self.entry_selected:
                self.update_entry()
            for entry in self._manager.get_entries():
                self.list_entries.insert(END, entry.name)
        else:
            for text, func in self.list_menu:
                self.list_entries.insert(END, text)
        self.update_input_state()

    def update_input_state(self):
        """Elemente aktivieren oder deaktivieren, abhängig davon, ob ein Eintrag ausgewählt ist"""
        state = NORMAL if self._manager and self.entry_selected else DISABLED
        for element in self.root.children.values():
            self.set_state(
                element, state,
                lambda e: e is not self.list_entries and isinstance(e, (Entry, Button, Text, Checkbutton, Listbox)))
        self.set_state(self.button_new, NORMAL if self._manager else DISABLED)

    def set_state(self, element, state, test=lambda e: True):
        """state eines Elementes setzen"""
        if element.children:
            for e in element.children.values():
                self.set_state(e, state, test)
        elif test(element):
            element['state'] = state

    def selection_changed(self, evt):
        index = evt.widget.curselection()[0] if evt.widget.curselection() else -1
        if self._manager:
            if self.entry_selected:
                self.update_entry()
            if index >= 0:
                self.entry_selected = self._manager.get_entries()[index]
                self.update_elements()
            self.update_input_state()
        else:
            func = self.list_menu[index][1] if index >= 0 else None
            if func:
                func()

    def update_elements(self):
        """Eingabeelemente mit Eigenschaften des ausgewählten Eintrags füllen, sonst leeren"""
        e = self.entry_selected
        self.var_name.set(e.name if e else "")
        self.var_user.set(e.user if e else "")
        self.var_password.set(e.password if e else "")
        self.var_attributes = e.attributes if e else dict()
        self.update_attribute_list()
        self.var_attr_val.set("")
        self.var_attr_key.set("")
        text_notes_state = self.text_notes["state"]  # state speichern
        self.text_notes["state"] = NORMAL  # ...zum Bearbeiten auf NORMAL setzen
        self.text_notes.delete("1.0", END)
        if e:
            self.text_notes.insert(END, e.notes)
        self.text_notes["state"] = text_notes_state  # ...und auf den vorherigen Wert setzen

    def update_entry(self):
        """Inhalte der Eingabeelemente in den Eintrag speichern"""
        e = self.entry_selected
        if e:
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
        self.list_entries.select_set(END, END)
        self.entry_selected = entry
        self.update_elements()
        self.update_input_state()

    def delete_entry(self):
        if self._manager and self.entry_selected:
            if messagebox.askyesno("Löschen?", f"'{self.entry_selected.name}' wirklich  löschen?"):
                self._manager.remove_entry(self.entry_selected)
                self.entry_selected = None
                self.update_elements()
                self.update_list()

    def update_attribute_list(self):
        state = self.text_notes["state"]  # state speichern
        self.list_attributes["state"] = NORMAL  # ...zum Bearbeiten auf NORMAL setzen
        self.list_attributes.delete(0, END)
        if self._manager and self.entry_selected:
            for key, val in self.var_attributes.items():
                self.list_attributes.insert(END, f"{key}:  {val}")
        self.list_attributes["state"] = state  # ...und auf den vorherigen Wert setzen

    def attribute_apply(self):
        if self._manager and self.entry_selected:
            key = self.var_attr_key.get()
            val = self.var_attr_val.get()
            if key:
                self.var_attributes[key] = val
                self.update_attribute_list()

    def attribute_remove(self):
        if self._manager and self.entry_selected:
            key = self.var_attr_key.get()
            if key and key in self.var_attributes:
                del self.var_attributes[key]
                self.update_attribute_list()

    def attributes_selection_changed(self, evt):
        if self._manager and self.entry_selected:
            index = evt.widget.curselection()[0] if evt.widget.curselection() else -1
            if index >= 0:
                selected_attribute = list(self.entry_selected.attributes.items())[index]
                self.var_attr_key.set(selected_attribute[0])
                self.var_attr_val.set(selected_attribute[1])

    def close(self):
        if self._manager:
            answer = messagebox.askyesnocancel("Datenbank schließen", "Speichern?")
            if answer is None:
                return
            elif answer:
                self.save()
            self._manager = None
            self.entry_selected = None
            self.update_list()
            self.update_elements()

    def quit(self, save=None):
        if self._manager:
            answer = messagebox.askyesnocancel("Beenden", "Datenbank speichern?") if save is None else save
            if answer is None:
                return
            elif answer:
                self.save()
        self.root.destroy()

    def save(self, password=None):
        if self._manager:
            if self._filename:
                if self.entry_selected:
                    self.update_entry()  # Aktuelle eingegebene Werte vor dem Speichern übertragen
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
            if self._manager and messagebox.askyesno("Öffnen", "Aktuelle Datenbank speichern?"):
                self.save()  # Nach Nachfrage die aktuelle Datenbank vor dem Öffnen speichern
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

    def copy_password(self):
        if self._manager and self.entry_selected:
            self.root.clipboard_clear()
            self.root.clipboard_append(self.var_password.get())

    def generate_password(self):
        if self._manager and self.entry_selected:
            generator = Passwordgenerator(self.root)
            if generator.password:
                self.var_password.set(generator.password)


# noinspection PyAttributeOutsideInit
class Passwordgenerator(simpledialog.Dialog):
    def body(self, master):
        self.title("Passwortmanager")
        self.length = StringVar(value="12")
        self.exclude = StringVar(value="")
        self.punctuation = BooleanVar(value=True)
        self.digits = BooleanVar(value=True)
        self.letters = BooleanVar(value=True)
        self.space = BooleanVar(value=True)
        self.password = None
        self.minsize(200, 150)
        frame = Frame(self)
        Label(frame, text="Länge:").grid(row=0, column=0, sticky=W)
        val = (self.register(lambda newval: newval.isnumeric() or not newval), '%P')
        Entry(frame, textvariable=self.length, validate="all", validatecommand=val).grid(row=0, column=1, sticky=W + E)
        checkbutton_conf = dict(column=0, columnspan=2, sticky=W, padx=10)
        Checkbutton(frame, text="Buchstaben", variable=self.letters).grid(checkbutton_conf, row=1)
        Checkbutton(frame, text="Zahlen", variable=self.digits).grid(checkbutton_conf, row=2)
        Checkbutton(frame, text="Sonderzeichen", variable=self.punctuation).grid(checkbutton_conf, row=3)
        Checkbutton(frame, text="Leerzeichen", variable=self.space).grid(checkbutton_conf, row=4)
        Label(frame, text="Zeichen ausschließen:").grid(row=5, column=0, sticky=W)
        val = (self.register(lambda action, prev, new: int(action) != 1 or new not in prev), '%d', '%s', '%S')
        Entry(frame, textvariable=self.exclude, validate="all", validatecommand=val).grid(row=5, column=1, sticky=W + E)
        frame.columnconfigure(0, weight=1, minsize=120)
        frame.columnconfigure(1, weight=10)
        frame.pack(fill="both", padx=10)

    def validate(self):
        length = int(self.length.get()) if self.length.get() else 0
        if length > 0 and any([self.letters.get(), self.digits.get(), self.punctuation.get(), self.space.get()]):
            password = generate_password(length, exclude=self.exclude.get(),
                                         letters=self.letters.get(), digits=self.digits.get(),
                                         punctuation=self.punctuation.get(), space=self.space.get())
            self.password = password if password else None
            return bool(self.password)
        return False


def export_saltfile():
    if check_file(crypt.default_salt_filename):
        filename = filedialog.asksaveasfilename()
        if filename:
            write_file(filename, read_file(crypt.default_salt_filename))


def import_saltfile():
    filename = filedialog.askopenfilename()
    if filename and check_file(filename):
        new_salt = read_file(filename)
        if check_file(crypt.default_salt_filename):
            old_salt = read_file(crypt.default_salt_filename)
            if new_salt != old_salt:
                write_file(crypt.default_salt_filename + "_old", old_salt)  # Alte Salt-Datei sichern
        write_file(crypt.default_salt_filename, new_salt)
