from base64 import b64encode, b64decode
import datetime
#from crypt import methods

from flask import Flask, render_template, request, session, url_for
from werkzeug.utils import redirect
from flask_mysqldb import MySQL
import secrets
import json
app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# mamalona del heroku
app.config['MYSQL_HOST'] = 'us-cdbr-east-06.cleardb.net'
app.config['MYSQL_USER'] = 'b7e3a09e061e12'
app.config['MYSQL_PASSWORD'] = '2f9d3cc1'
app.config['MYSQL_DB'] = 'heroku_d02c1597b242410'

app.config['MAX_CONTENT_LENGTH'] = 8 * 1024 * 1024
mysql = MySQL(app)

# ----------- FUNCIONES --------------
def cursor():
    cur = mysql.connection.cursor()
    return cur


# ------------- ROUTES ---------------

#home page
@app.route("/", methods=['GET','POST'])
def index():
    # Recabamos lista de productos
    cur = cursor()
    nombreC=""
    if 'nombreCliente' in session:
        print(session['nombreCliente'])
        nombreC = session['nombreCliente']
        pass
    cur.execute('''SELECT * FROM producto LIMIT 16''')
    lista_articulos_tupla = cur.fetchall()
    lista_articulos = []
    #print(lista_articulos_tupla)
    for articulo in lista_articulos_tupla:
        lista_articulos.append(list(articulo))
    #for articulo in lista_articulos:
    #    articulo[6] = b64encode(articulo[6])
    #print(lista_articulos)
    if request.method == 'POST':
        if 'nombreCliente' in session:
            print('carrito')
            return render_template('cart.html')
        else:
            return redirect('/')
    return render_template("index.html", lista_articulos = lista_articulos, nombre = nombreC)

@app.route("/searcher/<producto>", methods = ["GET", "POST"])
def buscador(prod):
    cur = cursor ()
    query = "SELECT * FROM producto WHERE nombre LIKE %s AND descripcion LIKE %s"
    val = (prod, prod)
    cur.execute(query, val)
    lista_articulo_tupla = cur.fetchall()
    lista_articulos = []
    print(lista_articulo_tupla)
    for a in lista_articulo_tupla:
        lista_articulos.append(list(a))
    print(lista_articulos)
    return render_template("index.html", lista = lista_articulos)
@app.route("/admin")
def admin():
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM producto')
        data = cur.fetchall()
        return render_template("admin.html", data = data)

    # TODO pagina para cambiar permisos de usuarios
    # TODO
@app.route("/admin/mod_prod/<id>", methods=["GET", "POST"])
def mod_prod(id):
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM producto WHERE idProducto = '" + id + "'")
        data = cur.fetchall()
        return render_template("mod_productos.html", data = data)
@app.route("/admin/mod_prod", methods = ["POST"])
def mod_produ():
    if request.method == 'POST':
        a = request.form['nombre']
        b = request.form['sku']
        c = request.form['descripcion']
        d = request.form['stock']
        e = request.form['precio']
        f = request.files['imagen'].read()
        g = request.form['id']
        imagen = b64encode(f)
        print(a,b,c,d,e,g)
        #query = "UPDATE productos SET nombre ='" + a + "', sku = '" + b + "', descripcion = '" + c + "', stock = '" + d + "', precio = '" + e + "', imagen = '" + imagen.decode() + "WHERE idProducto = '" + g + "'"
        #query = "UPDATE productos SET nombre ='%s' , sku = '%s', descripcion = '%s', stock = '%s', precio = '%s', imagen = '%s' WHERE ID = %s" ,{a,b,c,d,e,imagen,g}
        #query2 = 'UPDATE `heroku_d02c1597b242410`.`producto` SET `nombre` = %s, `sku` = %s, `descripcion` = %s, `stock` = %s, `precio` = %s WHERE `idProducto` = %s',(a,b,c,d,e,g)
        # TODO: fixear el tuneo del archivo
        query = "UPDATE producto SET nombre = %s, sku = %s, descripcion = %s, stock = %s, precio = %s, imagen = %s WHERE idProducto = %s"
        val = (a,b,c,d,e,imagen,g)
        print(query)
        cur = mysql.connection.cursor()
        cur.execute(query,val)
        mysql.connection.commit()
        return redirect(url_for('/admin'))

@app.route('/admin/usuarios', methods=['GET', 'POST'])
def usuarios():
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM usuario WHERE tipo = 'cliente'"
    cursor.execute(query)
    clientes = cursor.fetchall()
    query = "SELECT * FROM usuario WHERE tipo = 'admin'"
    cursor.execute(query)
    admin = cursor.fetchall()
    return render_template("users.html", regular = clientes, admin = admin)
@app.route("/admin/prom/<id>")
def admin_prom(id):
    cursor = mysql.connection.cursor()
    query = "UPDATE usuario SET tipo = %s WHERE idUsuario = %s"
    val = ("admin", id)
    cursor.execute(query, val)
    mysql.connection.commit()
    return redirect(url_for('/admin/usuarios'))
