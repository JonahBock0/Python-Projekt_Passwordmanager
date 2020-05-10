from tkinter import *


def gui(manager):
    root = Tk()
    root.title("Passwortmanager")
    root.minsize(400, 100)

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

    label_user = Label(text="Benutzername:")
    label_user.grid(row=1, column=2, sticky=W)
    text_user = Entry()
    text_user.grid(row=1, column=3, sticky=W + E)

    label_password = Label(text="Passwort:")
    label_password.grid(row=2, column=2, sticky=W)
    text_password = Entry()
    text_password.grid(row=2, column=3, sticky=W + E)

    label_notes = Label(text="Notizen:")
    label_notes.grid(row=3, column=2, sticky=W)
    text_notes = Text(cnf={"height": 3})
    text_notes.grid(row=3, column=3, sticky=N + S + W + E)

    label_attributes = Label(text="Attribute:")
    label_attributes.grid(row=4, column=2, sticky=W)
    text_attributes = Text(cnf={"height": 3})
    text_attributes.grid(row=4, column=3, sticky=N + S + W + E)

    for row in range(5):
        if row not in [0, 1, 2]:
            Grid.rowconfigure(root, row, weight=1)
    for col in range(4):
        if col not in [1, 2]:
            Grid.columnconfigure(root, col, weight=1)
    mincolsizes = {0: 100, 1: 20, 2: 100}
    for col, minsize in mincolsizes.items():
        Grid.columnconfigure(root, col, minsize=minsize)

    entry_list.bind("<<ListboxSelect>>", lambda evt: print(
        evt.widget.get(evt.widget.curselection()[0])
        if evt.widget.curselection()
        else "Keine Auswahl"))

    # entry_list.delete(0,END)
    for entry in manager.get_entries():
        entry_list.insert(END, entry.name)
    # for i in range(100):
    #     entry_list.insert(END, "Eintrag " + str(i))

    root.mainloop()
