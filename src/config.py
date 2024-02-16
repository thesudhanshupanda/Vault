import os
import sys
import string
import random
import hashlib
import sys
from getpass import getpass
from utils.dbconfig import dbconfig

from rich import print as printc
from rich.console import Console

console = Console()

def generateDeviceSecret(length =10):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def config():
    # create a database
    db = dbconfig()
    cursor = db.cursor()
    printc("[green][+] Creating new config [/green]")

    try:
        cursor.execute("Create Database pm")
    except Exception as e:
        printc("[red][!] An error occured while trying to create db.")
        console.print_exception(show_locals=True)
        sys.exit(0)
    printc("[green][+][/green] Database pm created")
    
    # create a table
    query = "CREATE TABLE pm.secrets (masterkey_hash TEXT NOT, device_secret TEXT NOT NULL)"
    res = cursor.execute(query)
    printc("[green][+][/green] Table 'secrets' created")
    
    
    query = "CREATE TABLE pm.entries (sitename TEXT NOT, siteurl TEXT NOT, email TEXT, username TEXT, password TEXT not null )"
    res = cursor.execute(query)
    printc("[green][+][/green] Table 'entries' created")
    
    
    while 1:
        mp = getpass("choose a MASTER PASSWORD:")
        if mp == getpass("Re-type:") and mp!="":
            break
        
#Hash the master password
hashed_mp = hashlib.sha256(mp.encode()).hexdigest()
printc("[green][+][/green] Generated hash of MASTER PASSWORD")

# generate a device secret
ds = generateDeviceSecret()
printc("[green][+][/green] Device Secret generated")

#Add them to db
query = "INSERT INTO pm.secrets (masterkey_hash, device_secret) values (%s, %s)"
val = (hashed_mp, ds)
cursor.execute(query, val)
db.commit()

printc("[green][+][/green] Added to the Database")

printc("[green][+] Configuration done! [/green]")

db.close()

config()