from flask import Flask, render_template, request, redirect, make_response
from flask_sqlalchemy import SQLAlchemy
from models import User
import json
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "super_secret_random_string"
db = SQLAlchemy(app)
csrf = CSRFProtect(app)

def check_login(login):
    pass

def check_name(full_name):
    pass

def check_password(password): 
    
    if len(password) < 5 or len(password) > 50: 
        return "Длина пароля должна быть не меньше 5 символов но и не больше 50."

    digit = False
    upper_letter = False
    lower_letter = False
    symbol = False

    for char in password:
        if not char.isdigit() and not char.isalpha():
            symbol = True

        elif char.isdigit():
            digit = True
        
        else:
            if char.isupper():
                upper_letter = True
            else:
                lower_letter = True
    
    if digit and upper_letter and lower_letter and symbol :
        return False
    
    return "Пароль должен содержать строчные и заглавные буквы, цыфры и хотя бы один специальный символ."

@app.route("/")
def first():

    return render_template("start.html")

@app.route("/pre_signin")
def pre_signin():

    return render_template("start.html")

@app.route("/reg", methods = ["POST"])
def reg():

    full_name = request.get_json().get('f')
    login = request.get_json().get('l')
    password = request.get_json().get('p')
    
    if full_name and login and password :
        
        if User.query.filter(User.login == login).first():
            return make_response({"message" : "Такой логин уже существует.", "status" : "1"})
        
        if not check_login(login):
            pass
        
        if not check_name(full_name):
            pass
        
        if check_password(password):
            return make_response({"message" : check_password(password), "status" : "1"})
        
        return make_response({"message" : "Вы успешно зарегистрированы.", "status" : "0"})
    else:
        return make_response({"message" : "Все поля обязательны для ввода.", "status" : "1"})
    return render_template("start.html")

@app.route("/signin")
def signin():

    return render_template("start.html")


if __name__ == "__main__":
	app.run(debug=True)