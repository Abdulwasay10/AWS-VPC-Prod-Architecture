from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "My First AWS PROJECT to demonstrate apps in private subnet"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
