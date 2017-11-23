from flask import Flask, jsonify, abort, request
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

@app.route("/users/<user_name>/food_diary", methods=["GET", "POST"])
def food_diary(user_name):
	if request.method == "POST":
		user = session.query(User).filter(User.name == user_name).first()
		session.add(FoodDiaryEntry(author_id=user.id, content="blahblahblah"))
		session.commit()
		return ('', 204)
	else:
		user = session.query(User).filter(User.name == user_name).first()
		diary_entries = session.query(FoodDiaryEntry).filter(FoodDiaryEntry.author_id==user.id).order_by(FoodDiaryEntry.created_at)
		return jsonify([food_diary_entry.to_response() for food_diary_entry in diary_entries])


#@app.route("/users/<user_name>/food_diary/<entry_id>", methods=["GET"])
#def get_food_diary_entry(user_name, entry_id):
#	user = session.query(User).filter(User.name == user_name).first()
#	entry = session.query(FoodDiaryEntry).filter(FoodDiaryEntry.author_id == user.id and FoodDiaryEntry.id == entry_id).first()
#	return entry.to_response

@app.teardown_appcontext
def shutdown_session(exception=None):
    pass

