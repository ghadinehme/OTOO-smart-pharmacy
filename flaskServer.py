# Created to allow server storage of users and their pill orders
# Additionally must store locations and pills available to dispense
# Created Ben Randoing on 02/12/2023

from flask import Flask, jsonify, request, render_template
from helper import recipes, descriptions, ingredients, instructions
import json
import numpy as np
import sqlalchemy

app = Flask(__name__)

@app.route("/")
def index():
  return render_template("index.html", template_recipes=recipes)

@app.route("/recipe/<int:id>", methods=["GET", "POST"])
def recipe(id):
  return render_template("recipe.html", template_recipe=recipes[id],
                         template_description=descriptions[id],
                         template_ingredients=ingredients[id],
                         template_instructions=instructions[id])

@app.route("/about")
def about():
  return render_template("about.html")

if __name__ == '__main__':
    app.run()