# Importe
from flask import Flask, render_template, request, redirect
from whatsmymusic.datenbank import auslesen, speichern, sortiert_eintraege, auslesen_ausgewaehlt, eintrag_korrigiert, \
    eintrag_loeschen, liste_gehoert
import plotly.express as px
from plotly.offline import plot

app = Flask("whatsmymusic")


# Route Startseite
@app.route("/")
def index():
    return render_template("index.html")


# Route Eintrag erstellen
@app.route("/neuer-eintrag", methods=["GET", "POST"])
def neueintrag():
    if request.method == "GET":
        return render_template("neuer-eintrag.html")

    if request.method == "POST":
        daten_eintraege = request.form.to_dict()
        speichern(daten_eintraege)
        return redirect("/archiv")


# Route Archiv öffnen
@app.route("/archiv", methods=["GET", "POST"])
def archivopen():
    # Die verschiedenen Filtermöglichkeiten als Listen formatieren
    eintraege = auslesen()
    liste_intepreten = [resultat['intepret'] for resultat in eintraege]
    liste_intepreten = set(liste_intepreten)

    liste_genre = [resultat['genre'] for resultat in eintraege]
    liste_genre = set(liste_genre)

    liste_release = [resultat['release'] for resultat in eintraege]
    liste_release = set(liste_release)
    # Auswahlmöglichkeiten Select Filter
    typ = ["Lied", "Album"]
    genre = liste_genre
    intepret = liste_intepreten
    monat = liste_gehoert()["monate"]
    hoerjahr = liste_gehoert()["jahre"]
    jahr = liste_release
    bewertung = ["1", "2", "3", "4", "5"]

    if request.method == "GET":
        eintraege = auslesen()
    if request.method == "POST":
        eintraege = sortiert_eintraege(request.form.to_dict())
    return render_template("archiv.html", typen=typ, genres=genre, intepreten=intepret, monate=monat,
                           hoerjahre=hoerjahr, jahre=jahr, bewertungen=bewertung, eintraege=eintraege)


# Route Einträge bearbeiten
@app.route("/bearbeiten/<eintrag_id>", methods=["GET", "POST"])
def eintragbearbeiten(eintrag_id):
    if request.method == "GET":
        eintrag = auslesen_ausgewaehlt(int(eintrag_id))
        return render_template("bearbeiten.html", eintrag=eintrag)
    if request.method == "POST":
        eintrag_korrigiert(int(eintrag_id), request.form.to_dict())
        return redirect("/archiv")


@app.route("/loeschen/<eintrag_id>", methods=["GET", "POST"])
def eintraglöschenopen(eintrag_id):
    eintrag_loeschen(int(eintrag_id))
    return redirect("/archiv")


# Route Datenvisualisierung
@app.route("/statistiken")
def statistikopen():
    eintraege = auslesen()
    rating = {}
    for eintrag in eintraege:
        if eintrag[1] not in rating:
            rating[eintrag[1]] = 1
        else:
            rating[eintrag[1]] += 1

    x = rating.keys()
    y = rating.values()
    fig = px.bar(x=x, y=y)
    div = plot(fig, output_type="div")

    return render_template("statistiken.html", barchart=div, seitentitel="Piechart")


# Run App
if __name__ == "__main__":
    app.run(debug=True, port=5005)
