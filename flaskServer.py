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
import json
import serial
import logging
import solenoid
import led

import requests
# from pyzbar.pyzbar import decode
from bs4 import BeautifulSoup
from scan import read_qr


# import dispense
# import slider
try:
    import RPi.GPIO as GPIO
    import advance
except ImportError:
    pass
import time


serial_port = '/dev/ttyUSB1'
baud_rate = 115200

ser = serial.Serial(serial_port, baud_rate, timeout=1)

# ~ logging.basicConfig(filename='printer.log', level=logging.INFO)

serial_port_qr = '/dev/ttyUSB0'

baud_rate = 38400

ser_qr = serial.Serial(serial_port_qr, baud_rate, timeout=1)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myDB.db' #path to database and its name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #to supress warning
app.config['SERVER_NAME'] = '127.0.0.1:5050'  
app.config['APPLICATION_ROOT'] = '/'  
app.config['PREFERRED_URL_SCHEME'] = 'http'  
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
    pharm_location = db.Column(db.Integer, unique=True, primary_key=True) # primary key
    name = db.Column(db.String(80), index=True, unique=False)
    amt_left = db.Column(db.Integer, unique=False)
    description = db.Column(db.String(50), index=True, unique=False)
    pill_per_dose = db.Column(db.Integer, unique=False)
    image_filename = db.Column(db.String(80), unique=False)
    pill_function = db.Column(db.String(80), unique=False) # ie: Pain Relief
    location_id = db.Column(db.Integer,
                        db.ForeignKey('pharmacy.id'))  # foreign key column

# Use when setting up machine to create database
# ~ with app.app_context():
    # Use SQLAlchemy functionality that requires the application context
    # ~ db.create_all()

############################################################################
########################## Setup MQTT ######################################
############################################################################

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code: " + str(rc))
    client.subscribe("order")
    client.subscribe("done")
    
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
        isDone = False;
        isDone = advance.dispense(int(quantity / 2), location, ser)
        print(isDone)
            
        # Send a message to a different topic
        different_topic = "done"
        data = {
            "isDone": 1
        }
        json_data = json.dumps(data)
        client.publish(different_topic, json_data)

        # Process topic1 message as needed
    if topic == "done":
        # Handle message for order
        json_data = json.loads(payload)
        isDone = json_data["isDone"]
        
        print("Received MSG")
        # ~ with app.test_request_context():
            # ~ print("dome")
            # ~ home_url = url_for('home')
            # ~ print(home_url)
            # ~ redirect(home_url)

        
        
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

class QRForm(FlaskForm):
    submit = SubmitField('Done')

class RefillForm(FlaskForm):
    submit = SubmitField('Done')

############################################################################
########################## Flask Endpoints #################################
############################################################################
    
@app.route("/", methods=["GET", "POST"])
def home():
    solenoid.lock()
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
        return redirect(url_for("index", ailment=ailmentIn))

    return render_template("ailment.html", template_form=ailmt_form,
                           template_ailmt=get_ailments(meds))
    
@app.route("/place_order/<ailment>", methods=["GET", "POST"])
def index(ailment):
    meds = Pharmacy.query.get(1).meds.all()
    ailment_dict = create_ailment_dict(meds)
    print(ailment_dict)

    med_locs_of_interest = ailment_dict[ailment]
    print(med_locs_of_interest)
    keys = list(range(1, (len(med_locs_of_interest) + 1)))
    meds_of_interest = [ Medication.query.get(pharm_loc) for pharm_loc in med_locs_of_interest ]
    print(meds_of_interest)


    # Grab from DB
    medications = { key:value for (key, value) in zip(keys, meds_of_interest) }
    print(medications)
    pill_function = list(medications.values())[0].pill_function

    order_form = OrderForm()
    if order_form.validate_on_submit():
        # mqtt connect to client, send, disconnect
        # client.connect(broker_address, port)
        topic = "order"
        data = {
            "location": 1,
            "quantity": 2
        }
        # modify the amt_left of drug purchased
        existing_medication = Medication.query.get(data["location"])
        existing_medication.amt_left = existing_medication.amt_left - data["quantity"]
        db.session.commit()
        
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

@app.route("/lock", methods=["GET"])
def lock():
    solenoid.lock()
    
@app.route("/unlock", methods=["GET"])
def unlock():
    solenoid.unlock()

@app.route("/admin_portal", methods=["GET", "POST"])
def replace():
    solenoid.unlock()
    led.turn_off_leds()
    meds = Pharmacy.query.get(1).meds.all()
    keys = list(range(1, (len(meds) + 1)))

    order_form = OrderForm()
    # Grab from DB
    medications = {key: value for (key, value) in zip(keys, meds)}

    if order_form.validate_on_submit():
        location_store = request.form['location']
        led.turn_on_led(int(location_store) - 1)
        return redirect(url_for("qr", location_store=location_store))

    return render_template("index2.html", template_meds=medications,
                           template_form=order_form)

@app.route("/qr/<int:location_store>", methods=["GET", "POST"])
def qr(location_store):
    qr_form = QRForm()
    # read_qr()

    if qr_form.validate_on_submit():
        #remove at index
        medication_old = Medication.query.get(location_store)
        db.session.delete(medication_old)
        db.session.commit()

        medicine_string = read_qr(ser_qr)
        medicine_json = json.loads(medicine_string)
        medicine_name = medicine_json["name"]
        amt_left = medicine_json["amt_left"]
        description = medicine_json["description"]
        pill_per_dose = medicine_json["pill_per_dose"]
        img_file = medicine_json["image_filename"]
        pill_function = medicine_json["pill_function"]
        pharm_location = location_store
        location_id = 1

                
        new_medication = Medication(name=medicine_name, amt_left=amt_left, 
                                    description=description, pill_per_dose=pill_per_dose,
                                    image_filename=img_file, pill_function=pill_function,
                                    pharm_location=pharm_location, location_id=location_id)
        
        db.session.add(new_medication)
        db.session.commit()

        #replace at index
        return redirect(url_for("refill", location=location_store, name=medicine_name))

    return render_template("QR.html",
                           template_form=qr_form)

@app.route("/refill/<int:location>/<name>", methods=["GET", "POST"])
def refill(location, name):
    medicine_name = name
    refill_form = RefillForm()

    if refill_form.validate_on_submit():
        print("here")
        return redirect(url_for("replace"))

    return render_template("replace.html", template_form=refill_form,
                           template_name=medicine_name, template_loc=location)


@app.route("/admin", methods=["GET", "POST"])
def admin():
    owner_id = Pharmacy.query.get(1).owner_id
    hashed_correct_password = User.query.get(owner_id).password_hash
    admin_form = AdminForm()
    error_message = None  # Initialize error message to None
    if admin_form.validate_on_submit():
        input_password = request.form['password']
        if check_password_hash(hashed_correct_password, input_password):
            solenoid.unlock()
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
            ailment_dict[med.pill_function] += [med.pharm_location]
        else:
            ailment_dict[med.pill_function] = [med.pharm_location]
    return ailment_dict

def get_ailments(list_of_meds):
    ailment_set = set()
    for med in list_of_meds:
        ailment_set.add(med.pill_function)
    ailment_list_sorted = sorted(list(ailment_set))
    return ailment_list_sorted

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5050)
