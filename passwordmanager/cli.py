from passwordmanager.manager import Manager


def Untermenü(manager, entry):
    auswahl = int(input(f'''{entry.name}
Untermenü:
Wählen Sie eine der folgenden Funktionen:
    1. Namen bearbeiten
    2. Benutzer bearbeiten
    3. Passwort bearbeiten
    4. Notizen bearbeiten
    5. Attribute bearbeiten
    6. zurück ins Hauptmenü
Ihre Eingabe: '''))

    if auswahl == 6:
        return
    funktionen = {1: Eintrag_bearbeiten, 2: Eintrag_löschen}
    funktion = funktionen.get(auswahl, fehler)
    funktion(manager)


def edit_user(manager, entry):
    print(entry.name)


def Eintrag_löschen(manager, entry):
    print('Eintrag löschen:\n')
    manager.remove_entry(entry)


def Eintrag_bearbeiten(manager, entry):
    print('Eintrag_bearbeiten\n')


def Eintrag_hinzufügen(manager):
    print('Eintrag hinzufügen:\n')
    Untermenü(manager)
    manager.


def Eintrag_anzeigen(manager):
    print('Eintrag Anzeigen:\n')
    Untermenü(manager)


def fehler(manager):
    print("Die eingegebene Zahl ist nicht im Menü")


def menu(manager):
    while True:
        auswahl = int(input('''Willkommen im Passwordmanager
Hauptmenü:
Wählen Sie eine der folgenden Funktionen:
    1. Eintrag hinzufügen
    2. Eintrag anzeigen
    3. Programm verlassen
Ihre Eingabe: '''))
        if auswahl == 3:
            break
        funktionen = {1: Eintrag_hinzufügen, 2: Eintrag_anzeigen}
        funktion = funktionen.get(auswahl, fehler)
        funktion(manager)


def cli():
    auswahl = int(input('''Wählen Sie aus Folgendem:
    1. Neuen Datenbank erstellen
    2. Datenbank öffnen
Ihre Eingabe: '''))
    if auswahl == 1:
        pass
    if auswahl == 2:
        pass

    manager = Manager()
    menu(manager)


cli()
