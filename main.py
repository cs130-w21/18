from flask import Flask
from flask_cors import CORS
from os import environ
from backend.mood import mood_api
from backend.auth import auth_api

app = Flask(__name__)
CORS(app, resources={r"/*" : {"origins": environ['ALLOW_ORIGINS']}})
app.register_blueprint(mood_api, url_prefix='/api/v1/mood')
app.register_blueprint(auth_api, url_prefix='/login')

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    app.run()
