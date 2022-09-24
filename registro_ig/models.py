from config import MOVIMIENTOS_FILE, NEW_FILE, LAST_ID_FILE
import csv, os

def select_all():

    fichero = open(MOVIMIENTOS_FILE, "r")
    csvReader = csv.reader(fichero, delimiter=",", quotechar='"')
    movimientos = [movimiento for movimiento in csvReader]

    fichero.close()

    return movimientos

def select_by(id):
    
    fichero = open(MOVIMIENTOS_FILE, "r", newline="")
    csvReader = csv.reader(fichero, delimiter=",",quotechar='"')
    registro_definitivo = []
    for registro in csvReader:
        if registro[0] == str(id):
            registro_definitivo = registro
            break
        
    fichero.close()

    return registro_definitivo

def delete_by(id):
    
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
    os.rename(NEW_FILE, MOVIMIENTOS_FILE)

def createId():
    fichero = open(LAST_ID_FILE,"r")
    registro = fichero.read()
    id = int(registro) + 1
    fichero.close()

    return id

def saveLastId(id):
    fichero = open(LAST_ID_FILE, "w")
    fichero.write(str(id))
    fichero.close()

def insert(registro):
    
    id = createId()

    fichero = open(MOVIMIENTOS_FILE, "a", newline = "")
    csvWriter = csv.writer(fichero, delimiter=",", quotechar='"')
    
    # el siguiente comentario es lo mismo que lo de abajo
    # csvWriter.writerow(["{}".format(id), registro[0], registro[1], registro[2]])
    csvWriter.writerow([f"{id}"] + registro)
    fichero.close()

    saveLastId(id)

def updated_by(registro_mod):
    
    fichero_old = open(MOVIMIENTOS_FILE, "r")
    fichero = open(NEW_FILE, "w", newline="")
    csvReader = csv.reader(fichero_old, delimiter=",", quotechar='"')
    csvWriter = csv.writer(fichero, delimiter=",", quotechar='"')
    for registro in csvReader:
        if registro[0] != str(registro_mod[0]):
            csvWriter.writerow(registro)
        else:
            csvWriter.writerow(registro_mod)

    fichero_old.close()
    fichero.close()

    os.remove(MOVIMIENTOS_FILE)
    os.rename(NEW_FILE, MOVIMIENTOS_FILE)
    