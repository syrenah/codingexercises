numbers = [1, 2, 3, 4, 5, 6]
scores = {"Amit": 92, "Ben": 67, "Cindy": 85, "Dan": 73}


def is_passing_score(score_entry):
    return score_entry[1] >= 70


if __name__ == "__main__":
   
    even_numbers = list(filter(lambda number: number % 2 == 0, numbers))
    doubled_numbers = list(map(lambda number: number * 2, numbers))
    doubled_evens = list(
        map(lambda number: number * 2, filter(lambda number: number % 2 == 0, numbers))
    )

    even_squares = [number**2 for number in numbers if number % 2 == 0]

 
    passing_scores = dict(filter(lambda item: item[1] >= 70, scores.items()))
    passing_scores_with_function = dict(filter(is_passing_score, scores.items()))
    bonus_scores = dict(
        map(lambda item: (item[0], item[1] + 5), passing_scores.items())
    )

    # Dictionary comprehensions can filter and transform key-value pairs.
    high_scores = {name: score for name, score in scores.items() if score >= 80}
    score_labels = {
        name: "pass" if score >= 70 else "retry"
        for name, score in scores.items()
    }

    print(f"Original numbers: {numbers}")
    print(f"Even numbers with filter + lambda: {even_numbers}")
    print(f"Doubled numbers with map + lambda: {doubled_numbers}")
    print(f"Doubled evens with map + filter + lambda: {doubled_evens}")
    print(f"Even squares with a list comprehension: {even_squares}")
    print()
    print(f"Original scores: {scores}")
    print(f"Passing scores with filter + lambda: {passing_scores}")
    print(f"Passing scores with filter + function: {passing_scores_with_function}")
    print(f"Passing scores with a 5-point bonus using map: {bonus_scores}")
    print(f"Scores of 80 or more with a dict comprehension: {high_scores}")
    print(f"Pass/retry labels with a dict comprehension: {score_labels}")