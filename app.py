from flask import Flask, render_template, request
import hashlib
import controlador
from datetime import datetime
import envioemail

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("login.html")

@app.route("/validarUsuario", methods=["GET","POST"])
def validarUsuario():
    if request.method=="POST":
        usu = request.form["txtusuario"]
        pasw = request.form["txtpass"]
        pasw2 = pasw.encode()
        pasw2 = hashlib.sha384(pasw2).hexdigest()
        print(usu, pasw, pasw2)
        respuesta = controlador.validar_usuario(usu, pasw2)                      
        if len(respuesta) == 0:
            mensaje = "ERROR DE AUTENTICACIÓN! Lo invitamos a validar su usuario y contraseña"
            return render_template("informacion.html", datas = mensaje)       
        else:
            return render_template("principal.html")

@app.route("/registrarUsuario", methods=["GET","POST"])
def registrarUsuario():
        name = request.form["txtnombre"]
        email = request.form["txtusuarioregistro"]
        pasw = request.form["txtpassregistro"]
        pasw2 = pasw.encode()
        pasw2 = hashlib.sha384(pasw2).hexdigest()

        codigo=datetime.now()
        codigo2=str(codigo)
        codigo2=codigo2.replace("-","")
        codigo2=codigo2.replace(" ","")
        codigo2=codigo2.replace(":","")
        codigo2=codigo2.replace(".","")

        print(codigo2)

        mensaje="Sr, usuario su codigo de activacion es :\n\n"+codigo2+ "\n\n Recuerde copiarlo y pegarlo para validarlo en la seccion de login y activar su cuenta.\n\nMuchas Gracias"

        envioemail.enviar(email, mensaje)

        respuesta = controlador.registrar_usuario(name, email, pasw2, codigo2)
        mensaje = "El usuario "+ name + " se ha registrado correctamente"
        return render_template("informacion.html", datas = mensaje)    


@app.route("/activarUsuario", methods=["GET","POST"])
def activarUsuario():
        codigo = request.form["txtcodigo"]
        

        respuesta = controlador.activar_usuario(codigo)

        if len(respuesta)==0:
            mensaje = "El codigo de activacion es errone, verifiquelo."
        else:
            mensaje = "El usuario se ha activado exitosamente."
        return render_template("informacion.html", datas = mensaje)          

