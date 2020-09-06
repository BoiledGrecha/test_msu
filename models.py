from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key = True)
    full_name = db.Column(db.String)
    login = db.Column(db.String)
    password = db.Column(db.String)
    
# Clear db

# User.query.delete()
# db.session.commit()


# Initialize db

# db.create_all()