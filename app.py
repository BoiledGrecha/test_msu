from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from models import *
from random import shuffle
import json
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "super_secret_random_string"
db = SQLAlchemy(app)
csrf = CSRFProtect(app)

@app.route("/")
def first():
    return render_template("start.html")

if __name__ == "__main__":
	app.run(debug=True)