from flask import (
    Blueprint,
    request,
    jsonify,
    make_response,
    current_app,
    redirect,
    url_for,
)

fake_db = [
    {
        "id": 1,
        "name": "Nick"
    },
    {
        "id": 2,
        "name": "Sydney"
    },
    {
        "id": 3,
        "name": "Katherine"
    }
]

# define the blueprint
jokes = Blueprint("jokes", __name__)

@jokes.route("/joke", methods=["GET"])
def access_funny():
    response = {
        "the_joke": "Knock Knock!", 
        "id" : 5
    }
    return jsonify(response)

@jokes.route("/joke", methods=["POST"])
def add_joke():
    req = request.get_json()
    title = req["title"]
    return jsonify(title)

@jokes.route("/users/<int:id>", methods=["GET"])
def get_username_by_id(id):
    for user in fake_db :
        if id == user["id"] :
            username = {"name": user["name"]}
            return jsonify(username)
        
    message = "not found"
    return jsonify(message)

@jokes.route("/users", methods=["POST"])
def add_user():
    req = request.get_json()
    id = req["id"]
    name = req["name"]
    new_user = {"id": id, "name": name}
    return jsonify(new_user)


