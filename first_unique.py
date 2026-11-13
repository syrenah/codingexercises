"""Find the first value in a list that appears exactly once."""
from collections import Counter

def solution_original(A):
    """The original approach; list membership makes this quadratic."""
    if len(A) == 0:
        return -1
    seen = {}
    for x in A:
        if x not in seen:
            seen[x] = 1
        else:
            seen[x] = seen[x] + 1

    numbers = [key for key, value in seen.items() if value == 1]

    if len(numbers) == 0:
        return -1
    for x in A:
        if x in numbers:
            return x
    return -1


def solution_dict(A):
    """Count with a dictionary, then scan A in its original order.
    Average time: O(N). Space: O(U), where U is the number of distinct values.
    """
    counts = {}

    for x in A:
        counts[x] = counts.get(x, 0) + 1

    for x in A:
        if counts[x] == 1:
            return x

    return -1


def solution_counter(A):
    """Use Counter to count, then scan A in its original order.
    Average time: O(N). Space: O(U), where U is the number of distinct values.
    """
    counts = Counter(A)
    print(counts)
    for x in A:
        if counts[x] == 1:
            return x

    return -1


if __name__ == "__main__":
    example = [4, 5, 1, 2, 1, 4, 5]
    print(solution_original(example))  # 2
    print(solution_dict(example))      # 2
    print(solution_counter(example))   # 2
