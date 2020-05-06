from getpass import getpass

from passwordmanager.crypt import generate_key
from passwordmanager.entry import Entry
from passwordmanager.manager import Manager, save_manager_to_file, open_manager_from_file


def entry_menu(manager, entry):
    while True:
        auswahl = input_int(f'''Ausgewählt: {entry.name}
Wählen Sie eine der folgenden Funktionen:
    1. Namen bearbeiten
    2. Benutzernamen bearbeiten
    3. Passwort bearbeiten
    4. Notizen bearbeiten
    5. Attribute bearbeiten
    6. Eintrag löschen
    7. zurück ins Hauptmenü
Ihre Eingabe: ''')

        if auswahl == 7:
            break
        funktionen = {1: lambda: edit_name(entry),
                      2: lambda: edit_user(entry),
                      3: lambda: edit_password(entry),
                      4: lambda: edit_notes(entry),
                      5: lambda: edit_attributes(entry),
                      6: lambda: delete_entry(manager, entry)}
        funktion = funktionen.get(auswahl, wrong_input)
        funktion()


def input_int(text: str, errorval: int = -1):
    try:
        return int(input(text))
    except ValueError:
        return errorval


def input_new_value(title: str, old_val: str):
    return input(title + ((":   (vorher '" + old_val + "')\n") if old_val else ":\n"))


def edit_attributes(entry):
    pass


def edit_name(entry):
    entry.name = input_new_value("Name", entry.name)


def edit_user(entry):
    entry.user = input_new_value("Benutzernamen", entry.user)


def edit_password(entry):
    entry.password = input_new_value("Passwort", entry.password)


def edit_notes(entry: Entry):
    if entry.notes:
        print(f"Notiz:\n{entry.notes}")
    auswahl = input_int('''Wählen Sie eine der folgenden Funktionen:
    1. Notiz ergänzen (anhängen)
    2. Notiz ersetzen
    3. Abbrechen''') if entry.notes else 2
    if auswahl == 3:
        return
    if auswahl == 1 or auswahl == 2:
        notes = (entry.notes + "\n") if auswahl == 1 else ""
        print(notes, end="")
        print("Eingeben:")
        while not notes.endswith("\n" * 3):
            notes += input() + "\n"
        entry.notes = notes[:-3]


def delete_entry(manager, entry):
    if input(f"Eintrag '{entry.name}' löschen? ('ja' eingeben)").lower() == "ja":
        manager.remove_entry(entry)


def add_entry(manager):
    print('Eintrag hinzufügen:\n')
    # Neuen Entry erstellen (Werte eingeben)
    entry = Entry()
    entry_menu(manager, entry)


def print_entry(entry):
    print("Name: " + entry.name, "Username: " + entry.user, "Passwort: " + entry.password, "Notiz:", entry.notes, "",
          entry.attributes, sep="\n")
    input()


def wrong_input():
    print("Die eingegebene Zahl ist nicht im Menü")


def menu(manager):
    while True:
        auswahl = input_int('''Willkommen im Passwordmanager
Hauptmenü:
Wählen Sie eine der folgenden Funktionen:
    1. Eintrag hinzufügen
    2. Eintrag anzeigen
    3. Programm verlassen
Ihre Eingabe: ''')
        if auswahl == 3:
            break
        funktionen = {1: add_entry, 2: entry_menu}
        funktion = funktionen.get(auswahl, wrong_input)
        funktion(manager)


def cli():
    auswahl = 0
    while auswahl not in [1, 2, 3]:
        auswahl = input_int('''Wählen Sie aus Folgendem:
    1. Neue Datenbank erstellen
    2. Datenbank öffnen
    3. Beenden
Ihre Eingabe: ''')
    if auswahl == 3:
        return
    filename = input("Dateiname/Pfad: ")
    key = generate_key(getpass("Passwort: "))
    manager = None
    if auswahl == 1:
        manager = Manager()
        save_manager_to_file(manager, filename, key=key)
    elif auswahl == 2:
        manager = open_manager_from_file(filename, key=key)
    menu(manager)
    save_manager_to_file(manager, filename, key=key)
