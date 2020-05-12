try:
    from passwordmanager import cli

    cli.cli()
except ModuleNotFoundError:
    print("Das Modul 'cryptography' ist erforderlich, aber nicht installiert")
