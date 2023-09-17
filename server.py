from flask import Flask
from markupsafe import escape
from flask import render_template
from flask import request, make_response, jsonify
import json
import openai, os


app = Flask(__name__)
burned_cal = 0

def chatgpt_feedback(): #to webserver
    openai.api_key = "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"

    with open('aggregate_file.json', 'r') as file1, open('json_file.jsonl', 'r') as file2:
        agg = json.parse(file1.read())
        meals = [json.parse(meal) for meal in file2.readlines()]

    user_data = jsonify({"agg": agg, "meals": meals})
    
    #chatGPT api
    prompt = "The following data is formatted such that the first json is the aggregate of all of my meals and the second json contains lines that describe individual meals that compose the aggregate. Using this data, could you give me some advice on how to improve my diet? " + "\n" + user_data
    model = "gpt-3.5-turbo"
    response = openai.Completion.create(engine=model, prompt=prompt, max_tokens=50)

    generated_text = response.choices[0].text
    return generated_text


@app.route('/terra', methods=['POST'])
def terra():
    data = request.json
    burned_cal = float(data["data"][0]["calories_data"]["total_burned_calories"])
    return data

@app.route('/data', methods=['GET'])
def mingquant(): #to webserver
    with open('aggregate_file.json', 'r') as file1, open('json_file.jsonl', 'r') as file2:
        agg = json.loads(file1.read())
        agg["chatgpt"] = chatgpt_feedback()
        agg["burned_cal"] = burned_cal

        meals = [json.loads(meal) for meal in file2.readlines()]
        
        print(jsonify({"agg": agg, "meals": meals}))
        return jsonify({"agg": agg, "meals": meals})

app.run(port=4000)