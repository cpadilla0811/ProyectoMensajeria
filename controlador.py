import sqlite3

def ver_enviados(correo):
    db = sqlite3.connect("mensajeria.db")
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    consulta ="select m.asunto,m.cuerpodelmensaje,m.fecha,m.hora,u.usuario from usuarios u, mensajeria m  where u.correo=m.idusuariorecibe and m.idusuarioenvia='"+correo+"'order by fecha desc, hora desc"
    cursor.execute(consulta)
    resultado = cursor.fetchall()
    return resultado

def ver_recibidos(correo):
    db = sqlite3.connect("mensajeria.db")
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    consulta ="select m.asunto,m.cuerpodelmensaje,m.fecha,m.hora,u.usuario from usuarios u, mensajeria m  where u.correo=m.idusuarioenvia and m.idusuariorecibe='"+correo+"'order by fecha desc, hora desc"
    cursor.execute(consulta)
    resultado = cursor.fetchall()
    return resultado

def validar_usuario(usuario, password):
    db = sqlite3.connect("mensajeria.db")
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    consulta = "select * from usuarios where correo='"+usuario+"' and password='"+password+"' and estado='1'"
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

def actualizar_pass(password,correo):
    db = sqlite3.connect("mensajeria.db")
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    consulta = "update usuarios set password='"+password+"' where correo='"+correo+"'"
    cursor.execute(consulta)
    db.commit()
    return "1"

def registrar_mail(origen, destino, asunto, mensaje):
    db = sqlite3.connect("mensajeria.db")
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    consulta = "insert into mensajeria (asunto,cuerpodelmensaje,fecha,hora,idusuarioenvia,idusuariorecibe,estado) values ('"+asunto+"', '"+mensaje+"',DATE('now'),TIME('now'),'"+origen+"','"+destino+"','0')"
    cursor.execute(consulta)
    db.commit()
    return "1"


def registrar_usuario(usuario, correo, password, codigo):
    try:
        db = sqlite3.connect("mensajeria.db")
        db.row_factory = sqlite3.Row
        cursor = db.cursor()
        consulta = "insert into usuarios (usuario, correo, password, estado, codigoactivacion) values ('"+usuario+"', '"+correo+"', '"+password+"', '0', '"+codigo+"');"
        cursor.execute(consulta)
        db.commit()
        return "Usuario registrado satisfactoriamente"
    except:
        return "¡¡ERROR!! Este USUARIO y/o CORREO ya existen. Intente nuevamente"


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
