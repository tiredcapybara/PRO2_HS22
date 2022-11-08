from flask import Flask, render_template

app = Flask(__name__)

# Routen verschiedene Seiten
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/neuer-eintrag-album")
def neualbum():
    return render_template("neuer-eintrag-album.html")

@app.route("/neuer-eintrag-song")
def neusong():
    return render_template("neuer-eintrag-song.html")

@app.route("/archiv")
def archivopen():
    return render_template("archiv.html")

@app.route("/statistiken")
def statistikopen():
    return render_template("statistiken.html")

if __name__ == "__main__":
    app.run(debug=True, port=5005)
