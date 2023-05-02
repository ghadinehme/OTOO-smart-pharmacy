# Created to allow server storage of users and their pill orders
# Additionally must store locations and pills available to dispense
# Created Ben Randoing on 02/12/2023

from flask import Flask, jsonify, request, render_template, redirect, url_for
# from helper import medications, descriptions, ingredients, instructions, \
#     orders, image_files, pill_per_dose, pill_function
from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField
from wtforms.validators import DataRequired
import json
import numpy as np
from flask_sqlalchemy import SQLAlchemy
# import stepper
# import dispense
# import slider
# import RPi.GPIO as GPIO
import time


app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myDB.db' #path to database and its name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #to supress warning
db = SQLAlchemy(app) #database instance

#Declare Database

class Pharmacy(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    location = db.Column(db.String(80), index=True, unique=True)
    meds = db.relationship('Medication', backref='pharmacy',
                                  lazy='dynamic')


class Medication(db.Model):
    name = db.Column(db.String(80), index=True, unique=True,
                     primary_key=True) # primary key
    amt_left = db.Column(db.Integer, unique=False)
    description = db.Column(db.String(50), index=True, unique=False)
    pill_per_dose = db.Column(db.Integer, unique=False)
    image_filename = db.Column(db.String(80), unique=True)
    pill_function = db.Column(db.String(80), unique=False) # ie: Pain Relief
    location_id = db.Column(db.Integer,
                        db.ForeignKey('pharmacy.id'))  # foreign key column

# use when settting up machine to createe database
# with app.app_context():
#     # Use SQLAlchemy functionality that requires the application context
#     db.create_all()


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

class AdminForm(FlaskForm):
    submit = SubmitField('Admin')
    
@app.route("/", methods=["GET", "POST"])
def home():
    next_form = NextForm()
    admin_form = AdminForm()
    if next_form.validate_on_submit():
        return redirect(url_for("index"))
    if admin_form.validate_on_submit():
        return redirect(url_for("admin"))

    return render_template("home.html", template_form=next_form, admin_form=admin_form)
    
    
@app.route("/place_order", methods=["GET", "POST"])
def index():
    keys = [1, 2, 3, 4, 5, 6, 7, 8]
    meds = Pharmacy.query.get(1).meds.all()
    # Grab from DB
    medications = { key:value for (key, value) in zip(keys, meds) }

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
                           template_form=pill_next_form)

@app.route("/product", methods=["GET", "POST"])
def product():
    keys = [1, 2, 3, 4, 5, 6, 7, 8]
    # Grab from DB
    medication = Medication.query.get('tylenol')

    order_form = OrderForm()
    if order_form.validate_on_submit():
        # form_data = order_form.data
        # order_num = len(orders.keys()) + 1
        # orders[order_num] = (medications[form_data["med"]], int(form_data[
        #     "quantity"]))
        return redirect(url_for("order_success"))
    return render_template("product.html", template_med=medication,
                           template_form=order_form)

@app.route("/order_success", methods=["GET", "POST"])
def order_success():
    return render_template("order_success.html")

@app.route("/admin", methods=["GET", "POST"])
def admin():
    return render_template("admin.html")







def create_image_filenames(image_file_dict):
    out_dict = {}
    for key, value in image_file_dict.items():
        out_dict[key] = url_for('static', filename=value)
    return out_dict

if __name__ == '__main__':
    app.run()
