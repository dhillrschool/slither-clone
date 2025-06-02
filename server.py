from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello!"

@app.route("/game")
def game():
    return "Hello, Game!<br><strong>this is in HTML!</strong>"

if __name__ == "__main__":
    app.run(debug=True)