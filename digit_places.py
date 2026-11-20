"""Extract the ones, tens, and hundreds digits from an integer."""

number = 482

ones_digit = number % 10
tens_digit = (number // 10) % 10
hundreds_digit = (number // 100) % 10

print(f"Ones: {ones_digit}")
print(f"Tens: {tens_digit}")
print(f"Hundreds: {hundreds_digit}")
