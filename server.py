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
def mingquant(): #to webserver
    with open('aggregate_file.json', 'r') as file1, open('json_file.jsonl', 'r') as file2:
        agg = json.loads(file1.read())
        meals = [json.loads(meal) for meal in file2.readlines()]
        
        print(jsonify({"agg": agg, "meals": meals}))
        return jsonify({"agg": agg, "meals": meals})

app.run(port=4000)