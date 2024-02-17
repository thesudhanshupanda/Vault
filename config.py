import os
import sys
import string
import random
import hashlib
from getpass import getpass
from dbconfig import dbconfig
from rich import print as printc
from rich.console import Console

console = Console()

def generateDeviceSecret(length=10):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def config():
    try:
        # create a database
        db = dbconfig()
        cursor = db.cursor()
        printc("[green][+] Creating new config [/green]")
        cursor.execute("CREATE DATABASE IF NOT EXISTS pm")

        # create a table
        query_secrets = "CREATE TABLE IF NOT EXISTS pm.secrets (masterkey_hash TEXT NOT NULL, device_secret TEXT NOT NULL)"
        cursor.execute(query_secrets)
        printc("[green][+][/green] Table 'secrets' created")

        query_entries = "CREATE TABLE IF NOT EXISTS pm.entries (sitename TEXT NOT NULL, siteurl TEXT NOT NULL, email TEXT, username TEXT, password TEXT NOT NULL)"
        cursor.execute(query_entries)
        printc("[green][+][/green] Table 'entries' created")

        mp = ""
        printc("[green][+] A [bold]MASTER PASSWORD[/bold] is the only password you will need to remember in order to access all your other passwords. Choosing a strong [bold]MASTER PASSWORD[/bold] is essential because all your other passwords will be [bold]encrypted[/bold] with a key that is derived from your [bold]MASTER PASSWORD[/bold]. Therefore, please choose a strong one that has upper and lower case characters, numbers, and also special characters. Remember your [bold]MASTER PASSWORD[/bold] because it won't be stored anywhere by this program, and you also cannot change it once chosen. [/green]\n")

        while True:
            mp = getpass("choose a MASTER PASSWORD:")
            if mp == getpass("Re-type:") and mp != "":
                break

        # Hash the master password
        hashed_mp = hashlib.sha256(mp.encode()).hexdigest()
        printc("[green][+][/green] Generated hash of MASTER PASSWORD")

        # generate a device secret
        ds = generateDeviceSecret()
        printc("[green][+][/green] Device Secret generated")

        # Add them to db
        query_insert = "INSERT INTO pm.secrets (masterkey_hash, device_secret) VALUES (%s, %s)"
        val = (hashed_mp, ds)
        cursor.execute(query_insert, val)
        db.commit()

        printc("[green][+][/green] Added to the Database")

        printc("[green][+] Configuration done! [/green]")

        db.close()

    except Exception as e:
        printc("[red][!] An error occurred: {}[/red]".format(e))
        console.print_exception(show_locals=True)
        sys.exit(0)

config()
