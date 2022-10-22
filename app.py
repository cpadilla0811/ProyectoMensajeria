from flask import Flask, render_template, request
import hashlib
import controlador
from datetime import datetime
import envioemail

app = Flask(__name__)

email_origen = ""


@app.route("/")
def hello_world():
    return render_template("login.html")


@app.route("/validarUsuario", methods=["GET", "POST"])
def validarUsuario():
    if request.method=="POST":
        usu = request.form["txtusuario"]
        usu=usu.replace("SELECT","").replace("INSERT","").replace("DELETE","").replace("UPDATE","").replace("select","").replace("insert","").replace("update","").replace("delete","")
        pasw = request.form["txtpass"]
        pasw=pasw.replace("SELECT","").replace("INSERT","").replace("DELETE","").replace("UPDATE","").replace("select","").replace("insert","").replace("update","").replace("delete","")
        pasw2 = pasw.encode()
        pasw2 = hashlib.sha384(pasw2).hexdigest()
        #print(usu, pasw, pasw2)
        respuesta = controlador.validar_usuario(usu, pasw2)

        global email_origen

        if len(respuesta) == 0:
            email_origen = ""
            mensaje = "ERROR DE AUTENTICACIÓN! Lo invitamos a validar su usuario y contraseña"
            return render_template("informacion.html", datas=mensaje)
        else:
            email_origen = usu
            respuesta2 = controlador.lista_destinatarios(usu)
            return render_template("principal.html", datas=respuesta2, infousuario=respuesta)


@app.route("/registrarUsuario", methods=["GET", "POST"])
def registrarUsuario():
    if request.method=="POST":
        name = request.form["txtnombre"]
        name=name.replace("SELECT","").replace("INSERT","").replace("DELETE","").replace("UPDATE","").replace("select","").replace("insert","").replace("update","").replace("delete","")
        email = request.form["txtusuarioregistro"]
        email=email.replace("SELECT","").replace("INSERT","").replace("DELETE","").replace("UPDATE","").replace("select","").replace("insert","").replace("update","").replace("delete","")
        pasw = request.form["txtpassregistro"]
        pasw=pasw.replace("SELECT","").replace("INSERT","").replace("DELETE","").replace("UPDATE","").replace("select","").replace("insert","").replace("update","").replace("delete","")
        pasw2 = pasw.encode()
        pasw2 = hashlib.sha384(pasw2).hexdigest()

        codigo = datetime.now()
        codigo2 = str(codigo)
        codigo2 = codigo2.replace("-", "")
        codigo2 = codigo2.replace(" ", "")
        codigo2 = codigo2.replace(":", "")
        codigo2 = codigo2.replace(".", "")

        # print(codigo2)

        mensaje = "Sr "+name+", usuario su codigo de activacion es :\n\n"+codigo2 + \
            "\n\nRecuerde copiarlo y pegarlo para validarlo en la seccion de login y activar su cuenta.\n\nMuchas Gracias"

        respEmail = envioemail.enviar(email, mensaje, "Codigo de Activacion")

        respuesta = controlador.registrar_usuario(name, email, pasw2, codigo2)

        if respEmail=="0":
            respuesta = "El usuario se ha registrado correctamente. No fue posible enviar el correo electrónico, utilize el siguiente código de activación: "+codigo2
            
        #mensaje = "El usuario "+ name + " se ha registrado correctamente"
        return render_template("informacion.html", datas = respuesta)    


@app.route("/activarUsuario", methods=["GET", "POST"])
def activarUsuario():
    if request.method=="POST":
        codigo = request.form["txtcodigo"]
        codigo=codigo.replace("SELECT","").replace("INSERT","").replace("DELETE","").replace("UPDATE","").replace("select","").replace("insert","").replace("update","").replace("delete","")

        respuesta = controlador.activar_usuario(codigo)

        if len(respuesta) == 0:
            mensaje = "El codigo de activacion es erroneo, verifiquelo."
        else:
            mensaje = "El usuario se ha activado exitosamente."
        return render_template("informacion.html", datas=mensaje)


@app.route("/enviarmail", methods=["GET", "POST"])
def enviarmail():
    if request.method=="POST":
        emaildestino = request.form["emaildestino"]
        emaildestino=emaildestino.replace("SELECT","").replace("INSERT","").replace("DELETE","").replace("UPDATE","").replace("select","").replace("insert","").replace("update","").replace("delete","")
        asunto = request.form["asunto"]
        asunto=asunto.replace("SELECT","").replace("INSERT","").replace("DELETE","").replace("UPDATE","").replace("select","").replace("insert","").replace("update","").replace("delete","")
        mensaje = request.form["mensaje"]
        mensaje=mensaje.replace("SELECT","").replace("INSERT","").replace("DELETE","").replace("UPDATE","").replace("select","").replace("insert","").replace("update","").replace("delete","")
        controlador.registrar_mail(email_origen, emaildestino, asunto, mensaje)
        mensaje2 = "Sr usuario, usted recibió un mensaje nuevo, por favor ingrese a la plataforma para observar su email en la pestaña historial. \n\nMuchas gracias."

        envioemail.enviar(emaildestino, mensaje2, "Nuevo mensaje enviado")

        return "Email enviado satisfactoriamente"


@app.route("/HistorialEnviados", methods=["GET", "POST"])
def HistorialEnviados():
    if request.method=="POST":
        resultado=controlador.ver_enviados(email_origen)
        return render_template("respuesta.html", datas = resultado) 

@app.route("/HistorialRecibidos", methods=["GET","POST"])
def HistorialRecibidos():
    if request.method=="POST":
        resultado=controlador.ver_recibidos(email_origen)
        return render_template("respuesta2.html", datas = resultado) 

@app.route("/cambiopassword", methods=["GET","POST"])
def cambiopassword():
    if request.method=="POST":
        password = request.form["pass"]
        password=password.replace("SELECT","").replace("INSERT","").replace("DELETE","").replace("UPDATE","").replace("select","").replace("insert","").replace("update","").replace("delete","")
        passw2 = password.encode()
        passw2 = hashlib.sha384(passw2).hexdigest()

        controlador.actualizar_pass(passw2,email_origen)
        return "Actualización Satisfactoria"
