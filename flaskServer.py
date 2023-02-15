# Created to allow server storage of users and their pill orders
# Additionally must store locations and pills available to dispense
# Created Ben Randoing on 02/12/2023

from flask import Flask, jsonify, request
import json
import numpy as np
import sqlalchemy
import matplotlib

app = Flask(__name__)

test_dict = {'name': 'Ben Randoing'}

@app.route('/')
@app.route('/home', methods = ["GET", "POST"])
def home():
    if request.method == "POST":
        print(request.get_json())
    else:
        return jsonify(test_dict)

if __name__ == '__main__':
    app.run()