# Created to allow server storage of users and their pill orders
# Additionally must store locations and pills available to dispense
# Created Ben Randoing on 02/12/2023

from flask import Flask, jsonify
import json
import numpy as np
import sqlalchemy
import matplotlib

app = Flask(__name__)

test_dict = {'name': 'Ben Randoing'}

@app.route('/')
@app.route('/home')
def home():
    return jsonify(test_dict)

if __name__ == '__main__':
    app.run()