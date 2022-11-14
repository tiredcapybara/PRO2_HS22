from flask import Flask
from flask import render_template
from flask import request

from whatsmymusic.datenbank import abspeichern
from whatsmymusic.datenbank import auslesen

app = Flask("whatsmymusic")


# Routen verschiedene Seiten
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/neuer-eintrag-album")
def neualbum():
    return render_template("neuer-eintrag-album.html")


@app.route("/neuer-eintrag-song", methods=["GET", "POST"])
def neusong():
    if request.method == "GET":
        return render_template("neuer-eintrag-song.html")

    if request.method == "POST":
        titel = request.form['titel']
        intepret = request.form['intepret']
        genre = request.form['genre']
        gehoert = request.form['gehoert']
        release = request.form['release']
        rating = request.form['rating']
        print(f"Request Form Titel: {titel}")
        print(f"Request Form Intepret: {intepret}")
        print(f"Request Form Genre: {genre}")
        print(f"Request Form Gehört am: {gehoert}")
        print(f"Request Form Erscheinungsjahr: {release}")
        print(f"Request Form Rating: {rating}")
        abspeichern(titel, intepret, genre, gehoert, release, rating)
        return "Eintrag gespeichert Neuer Eintrag"


@app.route("/archiv")
def archivopen():
    songs = auslesen()
    songs_html = songs.replace("\n", "<br>")
    songs_liste = songs.split("\n")
    neue_liste = []
    for eintrag in songs_liste:
        titel, intepret, genre, gehoert, release, rating = eintrag.split(",")
        neue_liste.append([titel, intepret, genre, gehoert, release, rating])
    return render_template("archiv.html", liste=neue_liste)


@app.route("/statistiken")
def statistikopen():
    return render_template("statistiken.html")


if __name__ == "__main__":
    app.run(debug=True, port=5005)
