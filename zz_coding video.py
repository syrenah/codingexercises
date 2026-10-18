from cute_bird_class_stuff import Bird
n = 12345
# Get all digits one at a time from right to left
while n > 0:
    digit = n % 10
    print(digit)
    n //= 10

nums=[1,2,3,4,5]

n = 1234567
ones      = (n // 1) % 10      # 7
tens      = (n // 10) % 10     # 6
hundreds  = (n // 100) % 10    # 5
thousands = (n // 1000) % 10   # 4


n % 10     # last digit
n // 10    # remove last digit
n / 10     # regular division (float)
(n // 10) % 10  # tens digit

n = 1234567

first_two = int(str(n)[:2])
print(first_two)  # 12

print(nums)# The entire list

print(len(nums))
# Number of elements
print(nums[0])# First element
print(nums[-1])# Last element
print(nums[:3])# First three elements
print(nums[::-1])# List in reverse order

x = "123"
print(dir(__builtins__))

print(type(x))

s = "hello\n"

print(s)
print(repr(s))

# str()
# int()
# float()
# bool()
# list()
# tuple()
# set()
# dict()

print(dir(str))

object = Bird(name="Lucy")
print(help(object))
print(dir(object))
print(type(object))


names = ["Bob", "Sue"]
ages = [25, 30]

print(list(zip(names, ages)))


numbers = [1, 2, 3]

result = list(map(lambda x: x * 2, numbers))
print(result)

##filter() - Keep only matching items
numbers = [1, 2, 3, 4, 5, 6]

result = list(filter(lambda x: x % 2 == 0, numbers))
print(result)

name = input("Enter your name: ")
print("Hello", name)