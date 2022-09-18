from flask import render_template
from registro_ig import app



@app.route("/")
def index():
    return render_template("index.html", pageTitle = "Lista")

@app.route("/nuevo")
def alta():
    return render_template("new.html", pageTitle = "Alta")

@app.route("/modification")
def modificacion():
    return render_template("modification.html", pageTitle = "Modificacion")

@app.route("/baja")
def baja():
    return render_template("baja.html", pageTitle = "Baja")