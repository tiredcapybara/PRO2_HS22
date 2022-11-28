from flask import Flask, render_template, request, redirect
from whatsmymusic.datenbank import auslesen, auslesenalb, album_speichern, song_speichern

app = Flask("whatsmymusic")


# Routen zu Seiten
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/neuer-eintrag-album", methods=["GET", "POST"])
def neualbum():
    if request.method == "GET":
        return render_template("neuer-eintrag-album.html")

    if request.method == "POST":
        daten_alben = request.form.to_dict()
        album_speichern(daten_alben)
        print(daten_alben)
        return redirect("/archiv")


@app.route("/neuer-eintrag-song", methods=["GET", "POST"])
def neusong():
    if request.method == "GET":
        return render_template("neuer-eintrag-song.html")

    if request.method == "POST":
        daten_songs = request.form.to_dict()
        song_speichern(daten_songs)
        return redirect("/archiv")


@app.route("/archiv")
def archivopen():
    songs = auslesen()
    return render_template("archiv.html", songs=songs)


@app.route("/statistiken")
def statistikopen():
    return render_template("statistiken.html")


if __name__ == "__main__":
    app.run(debug=True, port=5005)
