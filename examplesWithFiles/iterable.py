from collections.abc import Iterator
from pathlib import Path
import sys

#python iterable.py with_example_data.txt
def prime_numbers(beginning_int: int, end_int: int) -> Iterator[int]:
    """Yield prime numbers between beginning_int and end_int, inclusive."""
    for candidate in range(max(2, beginning_int), end_int + 1):
        is_prime = True
        divisor = 2
        while divisor * divisor <= candidate:
            if candidate % divisor == 0:
                is_prime = False
                break
            divisor += 1

        if is_prime:
            yield candidate


class FileLineIterable:
    """Iterate over the lines in a UTF-8 text file."""

    def __init__(self, filename: str | Path) -> None:
        self.filename = Path(filename)

    def __iter__(self) -> Iterator[str]:
        with self.filename.open(encoding="utf-8") as file:
            for line in file:
                yield line
            yield from file

if __name__ == "__main__":
    # if len(sys.argv) != 2:
    #     print(f"Usage: python {Path(sys.argv[0]).name} <filename>")
    #     raise SystemExit(1)

    for prime in prime_numbers(10, 30):
        print(prime)

    print(list(prime_numbers(10, 30)))

    lines = FileLineIterable(sys.argv[1])
    print(type(lines))
    print(f"lines is a {type(lines).__name__} object that can be iterated over")
    for line_number, line in enumerate(lines, start=1):
        text = line.rstrip("\r\n")
        print(f"{line_number}: {text}")