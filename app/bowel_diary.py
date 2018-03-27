from flask import Flask, jsonify, abort, request, render_template
from datetime import datetime
import json
from app.database import Base, Session, User, FoodDiaryEntry

app = Flask(__name__)

session = Session()

#### GENERAL ####
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

#### HOME PAGE ####
#Route for home page
@app.route("/users/<user_name>/home", methods=["GET", "POST"])
def home_page(user_name):
	if request.method == "GET":
		return render_template("home.html")

#### FOOD DIARY PAGES ####
#Route for food entry page
@app.route("/users/<user_name>/food_entry", methods=["GET", "POST"])
def food_entry_page(user_name):
	if request.method == "GET":
		return render_template("food_entry.html")

#Submit new food entry
@app.route("/food_entry_test_form_submit", methods=["POST"])
def food_diary():#user_name#
	if request.method == "POST":
		date_time = request.form['date_time']
		print("Date and time: " + date_time)
		food_entry = request.form
		for name, value in food_entry.iteritems():
			if "food_entry_" in name:
				print(value)
				#TO DO: submit to database
				#TO DO: redirect to food diary page
		#user = session.query(User).filter(User.name == user_name).first()
		#session.add(FoodDiaryEntry(author_id=user.id, date_time=date_time, food_entry=food_entry))
		#session.commit()
		return ('', 204)
	else:
		user = session.query(User).filter(User.name == user_name).first()
		diary_entries = session.query(FoodDiaryEntry).filter(FoodDiaryEntry.author_id==user.id).order_by(FoodDiaryEntry.created_at)
		return jsonify([food_diary_entry.to_response() for food_diary_entry in diary_entries])

#Query old food entiries
def food_diary_entries(user_name):
	user = session.query(User).filter(User.name == user_name).first()
	diary_entries = session.query(FoodDiaryEntry).filter(FoodDiaryEntry.author_id==user.id).order_by(FoodDiaryEntry.created_at)
	return diary_entries

#Route for food diary page
@app.route("/users/<user_name>/food_diary", methods=['GET'])
def food_diary_page(user_name):
	#entries = food_diary_entries(user_name)
	entries = "t"
	return render_template("food_diary.html", entries=entries)


#### BOWEL DIARY PAGES ####
#Route for bowel entry page
@app.route("/users/<user_name>/bowel_entry", methods=["GET", "POST"])
def bowel_entry_page(user_name):
	if request.method == "GET":
		return render_template("bowel_entry.html")

#Submit new bowel diary entry
@app.route("/bowel_entry_test_form_submit", methods=["POST"])
def bowel_diary():#user_name#
	if request.method == "POST":
		date_time = request.form['date_time']
		episode = request.form['episode']
		urgency = request.form['urgency']
		bristol = request.form['bristol']
		print(date_time + ", " + episode + ", " + urgency + ", " + bristol)

		if episode == 'toilet':
			bm_leak = request.form['bm_leak']
			print(bm_leak)
		elif episode == 'leakage':
			episode_leakage = request.form['episode_leakage']
			print(episode_leakage)
		# user = session.query(User).filter(User.name == user_name).first()
		# session.add(BowelDiaryEntry(author_id=user.id, content=content))
		# session.commit()
		#return ('', 204)
	else:
		user = session.query(User).filter(User.name == user_name).first()
		diary_entries = session.query(BowelDiaryEntry).filter(BowelDiaryEntry.author_id==user.id).order_by(BowelDiaryEntry.created_at)
		return jsonify([bowel_diary_entry.to_response() for bowel_diary_entry in diary_entries])

#Query old bowel diary entries from database
def bowel_diary_entries(user_name):
	user = session.query(User).filter(User.name == user_name).first()
	diary_entries = session.query(BowelDiaryEntry).filter(BowelDiaryEntry.author_id==user.id).order_by(BowelDiaryEntry.created_at)
	return diary_entries

#Route for bowel diary page
@app.route("/users/<user_name>/bowel_diary", methods=['GET'])
def bowel_diary_page(user_name):
	#entries = bowel_diary_entries(user_name)
	entries = "t"
	return render_template("bowel_diary.html", entries=entries)

#################
#### TEST #####
@app.route("/test_form", methods=["GET", "POST"])
def test_form():
	if request.method == "GET":
		return render_template("test.html")

@app.route("/test_form_submit", methods=["POST"])
def test_form_submit():
	if request.method == "POST":
		like_ice_cream = request.form['like_ice_cream']
		ice_cream_flavor = request.form['ice_cream_flavor']
		print("Do you like ice cream? " + like_ice_cream + ". Gimme some " + ice_cream_flavor + "!!!!!!")
		return render_template("test_results.html", like_ice_cream=like_ice_cream, ice_cream_flavor=ice_cream_flavor)
#################
#################


@app.teardown_appcontext
def shutdown_session(exception=None):
    pass
