import getpass
from passwordmanager.manager import Manager

def Untermenü(manager):
    auswahl = int(input('Untermenü:\nWählen Sie eine der folgenden Funktionen:\
                 \n\n\t1. Eintrag bearbeiten\n\t2. Eintrag löschen\n\t3. zurück ins Hauptmenü\n\nIhre Eingabe: '))
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
        auswahl = int(input('Willkommen im Passwordmanager\n\nHauptmenü:\nWählen Sie eine der folgenden Funktionen:\
                                \n\n\t\t1. Eintrag hinzufügen\n\t\t2. Eintrag anzeigen\n\t\t3. Programm verlassen\n\nIhre Eingabe: '))
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