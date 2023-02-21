# Created to allow server storage of users and their pill orders
# Additionally must store locations and pills available to dispense
# Created Ben Randoing on 02/12/2023

from flask import Flask, jsonify, request, render_template
from helper import medications, descriptions, ingredients, instructions
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerRangeField
import json
import numpy as np
import sqlalchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'

class OrderForm(FlaskForm):
    med = SelectField("Medication", coerce=int,
                      choices = [(1, "Tylenol"),
                                 (2, "Ibuprofen"),
                                 (3, "Aleve")])
    quantity = IntegerRangeField("Quantity")
    submit = SubmitField('Submit Order')

@app.route("/")
def index():
    order_form = OrderForm()
    return render_template("index.html", template_meds=medications,
                           template_form=order_form)

@app.route("/med/<int:id>", methods=["GET", "POST"])
def recipe(id):
    return render_template("med.html", template_med=medications[id],
                         template_description=descriptions[id],
                         template_ingredients=ingredients[id],
                         template_instructions=instructions[id])

@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == '__main__':
    app.run()