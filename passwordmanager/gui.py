from tkinter import *
from tkinter import messagebox

passwordsymbol = "•"


def gui():
    manager = None
    root = Tk()
    root.title("Passwortmanager")
    root.minsize(400, 100)
    root.protocol("WM_DELETE_WINDOW", lambda: close(root))
    menu = Menu(root)
    root.config(menu=menu)
    menu_db = Menu(menu)
    menu.add_cascade(label="Datenbank", menu=menu_db)
    menu_db.add_command(label="Neu", command=new)
    menu_db.add_command(label="Speichern", command=save)
    menu_db.add_command(label="Laden", command=load)
    menu_db.add_separator()
    menu_db.add_command(label="Speichern und Beenden", command=lambda: close(root))

    entry_list = Listbox(selectmode=BROWSE)
    entry_list.grid(row=0, rowspan=5, sticky=N + S + W + E)

    entry_scrollbar = Scrollbar(orient=VERTICAL)
    entry_list.config(yscrollcommand=entry_scrollbar.set)
    entry_scrollbar.config(command=entry_list.yview)
    entry_scrollbar.grid(row=0, column=1, rowspan=5, sticky=N + S + W)

    label_name = Label(text="Name:")
    label_name.grid(row=0, column=2, sticky=W)
    text_name = Entry()
    text_name.grid(row=0, column=3, sticky=W + E)
    Grid.rowconfigure(root, 0, pad=3)

    label_user = Label(text="Benutzername:")
    label_user.grid(row=1, column=2, sticky=W)
    text_user = Entry()
    text_user.grid(row=1, column=3, sticky=W + E)
    Grid.rowconfigure(root, 1, pad=3)

    label_password = Label(text="Passwort:")
    label_password.grid(row=2, column=2, sticky=W)
    text_password = Entry(show=passwordsymbol)
    text_password.grid(row=2, column=3, sticky=W + E)
    Grid.rowconfigure(root, 2, pad=3)

    show_password = BooleanVar()
    checkbox_showpassword = Checkbutton(text="Passwort zeigen", variable=show_password,
                                        command=lambda: text_password.config(
                                            show='' if show_password.get() else passwordsymbol))
    checkbox_showpassword.grid(row=3, column=3, sticky=W)
    Grid.rowconfigure(root, 3, pad=3)

    label_notes = Label(text="Notizen:")
    label_notes.grid(row=4, column=2, sticky=N + W)
    text_notes = Text(cnf={"height": 3})
    text_notes.grid(row=4, column=3, sticky=N + S + W + E, pady=3)
    Grid.rowconfigure(root, 4, pad=3)

    label_attributes = Label(text="Attribute:")
    label_attributes.grid(row=5, column=2, sticky=N + W)
    text_attributes = Text(cnf={"height": 3})
    text_attributes.grid(row=5, column=3, sticky=N + S + W + E, pady=3)
    Grid.rowconfigure(root, 5, pad=3)

    row_weights = [0, 0, 0, 0, 1, 1]
    for row, weight in enumerate(row_weights):
        Grid.rowconfigure(root, row, weight=weight)
    col_weights = [1, 0, 0, 2]
    for col, weight in enumerate(col_weights):
        Grid.columnconfigure(root, col, weight=weight)
    mincolsizes = {0: 100, 2: 100}
    for col, minsize in mincolsizes.items():
        Grid.columnconfigure(root, col, minsize=minsize)

    entry_list.bind("<<ListboxSelect>>", lambda evt: print(
        evt.widget.get(evt.widget.curselection()[0])
        if evt.widget.curselection()
        else "Keine Auswahl"))

    update_list(manager, entry_list)
    # for i in range(100):
    #     entry_list.insert(END, "Eintrag " + str(i))

    root.mainloop()


def update_list(manager, entry_list: Listbox):
    if not manager:
        return
    entry_list.delete(0, END)
    for entry in manager.get_entries():
        entry_list.insert(END, entry.name)


def close(root: Tk):
    answer = messagebox.askyesnocancel("Beenden", "Datenbank speichern?")
    if answer is None:
        return
    elif answer:
        save()
    root.destroy()


def save():
    pass


def load():
    pass


def new():
    pass
