from models.center import *
from models.animal import *

#add_center("Center10007", "pas", "address")
print(get_all_centers())


#add_animal(1, "Tarzan", 12, "Haskell")
#print(get_all_animals())
#delete_animal(15)
#print(get_animal(12))
print(get_all_animals())
# animal = get_animal(5)
# animal.center_id = 1
# update_animal(5, animal)
print(get_center(2).animals)
#print(get_all_species())
# delete_animal(2)
# print(get_center(1).animals)