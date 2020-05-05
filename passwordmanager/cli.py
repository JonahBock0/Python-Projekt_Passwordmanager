from passwordmanager.manager import Manager


def Untermenü(manager):
    auswahl = int(input('''Untermenü:
Wählen Sie eine der folgenden Funktionen:
    1. Eintrag bearbeiten
    2. Eintrag löschen
    3. zurück ins Hauptmenü
Ihre Eingabe: '''))
    if auswahl == 3:
        return
    funktionen = {1: Eintrag_bearbeiten, 2: Eintrag_löschen}
    funktion = funktionen.get(auswahl, fehler)
    funktion(manager)


def Eintrag_löschen(manager):
    print('Eintrag löschen:\n')


def Eintrag_bearbeiten(manager):
    print('Eintrag_bearbeiten\n')


def Eintrag_hinzufügen(manager):
    print('Eintrag hinzufügen:n')
    Untermenü(manager)


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
    # Neue "Datenbank" erstellen oder einlesen
    manager = Manager()
    menu(manager)


cli()
