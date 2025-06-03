import random
from flask import Flask, request

app = Flask(__name__)

users = []
user_parts = []
food = []

for i in range(1000):
    food.append({
        "x": random.randint(-2000, 2000),
        "y": random.randint(-2000, 2000)
    })

@app.route("/")
def home():
    return "<h1>Hello!</h1>this is the api for my slither.io clone.<br>cool, right?"

@app.route("/register", methods=['POST'])
def register():
    data = request.get_json()
    username = data.get("username")
    users.append({"username": username, "x": 0, "y": 0, "dir": 0, "length": 10})
    return str(len(users))

@app.route("/modify/<int:user_id>", methods=['POST'])
def modify(user_id):
    data = request.get_json()
    user_id -= 1
    users[user_id]["x"] = data["x"]
    users[user_id]["y"] = data["y"]
    users[user_id]["dir"] = data["dir"]
    users[user_id]["length"] = data["length"]
    return "success"

@app.route("/remove/<int:user_id>")
def remove(user_id):
    users.pop(user_id-1)
    return "success"

@app.route("/remove_food/<int:food_id>")
def remove_food(food_id):
    food.pop(food_id)
    return "success"

@app.route("/users", methods=['GET'])
def get_users():
    return f"{users}".replace("'", "\"")

@app.route("/food", methods=['GET'])
def get_food():
    return f"{food}".replace("'", "\"")

if __name__ == "__main__":
    app.run(debug=True)