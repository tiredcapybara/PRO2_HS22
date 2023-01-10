# Importe für Datenspeicherung, Datumsformate und Balkendiagramm zeichnen
import json
from datetime import datetime
import plotly.express as px
from plotly.offline import plot


# Funktion um Einträge auszulesen aus json File
def auslesen():
    file = open("databasesongs.json")
    # Variable eintraege wird dem Inhalt des json Files gleichgesetzt
    eintraege = json.load(file)
    return eintraege


# Neue Einträge abspeichern
def speichern(daten):
    # Variable eintraege wird Daten aus File gleichgesetzt
    eintraege = auslesen()
    # id erstellen um Einträge wiederzufinden für löschen und bearbeiten. Einzigartig für jeden Eintrag
    id_eintrag = eintraege[-1]["id"]
    # Dictionary Struktur für Einträge aufbauen
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
    # Neuer Eintrag wird am Ende des Dictionary angehängt
    eintraege.append(eintrag)
    # json formatieren
    eintraege_json = json.dumps(eintraege, indent=4)
    # json file wird verändert
    file = open("databasesongs.json", "w")
    file.write(eintraege_json)
    file.close()
    return


# Filterungsfunktion für Einträge
def sortiert_eintraege(merkmale):
    # Variable eintraege wird Daten aus File gleichgesetzt
    eintraege = auslesen()
    # Liste der Einträge nach Filtern, zur Ausgabe
    eintraege_gefiltert = []
    # Checks für Übereinstimmung der Filterung
    for eintrag in eintraege:
        # Hördatum wird in Schema Jahr, Monat und Tag festgehalten, um Jahr und Monat auszupicken
        date = eintrag["gehoert"]
        date = datetime.strptime(date, "%Y-%m-%d")
        # Checks um die Einträge
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
    # Gefilterte Einträge werden ausgegeben
    return eintraege_gefiltert


def auslesen_ausgewaehlt(eintrag_id):
    # Hiermit wird die id von ausgewählten Einträgen eingelesen und kann denn richtigen Eintrag ausgeben. Für bearbeiten und löschen benötigt
    for eintrag in auslesen():
        if eintrag["id"] == eintrag_id:
            return eintrag
    return


# Veränderungen in Beiträgen festhalten
def eintrag_korrigiert(eintrag_id, daten):
    # Variable position für die Suche nach richtiger id
    position = 0
    # Variable eintraege wird Daten aus File gleichgesetzt
    eintraege = auslesen()
    # Aufbau bearbeiteter Eintrag (gleich wie der normale Eintrag im file)
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
    # Die ids im file werden alle durch-kontrolliert bis man zum id des zu bearbeitenden Eintrages kommt
    for eintrag in eintraege:
        if eintrag["id"] == eintrag_id:
            eintraege[position] = eintrag_bearbeitet
        else:
            position = position + 1

    # Auf Daten in json zugreifen und änderungen abgeben
    eintraege_json = json.dumps(eintraege, indent=4)
    file = open("databasesongs.json", "w")
    file.write(eintraege_json)
    file.close()
    return auslesen_ausgewaehlt(eintrag_id)


# json anpassen nach Löschung
def eintrag_loeschen(eintrag_id):
    # Variable eintraege wird Daten aus File gleichgesetzt
    eintraege = auslesen()
    # Leere Liste für die nicht-gelöschten Einträge
    eintraege_neu = []
    for eintrag in eintraege:
        # Es wird kontrolliert, ob dieser Eintrag der zu löschende Eintrag ist. Falls es dieser NICHT ist wird der Beitrag in die erstellte Liste hinzugefügt
        if eintrag["id"] != eintrag_id:
            eintraege_neu.append(eintrag)
    # Die Daten aus der werden zum json file hinzugefügt. Der gelöschte Beitrag ist nicht in der Liste ergo verschwindet dieser
    eintraege_json = json.dumps(eintraege_neu, indent=4)
    file = open("databasesongs.json", "w")
    file.write(eintraege_json)
    file.close()
    return


# Funktion für Aufteilung Datum in Monat und Jahr in Liste
def liste_gehoert():
    # Variable eintraege wird Daten aus File gleichgesetzt
    eintraege = auslesen()
    # Leere Listen werden erstellt, um Daten zu Monaten und Jahren zu speichern
    gehoert_monate = []
    gehoert_jahre = []
    for eintrag in eintraege:
        # Jeder einzelne Eintrag wird kontrolliert, das Hördatum ausgewählt und in das richtige Format gespeichert
        date = eintrag["gehoert"]
        date = datetime.strptime(date, "%Y-%m-%d")
        # Monat wird ausgepickt und in die Liste eingetragen, Doppelnennungen werden nicht berrücksichtigt
        if date.month not in gehoert_monate:
            gehoert_monate.append(date.month)
        # Jahr wird ausgepickt und in die Liste eingetragen, Doppelnennungen werden nicht berrücksichtigt
        if date.year not in gehoert_jahre:
            gehoert_jahre.append(date.year)
    # Listen werden sortiert
    gehoert_monate = sorted(gehoert_monate)
    gehoert_jahre = sorted(gehoert_jahre)
    #Die Listen werden im Dictionary resultat eingetragen
    resultat = {
        "monate": gehoert_monate,
        "jahre": gehoert_jahre
    }
    return resultat


# Funktion für das Zeichnen des Diagramms
def statistik_zeichnen(auswahl_x):
    # Variable eintraege wird Daten aus File gleichgesetzt
    eintraege = auslesen()
    # Leeres Dictionary für Diagramm-Daten wird erstellt
    ratings = {}
    for eintrag in eintraege:
        # Es wird durch jeden Eintrag gegangen und alle jeweiligen Ratings rausgenommen. Die gleichen Ratings werden gezählt
        # die Anzahl von einem jeweiligen Rating wird als Value im Dictionary festgehalten
        if eintrag["rating"] not in ratings:
            ratings[eintrag["rating"]] = 1
        else:
            ratings[eintrag["rating"]] += 1
    # Wiederholung des gleichen Prinzips
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
    releases = {}
    for eintrag in eintraege:
        if eintrag["release"] not in releases:
            releases[eintrag["release"]] = 1
        else:
            releases[eintrag["release"]] += 1

    # Check, welche Daten für Diagramm ausgewählt wurden
    if auswahl_x == "rating":
        # Das erstellte Dictionary wird in Keys und Values aufgeteilt. X-Achse = keys Y-Achse = values (diese sind je nach Diagramm verschieden)
        x = ratings.keys()
        y = ratings.values()
    elif auswahl_x == "genre":
        x = genres.keys()
        y = genres.values()
    elif auswahl_x == "release":
        x = releases.keys()
        y = releases.values()
    else:
        x = intepreten.keys()
        y = intepreten.values()

    # Diagramm zeichnen
    fig = px.bar(x=x, y=y)
    div = plot(fig, output_type="div")
    return div
