medications = {1: "Tylenol", 2: "Ibuprofen", 3: "Aleve"}
types = {1: "Breakfast", 2: "Breakfast"}
descriptions = {1: "Pain Relief", 2: "Pain Relief", 3: "Allergy Relief"}
ingredients = {1: ["a", "b", "c"], 2: ["a", "b", "c"], 3: ["a", "b", "c"]}
instructions = {1: {"Step 2": "a", "Step 5": "b", "Step 1": "c", "Step 4": "d", "Step 3": "e"},
                2: {"Step 3": "a", "Step 4": "b", "Step 1": "c", "Step 2": "d"},
                3: {"Step 3": "a", "Step 4": "b", "Step 1": "c", "Step 2": "d"}}
comments = {1: ["Yummy!!", "Egg-cellent ;->"], 2: ["Toasty", "What a great recipe!"]}

def add_ingredients(recipe_id=None, text=None):
  if recipe_id and text:
    text_list = text.split("\n")
    ingredients[recipe_id] = text_list

def add_instructions(recipe_id=None, text=None):
  if recipe_id and text:
    text_list = text.split("\n")
    instructions_dict = {}
    for i, instruction in enumerate(text_list):
      instructions_dict["Step {}".format(i+1)] = instruction

    instructions[recipe_id] = instructions_dict