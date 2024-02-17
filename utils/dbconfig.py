import mysql.connector

# connect to the database.

from rich import print as printc
from rich.console import Console
console = Console()
def dbconfig():
    try:
        db = mysql.connector.connect(
            host='localhost',
            user='pm',
            passwd='password'
        )
        return db
    except Exception as e:
        printc("An error occurred while connecting to the database:", e)
        return None