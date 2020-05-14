try:
    from passwordmanager import cli

    cli.cli()
except ModuleNotFoundError as e:
    print(f"Das Modul {e.name} fehlt, bitte mit 'pip install {e.name}' installieren")
