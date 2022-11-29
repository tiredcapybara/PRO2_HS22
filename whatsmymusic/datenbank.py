import json


def auslesen():
    file = open("databasesongs.json")
    eintraege = json.load(file)
    return eintraege


def speichern(daten):
    eintraege = auslesen()
    id_eintrag = eintraege[-1]["id"]

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

    eintraege_json = json.dumps(eintraege, indent=4)
    file = open("databasesongs.json", "w")
    file.write(eintraege_json)
    file.close()
    return
def sortiert_eintraege(merkmale):
    eintraege = auslesen()
    eintraege_gefiltert = []
    for eintrag in eintraege:
        checks = (
            merkmale["typ"] == "" or eintrag["typ"] == merkmale["typ"],
            merkmale["intepret"] == "" or eintrag["intepret"] == merkmale["intepret"],
            merkmale["release"] == "" or eintrag["release"] == merkmale["release"],
            merkmale["gehoert"] == "" or eintrag["gehoert"] == merkmale["gehoert"],
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

    for eintrag in eintraege:
        if eintrag["id"] == eintrag_id:
            print(eintrag["id"])
            print(position)
            eintraege[position] = eintrag_bearbeitet
        else:
            position = position + 1


    eintraege_json = json.dumps(eintraege, indent=4)
    file = open("databasesongs.json", "w")
    file.write(eintraege_json)
    file.close()
    return auslesen_ausgewaehlt(eintrag_id)


