from flask import Flask, render_template, request, redirect, make_response, url_for
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
    
    if len(login) > 20 or len(login) < 5:
        return "Логин не может содержать меньше 5 и больше 20 символов"

    return False

def check_name(full_name):
    
    if len(full_name) > 150:
        return "ФИО не может быть длиннее 150 символов"

    for char in full_name:

        if (not char.isdigit() and not char.isalpha() and
            char not in [".", "-", " "]):
            return "ФИО не может содержать спец символы кроме \".\", \"-\", \" \"."

    return False

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
    # проверка на куки и редирект и сделать отдельную страничку убийцу куки
    login = request.cookies.get("login")
    password = request.cookies.get("password")
    result = make_response(render_template("start.html"))

    if (login and password):
        user = User.query.filter(User.login == login).first()
        if user and user.password == password:
            return redirect("https://ya.ru/")
        else:
            result.set_cookie("login", "", 0)
            result.set_cookie("password", "", 0)

    return result

@app.route("/signin", methods = ["POST"])
def signin():
    
    if not request.form.get("login") or not request.form.get("password"):
        return render_template("error.html")

    user = User.query.filter(User.login == request.form["login"]).first()
    
    if user and check_password_hash(user.password, request.form["password"]):

        result = make_response(redirect("https://ya.ru/"))
        result.set_cookie("login",
            request.form["login"], 
            60 * 60 * 24)
        result.set_cookie("password",
            user.password,
            60 * 60 * 24)
        
        return result

    print(user.password)
    print(generate_password_hash(request.form["password"]))
    print(request.form["password"])

    return render_template("error.html")

@app.route("/reg", methods = ["POST"])
def reg():

    full_name = request.get_json().get('f')
    login = request.get_json().get('l')
    password = request.get_json().get('p')
    
    if full_name and login and password :
        
        if User.query.filter(User.login == login).first():
            return make_response({"message" : "Такой логин уже существует.", "status" : "1"})
        
        if check_login(login):
            return make_response({"message" : check_login(login), "status" : "1"})
        
        if check_name(full_name):
            return make_response({"message" : check_name(full_name), "status" : "1"})
        
        if check_password(password):
            return make_response({"message" : check_password(password), "status" : "1"})
        
        try:
            print(password)
            user = User(full_name = full_name, login = login,
                password = generate_password_hash(password))
            db.session.add(user)
            db.session.commit()
        except:
            return make_response({"message" : "Возникла ошибка при записи в БД.",
                "status" : "1"})
        
        return make_response({"message" : "Вы успешно зарегистрированы.", "status" : "0"})
    else:
        return make_response({"message" : "Все поля обязательны для ввода.", "status" : "1"})

@app.route("/pre_signin", methods = ["POST"])
def pre_signin():
    
    login = request.get_json().get('l')
    password = request.get_json().get('p')
    
    if not login and not password:
        return make_response({"message" : "Заполните оба поля.", "status" : "1"})

    user = User.query.filter(User.login == login).first()
    if not user:
        return make_response({"message" : "Данный пользователь не существует ",
            "status" : "1"})
    if not check_password_hash(user.password, password):
        return make_response({"message" : "Неправильный пароль", "status" : "1"})

    return make_response({"message" : "Успешно", "status" : "0"})

@app.route("/kill_cookie")
def kill_coockie():

    result = make_response(render_template("start.html"))
    result.set_cookie("login", "", 0)
    result.set_cookie("password", "", 0)
    return result

if __name__ == "__main__":
	app.run(debug=False)