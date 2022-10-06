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

#login
@app.route('/login')
def login():
    return render_template('login.html')

# not founded page
@app.route('/item',methods=['GET','POST'])
def item(): #item page
    return render_template('item.html',error=None)

@app.route('/registerProduct', methods=['GET','POST'])
def product():
    if request.method == 'GET':
        return render_template('register_roducts.html')

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
        contraseña=request.form['password']
        confirmarContraseña=request.form['ConfirmPassword']
        # Verificar si existe el email
        cur.execute('''SELECT * FROM usuario WHERE contraseña="%s" AND email="%s"'''%(contraseña, email))
        row = cur.fetchone()
        print(cur)
        print(row)
        if row == NULL:
            return render_template('/registro_cliente.html',error="El correo electronico ya existe.")
        if contraseña!=confirmarContraseña:
            return render_template('/registro_cliente.html', error="Las contraseñas no coinciden")
        else:
            cur.execute('''INSERT INTO usuario(email, contraseña, tipo) VALUES ("%s", "%s", "cliente")'''%(email, contraseña))
            cur.execute('''SELECT * FROM usuario WHERE contraseña="%s" AND email="%s"'''%(contraseña, email))
            usuario = cur.fetchone()
            session['idUsuario'] = usuario[0]
            session['email'] = usuario[1]

            mysql.connection.commit()
            cur.close()

            return redirect('/')
    else:
        return render_template('/registro_cliente.html')

# @app.route('/login',methods=["GET","POST"])
# def login():
#     error=None
#     if request.method == 'POST':
#         email=request.form['correo']
#         password=request.form['password']
        
#         row=bdEcommerce.buscarUnaLinea("usuario","email",email)
        
#         if email=="" or password=="":
#             return render_template('login.html',error="Ingresa un correo y/o una contraseña")
#         if len(row)==0:
#             return render_template('login.html',error="Correo invalido")
#         if (email in row[0]):
#             if (password == row[0][2]):
#                 session['email']=email
#                 session['idUsuario']=row[0][0]
#                 session['tipo']=row[0][3]
#                 return redirect('/')
#             else:
#                 return render_template('login.html',error="Correo o contraseña incorrectos")     
#         else:
#             return render_template('login.html',error="Correo o contraseña incorrectos")
#     return render_template('login.html')


@app.errorhandler(404)
def page_not_found(errorhandler):
    return render_template("notfound.html"), 404

if __name__ == "__main__":
    app.run(debug =True, port=8000)