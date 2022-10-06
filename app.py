from asyncio.windows_events import NULL
import datetime
from flask import Flask, render_template, request, session
from werkzeug.utils import redirect
from flask_mysqldb import MySQL
import secrets
import json
app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'db_nara'

mysql = MySQL(app)

# ----------- FUNCIONES --------------
def cursor():
    cur = mysql.connection.cursor()
    return cur


# ------------- ROUTES ---------------

#home page
@app.route("/")
def index(): #index o root o home page
    return render_template("index.html")

# not founded page
@app.route('/item',methods=['GET','POST'])
def item(): #item page
    return render_template('item.html',error=None)

@app.route('/registro_producto', methods=['GET','POST'])
def registro_producto():
    if request.method == 'POST':
        nombre = request.form['nombre']
        sku = request.form['sku']
        descripcion = request.form['descripcion']
        stock = request.form['stock']
        precio = request.form['precio']
        imagen = request.files['imagen']

        cur = cursor()
        cur.execute('''INSERT INTO producto(nombre, sku, descripcion, stock, precio, imagen) VALUES ("%s", "%s", "%s", "%s", "%s", "%s")'''%(nombre, sku, descripcion, stock, precio, imagen))
        mysql.connection.commit()
        cur.close()

        return redirect('/')
    else:
        return render_template('registro_producto.html')


# ------------- Sistema de Usuarios -------------

@app.route('/registro_cliente',methods=["GET","POST"])
def registro():
    error=None
    if request.method=='POST':
        # Establecemos conexion con la base de datos
        cur = cursor()
        print(request.form)

        # Tratamos el formulario que viene del cliente
        email=request.form['email']
        password=request.form['password']
        confirmarpassword=request.form['ConfirmPassword']
        # Verificar si existe el email
        cur.execute('''SELECT * FROM usuario WHERE pass="%s" AND email="%s"'''%(password, email))
        usuario = cur.fetchone()
        print(cur)
        print(usuario)
        if usuario == NULL:
            return render_template('/registro_cliente.html',error="El correo electronico ya existe.")
        if password!=confirmarpassword:
            return render_template('/registro_cliente.html', error="Las passwords no coinciden")
        else:
            cur.execute('''INSERT INTO usuario(email, pass, tipo) VALUES ("%s", "%s", "cliente")'''%(email, password))
            cur.execute('''SELECT * FROM usuario WHERE pass="%s" AND email="%s"'''%(password, email))
            usuario = cur.fetchone()
            session['idUsuario'] = usuario[0]
            session['email'] = usuario[1]

            mysql.connection.commit()
            cur.close()

            return redirect('/')
    else:
        return render_template('/registro_cliente.html')


@app.route('/login',methods=["GET","POST"])
def login():
    error=None
    if request.method == 'POST':
        # extraemos los datos del formulario del request
        email=request.form['email']
        password=request.form['password']

        # corroboramos si el email y el password no estan vacios
        if email=="" or password=="":
            return render_template('login.html',error="Ingresa un correo y/o una contraseña")
        
        # hacemos conexion a la base de datos y recuperamos al usuario para ver si existe
        cur = cursor()
        cur.execute('''SELECT * FROM usuario WHERE pass="%s" AND email="%s"'''%(password, email))
        usuario = cur.fetchone()
        cur.close()

        print("-------------------- USUARIO ---------------")
        print(usuario)
        
        if usuario == None:
            print('entramo al correo invalido pippin')
            return render_template('login.html',error="Correo o contraseña invalidos")
        elif (email in usuario):
            if (password == usuario[2]):
                print('si entramos al bellaqueo pippin')
                session['email']=email
                session['idUsuario']=usuario[0]
                session['tipo']=usuario[3]
                return redirect('/')
            else:
                return render_template('login.html',error="Correo o password contraseña")     
        else:
            return render_template('login.html',error="Correo o password contraseña")
    return render_template('login.html')


@app.errorhandler(404)
def page_not_found(errorhandler):
    return render_template("notfound.html"), 404

if __name__ == "__main__":
    app.run(debug =True, port=8000)