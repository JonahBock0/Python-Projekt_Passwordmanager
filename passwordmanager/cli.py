import sys, getpass

MASTERPW = "HAWK2020"
PASSWORD = getpass.getpass("Master-Passwort eingeben: ")

while MASTERPW != PASSWORD:
    if MASTERPW != PASSWORD:
        print("Invalid Password\n")
        break
if MASTERPW == PASSWORD:
    print("Password correct\n")


    def Untermenü():
        auswahl_Untermenü = int(input('Untermenü:\nWählen Sie eine der folgenden Funktionen:\
                     \n\n\t1. Eintrag bearbeiten\n\t2. Eintrag löschen\n\t3. zurück ins Hauptmenü\n\nIhre Eingabe: '))
        switch_Untermenü = {1: Eintrag_bearbeiten, 2: Eintrag_löschen}
        funktion_Untermenü = switch_Untermenü.get(auswahl_Untermenü, fehler)
        funktion_Untermenü()


    def Eintrag_löschen():
        print('Eintrag löschen:\n')


    def Eintrag_bearbeiten():
        print('Eintrag_bearbeiten\n')


    def Eintrag_hinzufügen(service, password):
        print('Eintrag hinzufügen:n')
        Untermenü()


    def Eintrag_anzeigen():
        print('Eintrag Anzeigen:\n')
        Untermenü()


    def Programm_verlassen():
        print('Programm_verlassen:\n')
        sys.exit()


    def fehler():
        print("Die eingegebene Zahl ist nicht im Menü")


    def cli(manager):
        auswahl_Hauptmenü = int(input('Willkommen im Passwordmanager\n\nHauptmenü:\nWählen Sie eine der folgenden Funktionen:\
                                \n\n\t\t1. Eintrag hinzufügen\n\t\t2. Eintrag anzeigen\n\t\t3. Programm verlassen\n\nIhre Eingabe: '))
        switch_Hauptmenü = {1: Eintrag_hinzufügen, 2: Eintrag_anzeigen, 3: Programm_verlassen}
        funktion_Hauptmenü = switch_Hauptmenü.get(auswahl_Hauptmenü, fehler)
        funktion_Hauptmenü()


    cli(0)
