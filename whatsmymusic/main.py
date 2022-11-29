# Importe
from flask import Flask, render_template, request, redirect
from whatsmymusic.datenbank import auslesen, speichern, sortiert_eintraege, auslesen_ausgewaehlt, eintrag_korrigiert

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
    typ = ["Lied", "Album"]
    genre = ["Rock", "Rap"]
    intepret = ["Declan McKenna", "Eminem", "Lana Del Rey"]
    monat = ["11-2022", "10-2022", "09-2022"]
    jahr = [2002, 2015, 2022]
    bewertung = [1, 2, 3, 4, 5]
    if request.method == "GET":
        eintraege = auslesen()
    if request.method == "POST":
        eintraege = sortiert_eintraege(request.form.to_dict())
    return render_template("archiv.html", typen=typ, genres=genre, intepreten=intepret, monate=monat, jahre=jahr,
                               bewertungen=bewertung, eintraege=eintraege)



# Route Einträge bearbeiten
@app.route("/bearbeiten/<eintrag_id>", methods=["GET", "POST"])
def eintragbearbeiten(eintrag_id):
    if request.method == "GET":
        eintrag = auslesen_ausgewaehlt(int(eintrag_id))
        return render_template("bearbeiten.html", eintrag=eintrag)
    if request.method == "POST":
        eintrag_korrigiert(int(eintrag_id), request.form.to_dict())
        return redirect("/archiv")


# Route Datenvisualisierung
@app.route("/statistiken")
def statistikopen():
    return render_template("statistiken.html")


# Run App
if __name__ == "__main__":
    app.run(debug=True, port=5005)