@app.route("/admin/demo/<id>")
def demot_prom(id):
    cursor = mysql.connection.cursor()
    query = "UPDATE usuario SET tipo = %s WHERE idUsuario = %s"
    val = ("cliente",id)
    cursor.execute(query, val)
    mysql.connection.commit()
    return redirect(url_for('/admin/usuarios'))
@app.route("/admin/elim/<id>")
def elim_user(id):
    cursor = mysql.connection.cursor()
    query = "DELETE FROM usuario WHERE idUsuario = %s"
    val = (id)
    cursor.execute(query, val)
    mysql.connection.commit()
    return redirect(url_for('/admin/usuarios'))
@app.route('/admin/del_prod/<id>', methods =["GET","POST"])
def del_prod(id):
    query = "DELETE FROM productos WHERE idProducto = '" + id + "'"
    cur = mysql.connection.cursor()
    cur.execute(query)
    mysql.connection.commit()
    # codigo de schrodinger, puede que jale, puede que no
    return redirect(url_for('/admin'))

@app.route('/item/<id>',methods=['GET','POST'])
def item(id): #item page
    cur = mysql.connection.cursor()
    query = "SELECT * FROM producto WHERE idProducto = %s"
    val = (id)
    cur.execute(query,val)
    data = cur.fetchall()

    query = "SELECT * FROM producto LIMIT 4"
    cur.execute(query)
    reData = cur.fetchall()

    return render_template('item.html', error=None, data = data, related = reData)

@app.route('/registro_producto', methods=['GET','POST'])
def registro_producto():
    if request.method == 'POST':
        nombre = request.form['nombre']
        sku = request.form['sku']
        descripcion = request.form['descripcion']
        stock = request.form['stock']
        precio = request.form['precio']
        imagen = request.files['imagen'].read()
        imagenb64 = b64encode(imagen)
        cur = cursor()
        cur.execute('INSERT INTO producto(nombre, sku, descripcion, stock, precio, imagen) VALUES (%s, %s, %s, %s, %s, %s)', (nombre, sku, descripcion, stock, precio, imagenb64))
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
        nombre=request.form['name']
        apellido=request.form['lastName']
        direccion=request.form['adress']
        ciudad = request.form['city']
        estado = request.form['state']
        codigoPostal = request.form['zipCode']
        numCel = request.form['phoneNumber']
        email=request.form['email']
        password=request.form['password']
        confirmarpassword=request.form['ConfirmPassword']
        idC=0
        # Verificar si existe el email
        cur.execute('''SELECT * FROM usuario WHERE pass="%s" AND email="%s"'''%(password, email))
        usuario = cur.fetchone()
        print(cur)
        print(usuario)
        if usuario != None:
            return render_template('/registro_cliente.html', error="El correo electronico ya existe.")
        if password!=confirmarpassword:
            return render_template('/registro_cliente.html', error="Las passwords no coinciden")
        else:
            cur.execute('''INSERT INTO usuario(email, pass) VALUES ("%s", "%s")'''%(email, password))
            cur.execute('''SELECT max(id) from clientes''')
            idcliente=cur.fetchone()
            print(idcliente)
            if idcliente[0]==None:
                idC = 0
            else:
                idC = idcliente[0]+1
                
            cur.execute('''INSERT INTO clientes(id,nombre,apellido,direccion,ciudad,estado,codigoPost,numCel,email) VALUES(%s,"%s","%s","%s","%s","%s","%s",%s,"%s")'''%(idC,nombre,apellido,direccion,ciudad,estado,codigoPostal,numCel,email))
            # borre lo del tipo, la db ya tiene por default agregar users como clientes para no andar batallando
            cur.execute('''SELECT * FROM usuario WHERE pass="%s" AND email="%s"'''%(password, email))
            usuario = cur.fetchone()
            session['idUsuario'] = usuario[0]
            session['email'] = usuario[1]
            cur.execute('''SELECT * FROM clientes WHERE email="%s"'''%(session['email']))
            session['nombreCliente']=cur.fetchone()[8]
            print(session['nombreCliente'])
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
                cur=cursor()
                cur.execute('''SELECT * FROM clientes where email="%s"'''%(email))
                session['nombreCliente']=cur.fetchone()[1]
                cur.close()
                if usuario[3] == 'admin':
                    return redirect('/admin')
                return redirect('/')
            else:
                return render_template('login.html',error="Correo o password contraseña")     
        else:
            return render_template('login.html',error="Correo o password contraseña")
    return render_template('login.html')

@app.route("/logout")
def logout():
    error=None
    session.pop("nombreCliente")
    return redirect('/')

#-------------CARRITO-----------------
@app.route('/carrito',methods=["GET","POST"])
def carrito():
    error=None
    

@app.errorhandler(404)
def page_not_found(errorhandler):
    return render_template("notfound.html"), 404

if __name__ == "__main__":
    app.run(debug =True, port=8000)