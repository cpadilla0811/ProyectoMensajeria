import sqlite3

def validar_usuario(usuario, password):
    db = sqlite3.connect("mensajeria.db")
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    consulta = "select * from usuarios where correo='"+usuario+"' and password='"+password+"' and estado='1'"
    cursor.execute(consulta)
    resultado = cursor.fetchall()
    return resultado


def registrar_usuario(usuario, correo, password, codigo):
    db = sqlite3.connect("mensajeria.db")
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    consulta = "insert into usuarios (usuario, correo, password, estado, codigoactivacion) values ('"+usuario+"', '"+correo+"', '"+password+"', '0', '"+codigo+"');"
    cursor.execute(consulta)
    db.commit()
    return "1"


def activar_usuario(codigo):
    db = sqlite3.connect("mensajeria.db")
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    consulta = "update usuarios set estado='1' where codigoactivacion='"+codigo+"'"
    cursor.execute(consulta)
    db.commit()

    consulta2 = "select * from usuarios where codigoactivacion='"+codigo+"' and estado='1'"
    cursor.execute(consulta2)
    resultado = cursor.fetchall()
    return resultado
