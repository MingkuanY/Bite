from flask import Flask
from markupsafe import escape
from flask import render_template
from flask import request, make_response, jsonify
import json
import requests


app = Flask(__name__)
burned_cal = 0

@app.route('/terra', methods=['POST'])
def terra():
    data = request.json
    burned_cal = float(data["data"][0]["calories_data"]["total_burned_calories"])
    return data

@app.route('/data', methods=['GET'])
def mingquant():
    return """{"yeasty":"tasty"}"""

app.run(port=4000)