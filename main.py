from flask import Flask
from backend.mood import mood_api

app = Flask(__name__)
app.register_blueprint(mood_api, url_prefix='/api/v1/mood')

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    app.run()
