
from flask import render_template, request, redirect, url_for
import csv
from config import MOVIMIENTOS_FILE, LAST_ID_FILE
from registro_ig import app
from datetime import date
import os

@app.route("/")
def index():
    fichero = open(MOVIMIENTOS_FILE, "r")
    csvReader = csv.reader(fichero, delimiter=",", quotechar='"')
    """movimientos = []
    for movimiento in csvReader:
        movimientos.append(movimiento)"""
    movimientos = [movimiento for movimiento in csvReader] #esto es lo mismo que las tres líneas de arriba

    fichero.close()
    return render_template("index.html", pageTitle = "Lista", movements=movimientos)

@app.route("/nuevo", methods=["GET", "POST"])
def alta():
    if request.method == "GET":
        return render_template("new.html", pageTitle = "Alta", dataForm={})
    else:
        
        errores = validaFormulario(request.form)
        if not errores:
            fichero = open(LAST_ID_FILE,"r")
            registro = fichero.read()
            id = int(registro) + 1
            fichero.close()

            fichero = open(MOVIMIENTOS_FILE, "a", newline = "")
            csvWriter = csv.writer(fichero, delimiter=",", quotechar='"')
            # Generar un nuevo id
            # Leer todo el fichero y me quedo con el último registro
            # El nuevo id sera el id del ultimo registro + 1
            csvWriter.writerow(["{}".format(id), request.form["date"], request.form["concept"], request.form["quantity"]])
            fichero.close()

            fichero = open(LAST_ID_FILE, "w")
            fichero.write(str(id))
            fichero.close()

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


@app.route("/modification")
def modificacion():
    return render_template("modification.html", pageTitle = "Modificacion")

@app.route("/delete")
def baja():
    return render_template("delete.html", pageTitle = "Baja")

@app.route("/modificar/<int:id>", methods=["GET","POST"])
def modifica(id):
    if request.method == "GET":
        """
        1. Consultar en movimientos .txt y recuperar el movimiento con id de la petición
        2. Devolver el formulario html con los datos de mi registro
        """
        return render_template("modifica.html", registro = [])
    else:
        """
        1. validar el registro de entrada
        2. si el registro es correcto lo sustituyo en movimientos.txt. La mejor manera es copiar registro a registro el fichero nuevo y dar el cambiazo
        3. redirect
        4. si el registro es incorrecto la gestion de errores que conocemos
        """
        pass

@app.route("/borrar/<int:id>", methods=["GET","POST"])
def borrar(id):
    if request.method == "GET":
        """
        1. consultar en movimientos.txt y recuperar el registro con el id de la peticion
        2. devolver el formulario html con los datos de mi registro, no modificables
        3. tendra un boton que diga confirmar
        """
        fichero = open(MOVIMIENTOS_FILE, "r", newline="")
        csvReader = csv.reader(fichero, delimiter=",",quotechar='"')
        registro_definitivo = []
        for registro in csvReader:
            if registro[0] == str(id):
                registro_definitivo = registro
                break
        
        fichero.close()

        if registro_definitivo:
            return render_template("delete.html", registro = registro_definitivo)
        else:
            return redirect(url_for("index"))
    else:
        """
        borrar el registro
        """
        fichero_old = open(MOVIMIENTOS_FILE, "r")
        fichero = open("data/movimientos_nuevos.txt", "w", newline="")
        csvReader = csv.reader(fichero_old, delimiter=",", quotechar='"')
        csvWriter = csv.writer(fichero, delimiter=",", quotechar='"')
        for registro in csvReader:
            if registro[0] != str(id):
                csvWriter.writerow(registro)
        fichero_old.close()
        fichero.close()

        os.remove(MOVIMIENTOS_FILE)
        os.rename("data/movimientos_nuevos.txt", MOVIMIENTOS_FILE)

        return redirect(url_for("index"))

