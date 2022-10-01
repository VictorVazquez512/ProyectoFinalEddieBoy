from flask import Flask, render_template, request, session
from werkzeug.utils import redirect
from flask_mysqldb import MySQL
import secrets
import json
app = Flask(__name__)
app.secret_key = secrets.token_hex(16)


#home page
@app.route("/")
def index(): #index o root o home page
    return render_template("index.html")

#login
@app.route('/login')
def login():
    return render_template('login.html')

#formsignup
@app.route('/formsignup')
def register():
    return render_template('formsignup.html')

# not founded page

@app.route('/item',methods=['GET','POST'])
def item(): #item page
    return render_template('item.html',error=None)


@app.errorhandler(404)
def page_not_found(errorhandler):
    return render_template("notfound.html"), 404

if __name__ == "__main__":
    app.run(debug =True, port=8000 )