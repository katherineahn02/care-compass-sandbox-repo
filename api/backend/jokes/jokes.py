from flask import (
    Blueprint,
    request,
    jsonify,
    make_response,
    current_app,
    redirect,
    url_for,
)

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