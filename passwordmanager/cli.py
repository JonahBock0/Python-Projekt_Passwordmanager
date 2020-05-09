from getpass import getpass

from cryptography.exceptions import InvalidSignature
from cryptography.fernet import InvalidToken

from .crypt import generate_key
from .entry import Entry
from .files import check_file
from .generator import generate_password
from .manager import Manager, save_manager_to_file, open_manager_from_file


def entry_menu(manager: Manager, entry: Entry):
    if not entry:
        return
    while True:
        auswahl = input_int(f'''Ausgewählt: {entry.name}
Wählen Sie eine der folgenden Funktionen:
    1. Eintrag anzeigen
    2. Namen bearbeiten
    3. Benutzernamen bearbeiten
    4. Passwort bearbeiten
    5. Notizen bearbeiten
    6. Attribute bearbeiten
    7. Eintrag löschen
    8. zurück ins Hauptmenü
Ihre Eingabe: ''')

        if auswahl == 8:
            break
        functions = {1: lambda: print_entry(entry),
                     2: lambda: edit_name(entry),
                     3: lambda: edit_user(entry),
                     4: lambda: edit_password(entry),
                     5: lambda: edit_notes(entry),
                     6: lambda: edit_attributes(entry),
                     7: lambda: delete_entry(manager, entry)}
        function = functions.get(auswahl, wrong_input)
        function()


def input_int(text: str, errorval: int = -1):
    try:
        return int(input(text))
    except ValueError:
        return errorval


def input_or_generate_password() -> str:
    selection = 0
    password = ""
    while selection not in [1, 2, 3]:
        selection = input_int('''Auswählen:
    1. Passwort eingeben
    2. Passwort generieren
    3. Abbrechen
Auswählen: ''', 0)
    if selection == 1:
        while not password:
            password = input()
    elif selection == 2:
        length = 0
        while length <= 0:
            length = input_int("Länge: ", 0)
        password = generate_password(length)
    return password


def input_new_value(title: str, old_val: str) -> str:
    return input(title + ((":   (vorher '" + old_val + "')\n") if old_val else ":\n"))


def attributes_to_string(entry: Entry) -> str:
    string = ""
    if entry.attributes:
        max_len = len(max(entry.attributes.keys(), key=lambda x: len(x)))
        for key, val in entry.attributes.items():
            string += key + ":" + " " * (max_len - len(key) + 1) + val + "\n"
    return string


def edit_attributes(entry):
    while True:
        print(attributes_to_string(entry))
        selection = input_int('''
Auswählen:
    1. Attribut bearbeiten/hinzufügen
    2. Attribut entfernen
    3. Zurück
: ''', 0)
        if selection == 3:
            break
        elif selection == 1 or selection == 2:
            name = input("Attributsname: ")
            if name:
                if selection == 1:
                    entry.attributes[name] = input("Wert: ")
                elif selection == 2 and name in entry.attributes.keys():
                    del entry.attributes[name]
                print()


def edit_name(entry):
    entry.name = input_new_value("Name", entry.name)


def edit_user(entry):
    entry.user = input_new_value("Benutzernamen", entry.user)


def edit_password(entry):
    new_password = input_or_generate_password()
    if new_password:
        entry.password = new_password


def edit_notes(entry: Entry):
    if entry.notes:
        print(f"Notiz:\n{entry.notes}")
    auswahl = input_int('''Wählen Sie eine der folgenden Funktionen:
    1. Notiz ergänzen (anhängen)
    2. Notiz ersetzen
    3. Abbrechen
: ''') if entry.notes else 2
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
    if input(f"Eintrag '{entry.name}' löschen? ('ja' eingeben): ").lower() == "ja":
        manager.remove_entry(entry)


def add_entry(manager):
    print('Eintrag hinzufügen:\n')
    name = ""
    while not name:
        name = input("Name: ")
    user = input("Benutzername: ")
    password = input_or_generate_password()
    entry = Entry(name=name, user=user, password=password)
    manager.add_entry(entry)
    return entry


def select_entry_from_list(entries):
    if not entries:
        print("Keine Einträge zur Auswahl vorhanden")
        return None
    for i, entry in enumerate(entries):
        print(f"{i + 1}: {entry.name}")
    selection = -1
    while selection not in range(len(entries) + 1):
        selection = input_int("Auswahl (0 zum Abbrechen): ", -1)
    return entries[selection - 1] if selection > 0 else None


def print_entry(entry):
    print("Name: " + entry.name, "Username: " + entry.user, "Passwort: " + entry.password, "Notiz:", entry.notes, "",
          attributes_to_string(entry), sep="\n")
    input()


def wrong_input():
    print("Die eingegebene Zahl ist nicht im Menü")


def menu(manager):
    if not manager:
        return
    while True:
        auswahl = input_int('''
Hauptmenü:
Wählen Sie eine der folgenden Funktionen:
    1. Eintrag hinzufügen
    2. Alle Einträge auflisten
    3. Eintrag suchen
    4. Speichern
    5. Programm verlassen (speichern)
Ihre Eingabe: ''')
        print()
        if auswahl == 5:
            break
        elif auswahl == 4:
            return "save"
        functions = {1: lambda: add_entry(manager),
                     2: lambda: select_entry_from_list(manager.get_entries()),
                     3: lambda: select_entry_from_list(manager.find_entries(input("Suche: ")))}
        function = functions.get(auswahl, wrong_input)
        entry_menu(manager, function())


def cli():
    auswahl = 0
    while auswahl not in [1, 2, 3]:
        auswahl = input_int('''
Wählen Sie aus Folgendem:
    1. Neue Datenbank erstellen
    2. Datenbank öffnen
    3. Beenden
Ihre Eingabe: ''')
        print()
    if auswahl == 3:
        return
    manager = None
    key = None
    filename = input("Dateiname/Pfad: ")
    file_exists = None
    if filename:
        file_exists = check_file(filename)
    else:
        auswahl = 0
    try:
        if auswahl == 1:
            if not file_exists or (file_exists and input(
                    f"Datei existiert bereits, überschreiben? ('ja' eingeben): ").lower() == "ja"):
                password = getpass("Passwort eingeben: ")
                if password:
                    if getpass("Passwort wiederholen: ") == password:
                        key = generate_key(password)
                        manager = Manager()
                        save_manager_to_file(manager, filename, key=key)
                    else:
                        print("Passwörter stimmen nicht überein!")
        elif auswahl == 2:
            if file_exists:
                key = generate_key(getpass("Passwort: "))
                manager = open_manager_from_file(filename, key=key)
            else:
                raise FileNotFoundError
    except FileNotFoundError:
        print("Datei nicht gefunden!")
    except (InvalidSignature, InvalidToken):
        print("Fehler beim Entschlüsseln! Falsches Passwort (oder falsche Salt-Datei)")
    if manager:
        while menu(manager) == "save":
            save_manager_to_file(manager, filename, key=key)
        save_manager_to_file(manager, filename, key=key)
    elif auswahl != 3:
        cli()
