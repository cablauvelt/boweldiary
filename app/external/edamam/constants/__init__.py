import json
import os

current_file = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
print(current_file)
config = json.load(open(current_file + "/config.json"))
print(json.dumps(config))
app_key = config["app_key"]

app_id = config["app_id"]
