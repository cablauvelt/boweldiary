import json
import os

app_key = None
app_id = None

current_file = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

try:
    config = json.load(open(current_file + "/config.json"))
except IOError:
    msg ='Please put a file called config.json in {}'.format(current_file)
    msg = msg + ' of the form:\n { "app_id" : <Edamam app id>, "app_key" : <Edamam app key> }'
    raise ValueError(msg)
else:
    app_key = config["app_key"]
    app_id = config["app_id"]
