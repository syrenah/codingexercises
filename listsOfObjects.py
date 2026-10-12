from cute_bird_class_stuff import Chicken
import inspect
# Find routines (functions and methods) defined on the str type
# string_methods = inspect.getmembers(str, inspect.isroutine)
# print([name for name, method in string_methods])
class Pet:
    kind = "animal"
    @property
    def name(self):
        return "Milo"
    def speak(self):
        return "hello"

print(inspect.getmembers(Pet, lambda member: isinstance(member, property)))

pet = Pet()
pet_properties = inspect.getmembers(
    type(pet), lambda member: isinstance(member, property)
)
print("Pet properties:")
for property_name, _ in pet_properties:
    print(f"  {property_name}: {getattr(pet, property_name)}")


chickens = [
    Chicken(),
    Chicken(),
    Chicken(),
    Chicken(),
]

for chicken, (name, shoe_size) in zip(
    chickens,
    [ ("Chucky", 10), ("Clucky", 12), ("Cheep", 9), ("Cheep", 6)],
):
    chicken.name = name
    chicken.shoeSize = shoe_size

# Chicken publicly exposes name and shoeSize as properties.
large_shoes = [chicken for chicken in chickens if chicken.shoeSize >= 10]

print("Chickens with shoe size 10 or larger:")
for chicken in large_shoes:
    print(f"Name: {chicken.name}, shoe size: {chicken.shoeSize}")

# sorted() returns a new list, leaving the original list order unchanged.
chickens_by_shoe_size = sorted(chickens, key=lambda chicken: chicken.shoeSize)
print("Chickens sorted by shoe size:")
for chicken in chickens_by_shoe_size:
    print(f"{chicken.name}: {chicken.shoeSize}")

# next() finds the first matching object; None is returned if there is no match.
cluck = next((h for h in chickens if h.name == "Clucky"), None)
if cluck is not None:
    print(f"Found {cluck.name}")
    cluck.shoeSize = 13  # Objects can be updated through a reference from the list.

# any() checks whether at least one item matches; all() checks every item.
print(f"Any chicken has shoe size 13: {any(chicken.shoeSize == 13 for chicken in chickens)}")
print(type(any(chicken.shoeSize == 13 for chicken in chickens)))
print(f"All chickens have a name: {all(chicken.name for chicken in chickens)}")

# A list comprehension can filter objects out of a list.
new_chickens = [c for c in chickens if c.name != "Clucky"]
print(f"After removing Clucky: {[c.name for c in new_chickens]}")

for name, prop in inspect.getmembers(
    type(chicken),
    lambda member: isinstance(member, property),
):
    print(f"{name}: {getattr(chicken, name)}")

for chick in chickens:
    # print(vars(chick))  # vars() returns the __dict__ of an object, which contains its attributes and their values.
    # print(type(vars(chick)))  # <class 'dict'>
    
    # print(vars(chick).keys())  #<class 'dict_keys'>
    print(type(vars(chick).keys()) ) #{'_name': 'Bruno', '_Bird__shoeSize': 10, '_Bird__hatColor': 'red'}

mychicken = Chicken()
with mychicken as c:
    print(f"Inside the with block: {c.name}")
