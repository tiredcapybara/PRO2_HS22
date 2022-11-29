# Importe
from flask import Flask, render_template, request, redirect
from whatsmymusic.datenbank import auslesen, auslesenalb, album_speichern, song_speichern

app = Flask("whatsmymusic")


# Route Startseite
@app.route("/")
def index():
    return render_template("index.html")


# Route Album-Eintrag erstellen
@app.route("/neuer-eintrag-album", methods=["GET", "POST"])
def neualbum():
    if request.method == "GET":
        return render_template("neuer-eintrag-album.html")

    if request.method == "POST":
        daten_alben = request.form.to_dict()
        album_speichern(daten_alben)
        print(daten_alben)
        return redirect("/archiv")


# Route Song-Eintrag erstellen
@app.route("/neuer-eintrag-song", methods=["GET", "POST"])
def neusong():
    if request.method == "GET":
        return render_template("neuer-eintrag-song.html")

    if request.method == "POST":
        daten_songs = request.form.to_dict()
        song_speichern(daten_songs)
        return redirect("/archiv")


# Route Archiv öffnen
@app.route("/archiv")
def archivopen():
    genre = ["Rock", "Rap"]
    return render_template("archiv.html", genres=genre)

    # Wie kann ich zwischen Alben und Songs unterscheiden? If Checkmark1 == Songs?
    #if request.method == "GET":
      #  return render_template("archiv.html")
    #if request.method == "POST":

#songs = auslesen()
#   selection = []
  #  for song in songs:
 #       if song["genre"] == "Rock":
 #           selection.append(song)


@app.route("/bearbeiten")
def eintragbearbeiten():
    return render_template("bearbeiten.html")

@app.route("/statistiken")
def statistikopen():
    return render_template("statistiken.html")


# Run App
if __name__ == "__main__":
    app.run(debug=True, port=5005)
