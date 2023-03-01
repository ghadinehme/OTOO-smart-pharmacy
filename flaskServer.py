# Created to allow server storage of users and their pill orders
# Additionally must store locations and pills available to dispense
# Created Ben Randoing on 02/12/2023

from flask import Flask, jsonify, request, render_template, redirect, url_for
from helper import medications, descriptions, ingredients, instructions, orders
from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, RadioField
from wtforms.validators import DataRequired
import json
import numpy as np
import sqlalchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'

class OrderForm(FlaskForm):
    med = SelectField("Medication", coerce=int,
                      choices = [(1, medications[1]),
                                 (2, medications[2]),
                                 (3, medications[3])],
                      validators=[DataRequired()])
    quantity = RadioField("Quantity",
                          choices=[(5, "5"), (10, "10"),
                                   (20, "20")],
                          validators=[DataRequired()])
    submit = SubmitField('Submit Order')

@app.route("/", methods=["GET", "POST"])
def index():
    order_form = OrderForm()
    if order_form.validate_on_submit():
        form_data = order_form.data
        order_num = len(orders.keys()) + 1
        orders[order_num] = (medications[form_data["med"]], int(form_data[
            "quantity"]))
        print(orders)
        return redirect(url_for("order_success"))
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

@app.route("/order_success")
def order_success():
    return render_template("order_success.html")

if __name__ == '__main__':
    app.run()