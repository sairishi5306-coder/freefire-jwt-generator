from flask import Flask, jsonify, request
from flask_caching import Cache
from response import process_token
from colorama import init
import warnings
from urllib3.exceptions import InsecureRequestWarning
import time
import os

warnings.filterwarnings("ignore", category=InsecureRequestWarning)
init(autoreset=True)

app = Flask(__name__)
cache = Cache(app, config={"CACHE_TYPE": "simple"})

@app.route("/")
def home():
    return "SR KING - JWT Token Generator API is running!"

@app.route("/token", methods=["GET"])
def get_responses():
    uid = request.args.get("uid")
    password = request.args.get("password")

    if uid and password:
        cache_key = f"token_{uid}_{password}_{int(time.time())}"
        response = process_token(uid, password)
        cache.set(cache_key, response, timeout=25200)
        return jsonify(response)

    return jsonify({"message": "Please provide uid and password parameters"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5030))
    app.run(host="0.0.0.0", port=port)