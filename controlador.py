import sqlite3


def validar_usuario(usuario, password):
    db = sqlite3.connect("mensajeria.db")
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    consulta = "select * from usuarios where correo='" + \
        usuario+"' and password='"+password+"' and estado='1'"
    cursor.execute(consulta)
    resultado = cursor.fetchall()
    return resultado


def ver_enviados(correo):
    db = sqlite3.connect("mensajeria.db")
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    consulta = "select m.asunto,m.mensaje,m.fecha,m.hora,u.nombreusuario from usuarios u, mensajeria m where u.correo=m.id_usu_recibe and m.is_usu_envia='"+correo+"' order by fecha desc, fecha desc"
    cursor.execute(consulta)
    resultado = cursor.fetchall()
    return resultado


def lista_destinatarios(usuario):
    db = sqlite3.connect("mensajeria.db")
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    consulta = "select * from usuarios where correo<>'"+usuario+"' "
    cursor.execute(consulta)
    resultado = cursor.fetchall()
    return resultado


def registrar_mail(origen, destino, asunto, mensaje):
    db = sqlite3.connect("mensajeria.db")
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    consulta = "insert into mensajeria (asunto, mensaje, fecha, hora, id_usu_envia, id_usu_recibe, estado) values ('" + \
        asunto+"', '"+mensaje + \
        "', DATE('now'), TIME('now'), '"+origen+"','"+destino+"','0');"
    cursor.execute(consulta)
    db.commit()
    return "1"


def registrar_usuario(usuario, correo, password, codigo):
    db = sqlite3.connect("mensajeria.db")
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    consulta = "insert into usuarios (usuario, correo, password, estado, codigoactivacion) values ('" + \
        usuario+"', '"+correo+"', '"+password+"', '0', '"+codigo+"');"
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
