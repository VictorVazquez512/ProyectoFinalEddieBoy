from flask import Flask, render_template, request, session
from werkzeug.utils import redirect
import secrets
import json
app = Flask(__name__)
app.secret_key = secrets.token_hex(16)


#home page
@app.route("/")
def index(): #index o root o home page
    return render_template("index.html")


@app.route('/item',methods=['GET','POST'])
def item(): #item page
    return render_template('item.html',error=None)

if __name__ == "__main__":
    app.run(debug =True, port=8000 )