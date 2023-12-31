from flaskServer import db, Pharmacy, Medication, User, app
from werkzeug.security import generate_password_hash

user1 = User(id = 1, username = 'fiveFries!',
             password_hash = generate_password_hash("me310"))

pharmacy = Pharmacy(id = 1, location = 'loft', owner_id = \
    user1.id)

tylenol = Medication(name = 'tylenol', amt_left = 400, description = 'Tylenol Description',
                     pill_per_dose = 2, image_filename = 'tylenol_1.png',
                     pill_function = 'Pain Relief', pharm_location = 1,
                     location_id = \
    pharmacy.id)
    
tums = Medication(name = 'tums', amt_left = 400, description = 'Tums Description',
                     pill_per_dose = 2, image_filename = 'tums.png',
                     pill_function = ' Stomach', pharm_location = 2,
                     location_id = \
    pharmacy.id)

# ~ advil = Medication(name = 'advil', amt_left = 400, description = 'Advil '
                     # ~ 'Description',
                     # ~ pill_per_dose = 2, image_filename = 'advil.png',
                     # ~ pill_function = 'Pain Relief', pharm_location = 2,
                     # ~ location_id = pharmacy.id)

aleve = Medication(name = 'aleve', amt_left = 400, description = 'Aleve '
                     'Description',
                     pill_per_dose = 2, image_filename = 'aleve_1.png',
                     pill_function = 'Pain Relief', pharm_location =
                     3, location_id = pharmacy.id)

# ~ zantac = Medication(name = 'zantac', amt_left = 400, description = 'Zantac '
                     # ~ 'Description',
                     # ~ pill_per_dose = 2, image_filename = 'zantac_1.png',
                     # ~ pill_function = 'Antacid', pharm_location = 4,
                     # ~ location_id = pharmacy.id)

# ~ claritin = Medication(name = 'claritin', amt_left = 400, description =
                     # ~ 'Claritin Description',
                     # ~ pill_per_dose = 2, image_filename = 'claritin.png',
                     # ~ pill_function = 'Allergy Relief', pharm_location = 5,
                     # ~ location_id = pharmacy.id)

# ~ zyrtec = Medication(name = 'zyrtec', amt_left = 400, description = 'Zyrtec '
                     # ~ 'Description',
                     # ~ pill_per_dose = 2, image_filename = 'zyrtek_1.png',
                     # ~ pill_function = 'Allergy Relief', pharm_location =
                     # ~ 6, location_id = pharmacy.id)

# ~ dayquil = Medication(name = 'dayquil', amt_left = 400, description = 'DayQuil '
                     # ~ 'Description',
                     # ~ pill_per_dose = 2, image_filename = 'dayquil.png',
                     # ~ pill_function = 'Cold and Flu', pharm_location = 7,
                     # ~ location_id =
                     # ~ pharmacy.id)

# ~ peptobismol = Medication(name = 'peptobismol', amt_left = 400, description =
                     # ~ 'Peptobismol Description',
                     # ~ pill_per_dose = 2, image_filename = 'peptobismol.png',
                     # ~ pill_function = 'Stomach', pharm_location = 8,
                         # ~ location_id = pharmacy.id)

with app.app_context():
    db.session.add(user1)
    db.session.add(pharmacy)

    db.session.add(tylenol)
    db.session.add(aleve)


    try:
        db.session.commit()
    except:
        db.session.rollback()
