person = {
    "name": "Syrenah",
    "age": 30,
    "language": "Python"
}
# Loop through keys
for key in person:
    print(key)
# Loop through values
for value in person.values():
    print(value)
# Loop through keys and values
for key, value in person.items():
    print(key, value)
if "name" in person:
    print("Found name")
# Check for a key before accessing its value.
if "email" in person:
    print(person["email"])
else:
    print("email key is missing")

# get() returns a default value without changing the dictionary.
print(person.get("email", "Not found"))
print(person.get("name", "Not found"))

# setdefault() returns the existing value or inserts and returns the default.
email = person.setdefault("email", "unknown@example.com")
print(f"Email from setdefault: {email}")
# Catch KeyError when using square-bracket lookup for a possibly missing key.
try:
    print(person["phone"])
except KeyError:
    print("phone key is missing")
