import json
from datetime import datetime
import plotly.express as px
from plotly.offline import plot


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


# Funktion für Aufteilung Datum in Monat und Jahr
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


def statistik_zeichnen(auswahl_x):
    eintraege = auslesen()
    ratings = {}
    for eintrag in eintraege:
        if eintrag["rating"] not in ratings:
            ratings[eintrag["rating"]] = 1
        else:
            ratings[eintrag["rating"]] += 1
    genres = {}
    for eintrag in eintraege:
        if eintrag["genre"] not in genres:
            genres[eintrag["genre"]] = 1
        else:
            genres[eintrag["genre"]] += 1
    intepreten = {}
    for eintrag in eintraege:
        if eintrag["intepret"] not in intepreten:
            intepreten[eintrag["intepret"]] = 1
        else:
            intepreten[eintrag["intepret"]] += 1

    if auswahl_x == "rating":
        x = ratings.keys()
        y = ratings.values()
    elif auswahl_x == "genre":
        x = genres.keys()
        y = genres.values()
    else:
        x = intepreten.keys()
        y = intepreten.values()
    fig = px.bar(x=x, y=y)
    div = plot(fig, output_type="div")
    return div
