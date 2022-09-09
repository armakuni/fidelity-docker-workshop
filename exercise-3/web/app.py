from flask import Flask

app = Flask(__name__)


@app.route("/")
def index():
    return "Web App with Python Flask - exercise 3!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)