from flask import Flask, jsonify, abort, request, render_template
import json
from app.database import Base, Session, User, FoodDiaryEntry

app = Flask(__name__)

session = Session()

@app.route("/users/", methods=['POST'])
def create_user():
	password = request.form["password"]
	username = request.form["username"]
	new_user = User(name=username, password=password)
	session.add(new_user)
	session.commit()
	return ('', 204)


@app.route("/users/<user_name>", methods=['GET'])
def get_user(user_name):
	user = session.query(User).filter(User.name == user_name).first()
	return jsonify(user.to_response()) if user is not None else abort(404)

@app.route("/users", methods=['GET'])
def get_users():
	users = session.query(User).order_by(User.id)
	return jsonify([user.to_response() for user in users])

def food_diary_entries(user_name):
	user = session.query(User).filter(User.name == user_name).first()
	diary_entries = session.query(FoodDiaryEntry).filter(FoodDiaryEntry.author_id==user.id).order_by(FoodDiaryEntry.created_at)
	return diary_entries

@app.route("/users/<user_name>/food_diary", methods=['GET', 'POST'])
def food_diary_page(user_name):
	if request.method == "POST":
		body = request.get_json()
		content = body["content"]
		user = session.query(User).filter(User.name == user_name).first()
		session.add(FoodDiaryEntry(author_id=user.id, content=content))
		session.commit()
		return ('', 204)
	else:
		entries = food_diary_entries(user_name)
		return render_template("food_diary.html", entries=entries)

@app.teardown_appcontext
def shutdown_session(exception=None):
    pass

