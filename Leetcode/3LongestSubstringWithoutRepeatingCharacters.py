def lengthOfLongestSubstring_with_set(input_string: str) -> int:
    # Time: O(n); each character enters and leaves the window at most once.
    # Space: O(k), where k is the number of distinct characters in the window.
    seen = set()
    left = 0
    longest = 0

    for index in range(len(input_string)):
        print(index)
        while input_string[index] in seen:
            seen.remove(input_string[left])  # Remove the outgoing character from the window.
            left += 1

        seen.add(input_string[index])  # Add the new character to the window.
        longest = max(longest, index - left + 1)

    return longest


def lengthOfLongestSubstring_with_dictionary(input_string: str) -> int:
    # Time: O(n); each character is processed once, with constant-time lookups.
    # Space: O(k), where k is the number of distinct characters stored.
    last_seen = {}
    left = 0
    longest = 0

    for index, char in enumerate(input_string):
        if char in last_seen and last_seen[char] >= left:
            left = last_seen[char] + 1  # Start after the previous occurrence.

        last_seen[char] = index  # Remember the latest index for this character.
        longest = max(longest, index - left + 1)

    return longest


if __name__ == "__main__":
    text = "abcabcbb"
    print(f"Input: {text!r}")
    print(f"Set-based result: {lengthOfLongestSubstring_with_set(text)}")
    print(f"Index-based result: {lengthOfLongestSubstring_with_dictionary(text)}")