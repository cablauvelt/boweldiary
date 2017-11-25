from flask import Flask, jsonify, abort, request, render_template
import json
from app.database import Base, Session, User, FoodDiaryEntry
#Get Base db class, session here from DB.

app = Flask(__name__)

session = Session()

@app.route("/users/<user_name>", methods=['GET'])
def get_user(user_name):
	user = session.query(User).filter(User.name == user_name).first()
	return jsonify(user.to_response()) if user is not None else abort(404)

@app.route("/users", methods=['GET'])
def get_users():
	users = session.query(User).order_by(User.id)
	return jsonify([user.to_response() for user in users])

#@app.route("/users/<user_name>/food_diary", methods=["GET", "POST"])
def food_diary(user_name):
	if request.method == "POST":
		body = request.get_json()
		content = body["content"]
		user = session.query(User).filter(User.name == user_name).first()
		session.add(FoodDiaryEntry(author_id=user.id, content=content))
		session.commit()
		return ('', 204)
	else:
		user = session.query(User).filter(User.name == user_name).first()
		diary_entries = session.query(FoodDiaryEntry).filter(FoodDiaryEntry.author_id==user.id).order_by(FoodDiaryEntry.created_at)
		return jsonify([food_diary_entry.to_response() for food_diary_entry in diary_entries])

def food_diary_entries(user_name):
	user = session.query(User).filter(User.name == user_name).first()
	diary_entries = session.query(FoodDiaryEntry).filter(FoodDiaryEntry.author_id==user.id).order_by(FoodDiaryEntry.created_at)
	#return jsonify([food_diary_entry.to_response() for food_diary_entry in diary_entries])
	return diary_entries

@app.route("/users/<user_name>/food_diary", methods=['GET'])
def food_diary_page(user_name):
	entries = food_diary_entries(user_name)
	return render_template("food_diary.html", entries=entries)
	#return render_template("food_diary.html", entries=entries)

@app.teardown_appcontext
def shutdown_session(exception=None):
    pass

