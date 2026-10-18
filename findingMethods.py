import inspect

# Find the public methods defined on list, excluding special methods such as __len__.
list_methods = inspect.getmembers(
    list,
    lambda member: inspect.isroutine(member)
    and not member.__name__.startswith("__"),
)

numbers = [4, 2, 7, 2]
method_arguments = {
    "append": (9,),
    "count": (2,),
    "extend": ([9, 10],),
    "index": (2,),
    "insert": (1, 9),
    "remove": (2,),
}

print(f"Public list methods: {[name for name, _ in list_methods]}")
print(f"Starting numbers: {numbers}")
print("Results from public list methods:")
for name, _ in list_methods:
    working_numbers = numbers.copy()
    result = getattr(working_numbers, name)(
        *method_arguments.get(name, ())
    )
    print(
        f"  {name}: returned {result!r}; "
        f"list after call {working_numbers}"
    )