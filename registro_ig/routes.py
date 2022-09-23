
from flask import render_template, request, redirect, url_for
import csv
from config import MOVIMIENTOS_FILE, LAST_ID_FILE
from registro_ig import app
from datetime import date
from registro_ig.models import select_all, select_by, delete_by, insert, modification
import os

@app.route("/")
def index():
    return render_template("index.html", pageTitle = "Lista", movements=select_all())

@app.route("/nuevo", methods=["GET", "POST"])
def alta():
    if request.method == "GET":
        return render_template("new.html", pageTitle = "Alta", dataForm={})
    else: 
        errores = validaFormulario(request.form)
        if not errores:
            insert([request.form["date"], request.form["concept"], request.form["quantity"]])

            return redirect("/")
        else:
            return render_template("new.html", pageTitle="Alta", msgErrors=errores, dataForm=dict(request.form))

def validaFormulario(camposFormulario):
    errores = []
    hoy = date.today().isoformat()
    if camposFormulario["date"] > hoy:
        errores.append("La fecha introducida es el futuro.")
    if not camposFormulario["concept"]:
        errores.append("Introduce un concepto para la transacción.")
    if camposFormulario["quantity"] == "" or float(camposFormulario["quantity"]) == 0.0:
        errores.append("Introduce una cantidad positiva o negativa.")

    return errores

@app.route("/modificar/<int:id>", methods=["GET","POST"])
def modifica(id):
    if request.method == "GET":
        registro_definitivo = select_by(id)

        if registro_definitivo:
            return render_template("modification.html", registro = registro_definitivo)
        else:
            return redirect(url_for("index"))
    else:
        """
        1. validar el registro de entrada
        2. si el registro es correcto lo sustituyo en movimientos.txt. La mejor manera es copiar registro a registro el fichero nuevo y dar el cambiazo
        3. redirect
        4. si el registro es incorrecto la gestion de errores que conocemos
        """
        errores = validaFormulario(request.form)
        if not errores:
            modification([request.form["id"], request.form["date"], request.form["concept"], request.form["quantity"]])

            return redirect("/")
        else:
            return render_template("modification.html", pageTitle="Modificacion", msgErrors=errores, registro=dict(request.form))

@app.route("/borrar/<int:id>", methods=["GET","POST"])
def borrar(id):
    if request.method == "GET":
      
        registro_definitivo = select_by(id)

        if registro_definitivo:
            return render_template("delete.html", registro = registro_definitivo)
        else:
            return redirect(url_for("index"))

    else:

        delete_by(id)

        return redirect(url_for("index"))

