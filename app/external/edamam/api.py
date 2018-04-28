import requests
import json

from constants import app_id, app_key

search = "https://api.edamam.com/api/food-database/parser"

auto_complete = "http://api.edamam.com/auto-complete"

nutrient_api = "https://api.edamam.com/api/food-database/nutrients"

def api_auth_params():
    return { "app_id" : app_id, "app_key" : app_key }

def create_api_params(params_dict):
    auth_params = api_auth_params() 
    auth_params.update(params_dict)
    return auth_params 

def text_search(ingredient_text):
    query_params = create_api_params({ "ingr" : ingredient_text }) 
    r = requests.get(search, query_params)
    return r.json()

def barcode_search(barcode):
    query_params = create_api_params({"upc" : barcode })
    r = requests.get(search, query_params)
    return r.json()

def auto_complete(query_text):
    query_params = create_api_params({ "q" : query_text })
    r = requests.get(auto_complete, query_params)
    return r.json()

def create_ingredient(food_uri, measure_uri, quantity=1):
    return { "quantity" : quantity, "measureURI" : measure_uri, "foodURI" : food_uri }

def create_ingredients_request(ingredients, num_servings=1):
    return json.loads(json.dumps({ "yield" : num_servings, "ingredients" : ingredients }))

def get_nutrients(ingredient_text):
    search_hits = text_search(ingredient_text)
    hints = search_hits["hints"]
    ingredients = [ create_ingredient(hit["food"]["uri"], hit["measures"][0]["uri"]) for hit in hints ]
    nutrient_url = nutrient_api + "?app_id={}&app_key={}".format(app_id, app_key)
    r = requests.post(nutrient_url, json=create_ingredients_request([ingredients[0]]))
    return r

if __name__ == "__main__":
    cherry_pie = get_nutrients("cherry pie")
    print(cherry_pie.text)
