#Importo la librería Flask que es el framework que utilizare para hacer mi pág
from flask import Flask
from flask import render_template
from flask import redirect
from flask import url_for
from flask import session
from flask import request
from flask import flash
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from cs50 import SQL


app = Flask(__name__)#Creando un objeto de tipo flask llamado app
db = SQL("sqlite:///BaseDatos.db")#Creando un objeto de tipo SQL llamado db

#configuraciones Session#
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
Session(app)


#Decoradores#


#Ruta Index#
@app.route('/home')
@app.route('/')
def index():
    return render_template("index.html")

#Ruta Nosotros#
@app.route('/Nosotros')
def Nosotros():
    return render_template("Nosotros.html")

#Ruta Contacto#
@app.route('/Contacto')
def Contacto():
    return render_template("Contacto.html")

#Ruta register#
@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":

        #Asegurar envio del nombre de usuario#
        if not request.form.get("username"):
            flash("Ingrese un usuario")
            return render_template("register.html")

        #Asegurar envio de la contraseña#
        elif not request.form.get("password"):
            flash("Ingrese una contraseña")
            return render_template("register.html")

        #Asegurar envio del nombre de usuario#
        elif request.form.get("password") != request.form.get("confirmation"):
            flash("Las contraseñas no coinciden")
            return render_template("register.html")


        #Guarda Datos#
        usuario = request.form.get("username")
        contraseña = request.form.get("password")

        #Registrar nuevo usuario en la Base de datos#
        resultado = db.execute("INSERT INTO user (username, password) \
                                Values (:username, :password)",
                                username=usuario, password=generate_password_hash(contraseña))#Esta función encripta la contraseña del usuario#

        #Verifica si el usuario ya existe#
        if not resultado:
            flash("El usuario ya existe")
            return render_template("register.html")


        #Almacenando en la session#
        session["user_id"] = resultado;

        return redirect("/")

    else:
        return render_template("register.html")


#Ruta Login#
@app.route('/Login', methods=["GET", "POST"])
def Login():

    if request.method == "POST":

        #Asegurar envio username#
        if not request.form.get("username"):
            flash("Ingrese un usuario")
            return render_template("Login.html")

        #Asegurar envio del password#
        elif not request.form.get("password"):
            flash("Ingrese una contraseña")
            return render_template("Login.html")

        user = request.form.get("username")
        contra = request.form.get("password")

        #Consultar la base de datos#
        rows = db.execute("SELECT * FROM user WHERE username = :username", username = user)

        #Validar usuario y contraseña#
        if len(rows) != 1 or not check_password_hash(rows[0]["password"], contra):
            flash("Usuario o contraseña incorrecta")
            return render_template("Login.html")

        #Recordar al usuario ingresado o guardar el usuario en la session#
        session["user_id"] = rows[0]["user_id"]

        #Al inicio#
        return redirect("/")
    else:
        return render_template("Login.html")


#Si esta en el archivo principal vamos a ejecutar nuestra app
if __name__ == '__main__':
    app.run(debug = true, port = 5000)#Activamos el modo de depuración y el puerto donde deseo que se ejecute
    #El modo de depuración ayuda a que cualquier cambio que se haga se vea reflejado en la página

##Luego de terminar todo debo intaciar mi aplicacion FLASK: export FLASK_APP=app.py \nflask run
