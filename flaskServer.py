# Created to allow server storage of users and their pill orders
# Additionally must store locations and pills available to dispense
# Created Ben Randoing on 02/12/2023

from flask import Flask, jsonify, request, render_template, redirect, \
    url_for, make_response
from flask_login import UserMixin, LoginManager, login_required, login_user, current_user
from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms.validators import DataRequired
import json
import numpy as np
from flask_sqlalchemy import SQLAlchemy
import paho.mqtt.client as mqtt

import advance
# import dispense
# import slider
import RPi.GPIO as GPIO
import time


app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myDB.db' #path to database and its name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #to supress warning
db = SQLAlchemy(app) #database instance

#Declare Database Types that are Instantiated in helper.py
class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(64), index=True, unique=True)
  password_hash = db.Column(db.String(128))
  pharms = db.relationship('Pharmacy', backref='admin',
                         lazy='dynamic')

  def set_password(self, password):
      self.password_hash = generate_password_hash(password)

class Pharmacy(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    location = db.Column(db.String(80), index=True, unique=True)
    meds = db.relationship('Medication', backref='pharmacy',
                                  lazy='dynamic')
    owner_id = db.Column(db.Integer,
                            db.ForeignKey('user.id'))  # foreign key column

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

# # Use when setting up machine to create database
# with app.app_context():
#     # Use SQLAlchemy functionality that requires the application context
#     db.create_all()

############################################################################
########################## Setup MQTT ######################################
############################################################################

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code: " + str(rc))
    client.subscribe("order")
    
def on_message(client, userdata, msg):
    topic = msg.topic
    payload = str(msg.payload.decode("utf-8"))
    print("Received MSG");
    
    if topic == "order":
        # Handle message for order
        json_data = json.loads(payload)
        location = json_data["location"]
        quantity = json_data["quantity"]
        print("Received MSG");
        print(f"Order loaction is {location} with quantity of {quantity}.")
        advance.dispense(int(quantity / 2) - 1)
        # Process topic1 message as needed
        
broker_address = "localhost"
port = 1883
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker_address, port)
client.loop_start()

############################################################################
########################## Form Creations ##################################
############################################################################

class OrderForm(FlaskForm):
    submit = SubmitField('Submit Order')
    
class NextForm(FlaskForm):
    submit = SubmitField('Shop Now')

class AilmtForm(FlaskForm):
    submit = SubmitField('Ailment')

class AdminForm(FlaskForm):
    submit = SubmitField('Admin')

############################################################################
########################## Flask Endpoints #################################
############################################################################
    
@app.route("/", methods=["GET", "POST"])
def home():
    next_form = NextForm()
    admin_form = AdminForm()
    if request.method == "POST":
        if request.form['formName'] == "next":
            if next_form.validate_on_submit():
                return redirect(url_for("ailment"))
        if request.form['formName'] == "admin":
            if admin_form.validate_on_submit():
                return redirect(url_for("admin"))

    return render_template("home.html", template_form=next_form, admin_form=admin_form)

@app.route("/ailment", methods=["GET", "POST"])
def ailment():
    meds = Pharmacy.query.get(1).meds.all()
    ailmt_form = AilmtForm()
    if ailmt_form.validate_on_submit():
        ailmentIn = request.form['ailment']
        print(ailmentIn)
        return redirect(url_for("index", ailment=ailmentIn))

    return render_template("ailment.html", template_form=ailmt_form,
                           template_ailmt=get_ailments(meds))
    
@app.route("/place_order/<ailment>", methods=["GET", "POST"])
def index(ailment):
    meds = Pharmacy.query.get(1).meds.all()
    ailment_dict = create_ailment_dict(meds)
    med_names_of_interest = ailment_dict[ailment]
    keys = list(range(1, (len(med_names_of_interest) + 1)))
    meds_of_interest = [ Medication.query.get(name) for name in med_names_of_interest ]

    # Grab from DB
    medications = { key:value for (key, value) in zip(keys, meds_of_interest) }
    pill_function = list(medications.values())[0].pill_function

    order_form = OrderForm()
    if order_form.validate_on_submit():
        # mqtt connect to client, send, disconnect
        # client.connect(broker_address, port)
        topic = "order"
        data = {
            "location": 1,
            "quantity": 6
        }
        json_data = json.dumps(data)
        client.publish(topic, json_data)
        client.loop_start()
        return redirect(url_for("order_success"))

    return render_template("indexProduc.html", template_meds=medications,
                           template_form=order_form,
                           template_title=pill_function)

@app.route("/order_success", methods=["GET", "POST"])
def order_success():
    return render_template("order_success.html")

#################### Admin Endpoints #########################

@app.route("/admin_portal", methods=["GET", "POST"])
def replace():
    meds = Pharmacy.query.get(1).meds.all()
    keys = list(range(1, (len(meds) + 1)))

    order_form = OrderForm()
    # Grab from DB
    medications = {key: value for (key, value) in zip(keys, meds)}

    if order_form.validate_on_submit():
        return redirect(url_for("order_success"))

    return render_template("index2.html", template_meds=medications,
                           template_form=order_form)

@app.route("/admin", methods=["GET", "POST"])
def admin():
    owner_id = Pharmacy.query.get(1).owner_id
    hashed_correct_password = User.query.get(owner_id).password_hash
    admin_form = AdminForm()
    error_message = None  # Initialize error message to None
    if admin_form.validate_on_submit():
        input_password = request.form['password']
        if check_password_hash(hashed_correct_password, input_password):
            return redirect(url_for("replace"))
    response = make_response(render_template("admin.html", template_form=admin_form,
                           error_message=error_message))
    return response


############################################################################
########################## Helper Functions ################################
############################################################################


        
def create_image_filenames(image_file_dict):
    out_dict = {}
    for key, value in image_file_dict.items():
        out_dict[key] = url_for('static', filename=value)
    return out_dict

def create_ailment_dict(list_of_meds):
    ailment_dict = {}
    for med in list_of_meds:
        if med.pill_function in ailment_dict:
            ailment_dict[med.pill_function] += [med.name]
        else:
            ailment_dict[med.pill_function] = [med.name]
    return ailment_dict

def get_ailments(list_of_meds):
    ailment_set = set()
    for med in list_of_meds:
        ailment_set.add(med.pill_function)
    ailment_list_sorted = sorted(list(ailment_set))
    return ailment_list_sorted

if __name__ == '__main__':
    app.run()
    app.run()
