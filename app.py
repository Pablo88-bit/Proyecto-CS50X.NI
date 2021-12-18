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
from werkzeug.utils import send_from_directory
from PIL import Image
from glob import glob
import os
from cs50 import SQL
from helpers import login_required


app = Flask(__name__)#Creando un objeto de tipo flask llamado app
db = SQL("sqlite:///BaseDatos.db")#Creando un objeto de tipo SQL llamado db
UPLOAD_FOLDER = "./static/img/"#Creando la ruta donde se guardaran las imagenes en mi servidor
# ALLOWED_EXTENSIONS = {'.jpg', '.png'}
#configuraciones Session#
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
Session(app)


#Decoradores#
#Ruta Index#
@app.route('/')
@login_required
def index():
    return render_template("index.html")

@app.route('/info')
@login_required
def info():
    return render_template("info.html")

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
@app.route('/login', methods=["GET", "POST"])
def login():

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

#Ruta Salir#
@app.route('/salir')
@login_required
def salir():
    session.clear()
    return redirect("/login")

#Ruta convertir#
@app.route('/convertir', methods=["GET", "POST"])
@login_required
def convertir():
    if request.method == "POST":
        if "archivo" not in request.files:
            return redirect("/convertir")

        archivo = request.files['archivo']
        nuevo_formato = request.form.get("formato2")

        if archivo.filename == "":
            return redirect("/convertir")

        if archivo:
            nombreArchivo = archivo.filename
            archivo.save(os.path.join(app.config["UPLOAD_FOLDER"], nombreArchivo))

            nueva_extension = nuevo_formato if nuevo_formato != "jpeg" else "jpg"
            nuevo_nombre = ".".join(nombreArchivo.split(sep=".")[:-1]) + "." + nueva_extension
            
            im = Image.open(os.path.join(app.config["UPLOAD_FOLDER"], nombreArchivo)).convert("RGB")
            im.save(os.path.join(app.config["UPLOAD_FOLDER"], nuevo_nombre), nuevo_formato)
            return redirect("/descarga/" + nuevo_nombre)
        else:
            return redirect("/convertir")
    else: 
        return render_template("convertir.html")

@app.route("/upload", methods=['POST'])
@login_required
def upload():
    archivo = request.files['archivo']
    nombreArchivo = archivo.filename
    archivo.save(os.path.join(app.config["UPLOAD_FOLDER"], nombreArchivo))
    return "success"
    

@app.route("/descarga/<path:filename>", methods=['GET', 'POST'])
@login_required
def descarga(filename):
    descarga = os.path.join(app.config["UPLOAD_FOLDER"])
    return send_from_directory(descarga, filename,environ=request.environ, as_attachment=True)


#Si esta en el archivo principal vamos a ejecutar nuestra app
if __name__ == '__main__':
    app.run(debug=True, port = 5000)#Activamos el modo de depuración y el puerto donde deseo que se ejecute
    #El modo de depuración ayuda a que cualquier cambio que se haga se vea reflejado en la página

##Luego de terminar todo debo intaciar mi aplicacion FLASK: export FLASK_APP=app.py \nflask run
