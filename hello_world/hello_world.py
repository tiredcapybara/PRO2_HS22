from flask import Flask
from flask import render_template
import random

app = Flask("Hello World")

@app.route('/greet_all')
def greet_all():
    auswahl = ["Fabian", "Markus", "Franz", "Armando"]
    ausgewaehlter_name = random.choice(auswahl)
    return render_template("hello_all.html", alle_namen=auswahl)

@app.route('/hello')
def hello_world():
    auswahl = ["Fabian", "Markus", "Franz", "Armando"]
    ausgewaehlter_name = random.choice(auswahl)
    return render_template("hello.html", name=ausgewaehlter_name)

@app.route("/hallo")
@app.route("/hallo/<name>")
def name_selber(name="Welt"):
    return f'hallo, {name}!'


if __name__ == "__main__":
    app.run(debug=True, port=5000)