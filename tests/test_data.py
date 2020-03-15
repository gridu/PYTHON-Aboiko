test_login_register = "Center23"
test_password_register = "password23"
test_address = "Berlin"

not_existing_login = "John Doe"

test_login = "Center1"
test_password = "password1"
test_animal_id_for_login = 2
test_animal_id_not_related_for_login = 8
not_existing_animal_id = 99

test_animal_name = "Gregg"
test_animal_name_post = "Animal for post"
test_animal_age = 5
test_animal_specie = "red fox"

test_specie_id = 1
test_specie_not_existing_id = 99

# data to post specie
test_specie_name_for_post = "Flying elephant"
test_specie_price_for_post = 3
test_specie_description_for_post = "likes Python"

# test specie data to add (mocking function which checks presence of this specie in db)
test_specie_name_exists = "red fox"
test_specie_price_exists = 120.55
test_specie_description_exists = "Lives in forests"

test_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwiZXhwIjoxNTg0MTE3NzI1fQ.PyV7nGkaCWh04DRyS8YQAV6QOshmI7A-_cBjS7zJ3EM"

# test animal data to add (mocking function which checks presence of this animal in db)
test_animal_name_exists = "fox1"
test_animal_age_exists = 2
test_animal_specie_exists = "red fox"

# data to update an animal
# animal_data: 0 - animal id from route URL, 1 - center id to which animal
#     belongs to, 2 - animal name, 3 - animal age, 4 - specie
test_animal_data_exists = [5, 2, "Estampl", 7, "elephant"]
test_animal_not_existing = [35, 2, "Estampl", 7, "elephant"]
