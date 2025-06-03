from flask import Flask, request

app = Flask(__name__)

users = []

@app.route("/")
def home():
    return "<h1>Hello!</h1>this is the api for my slither.io clone.<br>cool, right?"

@app.route("/register", methods=['POST'])
def register():
    data = request.get_json()
    username = data.get("username")
    users.append({"username": username, "x": 0, "y": 0, "dir": 0})
    return "success"

@app.route("/modify", methods=['POST'])
def modify():
    data = request.get_json()
    user_id = int(data["user_id"]) - 1
    users[user_id]["x"] = data["x"]
    users[user_id]["y"] = data["y"]
    users[user_id]["dir"] = data["dir"]
    return "success"

@app.route("/users", methods=['GET'])
def get_users():
    return users

if __name__ == "__main__":
    app.run(debug=True)