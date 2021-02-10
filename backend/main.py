from flask import Flask
from mood import mood_api

app = Flask(__name__)
app.register_blueprint(mood_api)

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    app.run()