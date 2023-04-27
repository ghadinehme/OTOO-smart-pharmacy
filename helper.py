medications = {1: "Tylenol", 2: "Ibuprofen", 3: "Aleve"}
types = {1: "Breakfast", 2: "Breakfast"}
descriptions = {1: "Pain Relief", 2: "Pain Relief", 3: "Allergy Relief"}
ingredients = {1: ["a", "b", "c"], 2: ["a", "b", "c"], 3: ["a", "b", "c"]}
instructions = {1: {"Step 2": "a", "Step 5": "b", "Step 1": "c", "Step 4": "d", "Step 3": "e"},
                2: {"Step 3": "a", "Step 4": "b", "Step 1": "c", "Step 2": "d"},
                3: {"Step 3": "a", "Step 4": "b", "Step 1": "c", "Step 2": "d"}}
orders = {}
image_files = {1: "tylenol_1.png", 2: "advil.png", 3: "aleve_1.png",
               4: "zantac_1.png", 5: "claritin.png", 6: "zyrtek_1.png",
               7: "dayquil.png", 8: "peptobismol.png"}
pill_per_dose = {1: 2, 2: 3, 3: 2, 4: 2, 5: 2, 6: 2, 7: 2, 8: 2}
pill_function = {1: "Pain Relief", 2: "Pain Relief", 3: "Pain Relief",
                 4: "Antacid",
                 5: "Allergy Relief", 6: "Allergy Relief",
                 7: "Cold and Flu",
                 8: "Upset Stomach Relief"}


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