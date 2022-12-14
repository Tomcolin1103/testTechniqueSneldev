import wikipedia
import sqlite3

# Connexion à la base de données
con = sqlite3.connect("db")
cur = con.cursor()
cur.execute("""
    CREATE TABLE IF NOT EXISTS famous_people(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        summary TEXT NOT NULL,
        unique (name)
    )
""")

name = str(input("Enter the full name of a famous people : ").title())
searchResult = wikipedia.search(name, results=1)

try:
    if name.upper() not in searchResult[0].upper():
        if wikipedia.suggest(name) is None:
            print("I don't know this person.")
        else:
            print(f"Did you mean {wikipedia.suggest(name)}?")
    else:
        summary = wikipedia.summary(searchResult[0], auto_suggest=False)
        cur.execute("""INSERT INTO famous_people(name, summary) 
                    VALUES(?, ?)""",
                    (searchResult[0], summary)
                    )
        con.commit()
except IndexError:
    print("I don't know this person.")
except sqlite3.IntegrityError:
    print(f"Person already in table ({searchResult[0]})")
except wikipedia.exceptions.DisambiguationError:
    print(f"Too much result, be more specific")





