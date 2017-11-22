from flask import Flask
from app.database import Base, Session
#Get Base db class, session here from DB.

app = Flask(__name__)



@app.route("/")
def hello_world():
    return "Hello World"

