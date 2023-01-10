# Importe flask und Funktionen aus datenbank.py
from flask import Flask, render_template, request, redirect
from whatsmymusic.datenbank import auslesen, speichern, sortiert_eintraege, auslesen_ausgewaehlt, eintrag_korrigiert, \
    eintrag_loeschen, liste_gehoert, statistik_zeichnen

app = Flask("whatsmymusic")


# Route Startseite
@app.route("/")
def index():
    # HTML der Startseite wird angezeigt
    return render_template("index.html")


# Route Eintrag erstellen
@app.route("/neuer-eintrag", methods=["GET", "POST"])
def neueintrag():
    # HTML wird angezeigt bei Öffnen
    if request.method == "GET":
        return render_template("neuer-eintrag.html")
    # Bei Erstellen von neuem Eintrag werden Daten gespeichert und man wird zm Archiv weitergeleitet
    if request.method == "POST":
        daten_eintraege = request.form.to_dict()
        speichern(daten_eintraege)
        return redirect("/archiv")


# Route Archiv
@app.route("/archiv", methods=["GET", "POST"])
def archivopen():
    # Die verschiedenen Filtermöglichkeiten als Listen formatieren, hier werden alle Einträge ausgelesen und
    # die Listen mit nur einzigartigen Einträgen erstellt um nachher diese in den Auswahlfelder angezeigt zu kriegen
    eintraege = auslesen()
    # Intepret aus jedem Eintrag wird in eine Liste hinzugefügt
    liste_intepreten = [resultat['intepret'] for resultat in eintraege]
    # Doppeltnennungen werden gelöscht
    liste_intepreten = set(liste_intepreten)
    # Liste wird sortiert. Das gleiche passiert auch für die unteren 2 Listen
    liste_intepreten = sorted(liste_intepreten)

    liste_genre = [resultat['genre'] for resultat in eintraege]
    liste_genre = set(liste_genre)
    liste_genre = sorted(liste_genre)

    liste_release = [resultat['release'] for resultat in eintraege]
    liste_release = set(liste_release)
    liste_release = sorted(liste_release)

    # Auswahlmöglichkeiten Select Filter erstellen
    typ = ["Lied", "Album"]
    genre = liste_genre
    intepret = liste_intepreten
    monat = liste_gehoert()["monate"]
    hoerjahr = liste_gehoert()["jahre"]
    jahr = liste_release
    bewertung = ["1", "2", "3", "4", "5"]

    # GET Methode zeigt es automatisch alle Einträge an (also wenn man das Archiv einfach nur öffnet
    if request.method == "GET":
        eintraege = auslesen()
    # Nach der Auswahl der Filter werden nur die Einträge angezeigt, welche noch im gefilterten Dictionary sind, also den ausgewählten Kriterien ensprechen
    if request.method == "POST":
        eintraege = sortiert_eintraege(request.form.to_dict())
    return render_template("archiv.html", typen=typ, genres=genre, intepreten=intepret, monate=monat,
                           hoerjahre=hoerjahr, jahre=jahr, bewertungen=bewertung, eintraege=eintraege)


# Route Einträge bearbeiten. Eintrag wird mittels id angezeigt
@app.route("/bearbeiten/<eintrag_id>", methods=["GET", "POST"])
def eintragbearbeiten(eintrag_id):
    # Ausgewählter Eintrag wird angezeigt in Bearbeitungs-Maske
    if request.method == "GET":
        eintrag = auslesen_ausgewaehlt(int(eintrag_id))
        return render_template("bearbeiten.html", eintrag=eintrag)
    # Änderungen werden in json file gespeichert
    if request.method == "POST":
        eintrag_korrigiert(int(eintrag_id), request.form.to_dict())
        return redirect("/archiv")


# Route Eintraege löschen
@app.route("/loeschen/<eintrag_id>", methods=["GET", "POST"])
def eintragloeschenopen(eintrag_id):
    # Bei Klick auf Delete-Button wird der Eintrag mittels id gelöscht.
    eintrag_loeschen(int(eintrag_id))
    return redirect("/archiv")


# Route Statistiken
@app.route("/statistiken", methods=["GET", "POST"])
def grafik():
    # Durch Diagramm-Titel wird das h3 im html erstellt, um das Diagramm besser deuten zu können
    # Bei Öffnen der Seite sieht man nur die 2 Selection-Balken
    if request.method == "GET":
        return render_template("statistiken.html", diagramm_titel="false")
    # Nach Auswahl wird kontrolliert, was als x-Achse ausgewählt wurde
    if request.method == "POST":
        # Es wird ausgewählt, welches Diagramm angezeigt wird (basierend auf Auswahl)
        auswahl_x = request.form.to_dict()["x-achse"]
        div = statistik_zeichnen(auswahl_x)
        # Diagramm-Titel wird angepasst
        if auswahl_x == "rating":
            diagramm_titel = "Bewertungen"
        elif auswahl_x == "intepret":
            diagramm_titel = "Intepreten"
        elif auswahl_x == "release":
            diagramm_titel = "Erscheinungsjahre"
        else:
            diagramm_titel = "Genres"
        # Diagramm wird angezeigt
        return render_template("statistiken.html", barchart=div, diagramm_titel=diagramm_titel)


# Run App
if __name__ == "__main__":
    app.run(debug=True, port=5005)
