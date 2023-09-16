from flask import Flask
from markupsafe import escape
from flask import render_template
from flask import request, make_response
import json
import requests


app = Flask(__name__)

@app.route('/terra', methods=['POST'])
def terra():
    pass

@app.route('/data', methods=['GET'])
def mingquant():
    pass