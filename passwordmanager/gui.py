from tkinter import *


def gui(manager):
    root = Tk()
    root.title("Passwortmanager")

    entry_list = Listbox(selectmode=BROWSE)
    entry_list.grid(row=0, column=0, columnspan=2)

    label_name = Label(text="Name:")
    label_name.grid(row=1, column=0, sticky=W)
    text_name = Entry()
    text_name.grid(row=1, column=1, sticky=W + E)

    label_user = Label(text="Benutzername:")
    label_user.grid(row=2, column=0, sticky=W)
    text_user = Entry()
    text_user.grid(row=2, column=1, sticky=W + E)

    label_password = Label(text="Passwort:")
    label_password.grid(row=3, column=0, sticky=W)
    text_password = Entry()
    text_password.grid(row=3, column=1, sticky=W + E)

    label_notes = Label(text="Notizen:")
    label_notes.grid(row=5, column=0, sticky=W)
    text_notes = Text()
    text_notes.grid(row=5, column=1)

    label_attributes = Label(text="Attribute:")
    label_attributes.grid(row=4, column=0, sticky=W)
    text_attributes = Text()
    text_attributes.grid(row=4, column=1)

    entry_list.bind("<<ListboxSelect>>", lambda evt: print(
        evt.widget.get(evt.widget.curselection()[0])
        if evt.widget.curselection()
        else "Keine Auswahl"))

    # entry_list.delete(0,END)
    for entry in manager.get_entries():
        entry_list.insert(END, entry.name)

    root.mainloop()
