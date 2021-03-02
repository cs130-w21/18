from flask import Flask
from flask_cors import CORS
from os import environ
from backend.mood import mood_api
from backend.auth import auth_api
from backend.spotify_facade import spotify_api
from backend.playlist import playlist_api
from backend.user import user_api
from backend.utils.db import DB

with DB() as db:
    db.initialize()

app = Flask(__name__)
CORS(app, resources={r"/*" : {"origins": environ['ALLOW_ORIGINS']}})
app.register_blueprint(mood_api, url_prefix='/api/v1/mood')
app.register_blueprint(spotify_api, url_prefix='/api/v1/spotify')
app.register_blueprint(auth_api, url_prefix='/login')
app.register_blueprint(playlist_api, url_prefix='/api/v1/playlist')
app.register_blueprint(user_api, url_prefix='/api/v1/user')

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    app.run()
