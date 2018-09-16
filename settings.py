from flask import Flask

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = r'sqlite:///D:\PycharmProjects\Flask_Python\database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False