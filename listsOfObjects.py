from cute_bird_class_stuff import Chicken
import inspect


chickens = [
    Chicken(),
    Chicken(),
    Chicken(),
    Chicken(),
]

for chicken, (name, shoe_size) in zip(
    chickens,
    [("Bruno", 8), ("Penny", 10), ("Cluck", 12), ("Daisy", 9)],
):
    chicken.name = name
    chicken.shoeSize = shoe_size

# Chicken publicly exposes name and shoeSize as properties.
large_shoes = [chicken for chicken in chickens if chicken.shoeSize >= 10]

print("Chickens with shoe size 10 or larger:")
for chicken in large_shoes:
    print(f"Name: {chicken.name}, shoe size: {chicken.shoeSize}")

for name, prop in inspect.getmembers(
    type(chicken),
    lambda member: isinstance(member, property),
):
    print(f"{name}: {getattr(chicken, name)}")

for chicken in chickens:
    # print(chicken.keys())
    print(vars(chicken))  # vars() returns the __dict__ of an object, which contains its attributes and their values.
    print(type(vars(chicken)))  # <class 'dict'>
    
    print(vars(chicken).keys())  #<class 'dict_keys'>
    print(type(vars(chicken).keys()) ) 
    
mychicken = Chicken()
with mychicken as c:
    print(f"Inside the with block: {c.name}")
