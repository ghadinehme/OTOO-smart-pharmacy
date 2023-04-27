# Created to allow server storage of users and their pill orders
# Additionally must store locations and pills available to dispense
# Created Ben Randoing on 02/12/2023

from flask import Flask, jsonify, request, render_template, redirect, url_for
from helper import medications, descriptions, ingredients, instructions, \
    orders, image_files, pill_per_dose, pill_function
from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField
from wtforms.validators import DataRequired
import json
import numpy as np
import sqlalchemy
# import stepper
# import dispense
# import slider
# import RPi.GPIO as GPIO
import time



app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'

class OrderForm(FlaskForm):
    # med = SelectField("Medication", coerce=int,
    #                   choices = [(1, medications[1]),
    #                              (2, medications[2]),
    #                              (3, medications[3])],
    #                   validators=[DataRequired()])
    # quantity = SelectField("Quantity",
    #                       choices=[(i, str(i)) for i in range(1, 21) if i % 2 == 0],
    #                       validators=[DataRequired()])
    submit = SubmitField('Submit Order')
    
class NextForm(FlaskForm):
    submit = SubmitField('Shop Now')

class PillNextForm(FlaskForm):
    submit = SubmitField('Order Now')
    
@app.route("/", methods=["GET", "POST"])
def home():
    next_form = NextForm()
    if next_form.validate_on_submit():
        return redirect(url_for("index"))
    return render_template("home.html", template_form=next_form)
    
    
@app.route("/place_order", methods=["GET", "POST"])
def index():
    pill_next_form = PillNextForm()
    if pill_next_form.validate_on_submit():
        return redirect(url_for("product"))

        #Run slider left
        # slider.slider_turn(form_data["med"], 0)
        
        #Run DC Motors to Dispense
        # dispense.motor_turn(form_data["med"], int(form_data[
        #     "quantity"]))
        #dispense.motor_turn(1, 1)
        
        #Run slider right
        # slider.slider_turn(form_data["med"], 1)
        
    return render_template("index2.html", template_meds=medications,
                           template_form=pill_next_form,
                           template_images=create_image_filenames(
                           image_files), template_perdose=pill_per_dose,
                           template_function=pill_function)

@app.route("/product", methods=["GET", "POST"])
def product():
    order_form = OrderForm()
    if order_form.validate_on_submit():
        # form_data = order_form.data
        # order_num = len(orders.keys()) + 1
        # orders[order_num] = (medications[form_data["med"]], int(form_data[
        #     "quantity"]))
        return redirect(url_for("order_success"))
    return render_template("product.html", template_image=url_for('static',
                                                                  filename=image_files[1]),
                           template_perdose=pill_per_dose[1],
                           template_function=pill_function[1],
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

@app.route("/order_success", methods=["GET", "POST"])
def order_success():
    return render_template("order_success.html")







def create_image_filenames(image_file_dict):
    out_dict = {}
    for key, value in image_file_dict.items():
        out_dict[key] = url_for('static', filename=value)
    return out_dict

if __name__ == '__main__':
    app.run()
