import json
from datetime import datetime

# Einträge auslesen aus JSON
def auslesen():
    file = open("databasesongs.json")
    eintraege = json.load(file)
    return eintraege


# Neue Einträge abspeichern
def speichern(daten):
    eintraege = auslesen()
    # id erstellen um Einträge wiederzufinden für löschen und bearbeiten
    id_eintrag = eintraege[-1]["id"]
    # Dict Struktur für Einträge aufbauen
    eintrag = {
        "id": id_eintrag + 1,
        "titel": daten["titel"],
        "intepret": daten["intepret"],
        "genre": daten["genre"],
        "gehoert": daten["gehoert"],
        "release": daten["release"],
        "rating": daten["rating"],
        "typ": daten["typ"]
    }
    eintraege.append(eintrag)
    print(eintraege)
    # JSON formatieren und auslesen
    eintraege_json = json.dumps(eintraege, indent=4)
    file = open("databasesongs.json", "w")
    file.write(eintraege_json)
    file.close()
    return

# Filterungsfunktion für Einträge
def sortiert_eintraege(merkmale):
    eintraege = auslesen()
    eintraege_gefiltert = []
    # Checks für Übereinstimmung der Filterung
    for eintrag in eintraege:
        date = eintrag["gehoert"]
        date = datetime.strptime(date, "%Y-%m-%d")
        checks = (
            merkmale["typ"] == "" or eintrag["typ"] == merkmale["typ"],
            merkmale["intepret"] == "" or eintrag["intepret"] == merkmale["intepret"],
            merkmale["genre"] == "" or eintrag["genre"] == merkmale["genre"],
            merkmale["release"] == "" or eintrag["release"] == merkmale["release"],
            merkmale["gehoert"] == "" or str(date.month) == merkmale["gehoert"],
            merkmale["hoerjahr"] == "" or str(date.year) == merkmale["hoerjahr"],
            merkmale["rating"] == "" or eintrag["rating"] == merkmale["rating"]
        )
        if all(checks):
            eintraege_gefiltert.append(eintrag)
    return eintraege_gefiltert


def auslesen_ausgewaehlt(eintrag_id):
    for eintrag in auslesen():
        if eintrag["id"] == eintrag_id:
            return eintrag
    return

# Veränderungen in Beiträgen festhalten
def eintrag_korrigiert(eintrag_id, daten):
    position = 0
    eintraege = auslesen()
    eintrag_bearbeitet = {
        "id": eintrag_id,
        "titel": daten["titel"],
        "intepret": daten["intepret"],
        "genre": daten["genre"],
        "gehoert": daten["gehoert"],
        "release": daten["release"],
        "rating": daten["rating"],
        "typ": daten["typ"]
    }
# Erstellung ids für Einträge
    for eintrag in eintraege:
        if eintrag["id"] == eintrag_id:
            print(eintrag["id"])
            print(position)
            eintraege[position] = eintrag_bearbeitet
        else:
            position = position + 1

# Auf Daten in json zugreifen
    eintraege_json = json.dumps(eintraege, indent=4)
    file = open("databasesongs.json", "w")
    file.write(eintraege_json)
    file.close()
    return auslesen_ausgewaehlt(eintrag_id)
# JSON Liste anpassen nach Löschung
def eintrag_loeschen(eintrag_id):
    eintraege = auslesen()
    eintraege_neu = []
    for eintrag in eintraege:
        if eintrag["id"] != eintrag_id:
            eintraege_neu.append(eintrag)
    eintraege_json = json.dumps(eintraege_neu, indent=4)
    file = open("databasesongs.json", "w")
    file.write(eintraege_json)
    file.close()
    return
# Funktion für aufteilung Datum in Monat und Jahr
def liste_gehoert():
    eintraege = auslesen()
    gehoert_monate = []
    gehoert_jahre = []
    for eintrag in eintraege:
        date = eintrag["gehoert"]
        date = datetime.strptime(date, "%Y-%m-%d")
        if date.month not in gehoert_monate:
            gehoert_monate.append(date.month)
        if date.year not in gehoert_jahre:
            gehoert_jahre.append(date.year)

    gehoert_monate = sorted(gehoert_monate)
    gehoert_jahre = sorted(gehoert_jahre)

    resultat = {
        "monate": gehoert_monate,
        "jahre": gehoert_jahre
    }
    return resultat
# Erstellung der Listen für die Statistiken
def auslesen_statistiken():
    eintraege = auslesen()
    liste_genres = [resultat['genre'] for resultat in eintraege]
    liste_genres = set(liste_genres)
    liste_genres = sorted(liste_genres)

    liste_ratings = [resultat['rating'] for resultat in eintraege]
    liste_ratings = set(liste_ratings)
    liste_ratings = sorted(liste_ratings)



