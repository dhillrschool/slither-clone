from flask import Flask, request

app = Flask(__name__)

users = []

@app.route("/")
def home():
    return "Hello!"

@app.route("/game")
def game():
    return "Hello, Game!<br><strong>this is in HTML!</strong>"

@app.route("/register", methods=['POST'])
def register():
    data = request.get_json()
    username = data.get("username")
    users.append({"username": username, "id": len(users)+1})
    return f"hi {username}"

if __name__ == "__main__":
    app.run(debug=True)