
from flask import render_template, request, redirect
import csv
from registro_ig import app
from datetime import date

@app.route("/")
def index():
    fichero = open("data/movimientos.txt", "r")
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
            fichero = open("data/movimientos.txt", "a", newline = "")
            csvWriter = csv.writer(fichero, delimiter=",", quotechar='"')
            # Generar un nuevo id
            csvWriter.writerow([request.form["date"], request.form["concept"], request.form["quantity"]])
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
    else:
        """
        borrar el registro
        """
        pass