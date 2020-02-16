from flask import Flask, request, jsonify

app = Flask(__name__)

stores = [
    {"name": "My Wonderful Store", "items": [{"name": "Marlboro", "price": 16.50}]},
    {"name": "Nike", "items": [{"name": "F20 Sneakers", "price": 400.00}]},
]


@app.route("/store", methods=["POST"])
def create_store():
    """Creates new store and appends it to the stores' list
    
    Returns:
        json -- newly appended store
    """
    request_data = request.get_json()
    new_store = {"name": request_data["name"], "items": []}
    stores.append(new_store)
    return jsonify(new_store)


@app.route("/store/<string:name>", methods=["GET"])
def get_store(name):
    """Retrieve store by its name
    
    Arguments:
        name {string} -- name of a store to retrieve
    
    Returns:
        json -- retrived store
    """
    for store in stores:
        if store["name"] == name:
            return jsonify(store)

    return "Store Not Found", 400


@app.route("/store")
def get_stores():
    return jsonify({"stores": stores})


@app.route("/store/<string:name>/item", methods=["POST"])
def create_item_in_store(name):
    request_data = request.get_json()
    new_item = {"name": request_data["name"], "price": request_data["price"]}

    for store in stores:
        if store["name"] == name:
            store["items"].append(new_item)
            return jsonify(new_item)

    return "Couldn't create an item", 400


@app.route("/store/<string:name>/item")
def get_items_in_store(name):
    for store in stores:
        if store["name"] == name:
            return jsonify({"items": store["items"]})
    return "Store Not Found - can't get its items", 400


@app.route("/")
def home():
    return "home"
