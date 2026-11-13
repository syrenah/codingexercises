
def solution(S):
    # Implement your solution here
    words = S.split()

    lengths = []

    for w in words:
        if even_num_letters(w) and odd_num_digits(w) and only_alphanum(w):
            lengths.append(len(w))

    #return len of longest word or -1
    if len(lengths) == 0:
        return -1

    return max(lengths)


def even_num_letters(w):
    count = 0
    for c in w:
        if c.isalpha():
            count += 1

    return count % 2 == 0


def odd_num_digits(w):
    count = 0
    for c in w:
        if c.isdigit():
            count += 1
    return count % 2 != 0


def only_alphanum(w):
    return w.isalnum()
