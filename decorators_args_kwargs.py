def announce(func):
    """A basic decorator: it accepts the function being decorated."""

    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        return func(*args, **kwargs)

    return wrapper

@announce
def greet(name: str) -> str:
    return f"Hello, {name}!"

def repeat(times: int = 1):
    def decorator(func):
        def wrapper(*args, **kwargs):
            result = None
            for _ in range(times):
                result = func(*args, **kwargs)
            return result

        return wrapper

    return decorator


@repeat(3)
def say(message: str) -> None:
    print(message)


@repeat()
def say_once(message: str) -> None:
    print(message)


def show_call(func):
    """Display the positional and keyword arguments passed to a function."""

    def wrapper(*args, **kwargs):
        print(f"  args = {args!r}")
        print(f"  kwargs = {kwargs!r}")
        return func(*args, **kwargs)

    return wrapper


@show_call
def describe_person(name: str, age: int, city: str = "Unknown") -> str:
    return f"{name} is {age} and lives in {city}."


def make_profile(name: str, age: int, city: str) -> dict[str, object]:
    """A function that accepts ordinary positional and keyword arguments."""
    return {"name": name, "age": age, "city": city}


def main() -> None:
    print("1) A basic decorator")
    print(greet("Ada"))

    print("\n2) A decorator that accepts its own argument")
    say("Decorators can repeat a function call.")
    say_once("The default repeat count is one.")

    print("\n3) *args and **kwargs in a decorator")
    # Positional arguments are collected into args (a tuple).
    # Named arguments are collected into kwargs (a dictionary).
    print(describe_person("Grace", 37, city="New York"))

    print("\n4) Unpacking arguments with * and **")
    positional_values = ("Lin", 29)
    keyword_values = {"city": "London"}

    # * unpacks an iterable into positional arguments.
    # ** unpacks a dictionary into named arguments.
    print(describe_person(*positional_values, **keyword_values))

    print("\n5) Forwarding arbitrary arguments")
    saved_positional = ("Katherine", 45)
    saved_keywords = {"city": "Washington"}
    # A wrapper forwards both collections to the wrapped function with
    # func(*args, **kwargs), preserving the original call.
    print(describe_person(*saved_positional, **saved_keywords))

    print("\n6) Unpacking a dictionary into a function call")
    profile_values = {"name": "Dorothy", "age": 31, "city": "Chicago"}
    print(make_profile(**profile_values))


if __name__ == "__main__":
    main()
