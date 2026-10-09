def lengthOfLongestSubstring_with_set(input_string: str) -> int:
    # Time: O(n); each character enters and leaves the window at most once.
    # loops increase with the length of the string, but each character is processed at most twice
    #  (once when added to the set and once when removed), leading to a linear time complexity.
    # Space: O(k), where k is the number of distinct characters in the window.
    seenSet = set()
    # why not a list?
    #     Checking membership in a set is typically O(1).
    #     Checking membership in a list takes O(n) because Python may scan each item.
    right_index = 0
    longest_len = 0
    #sliding window aka substring
    for index in range(len(input_string)):

        # Comment A: loop will not execute at first because seen is empty,
        # will execute if the character is already in the set
        while input_string[index] in seenSet:
 
            seenSet.remove(input_string[right_index])  
            # Remove the outgoing character from the window.

            right_index += 1 # moving the  right_index to the right.
            
        seenSet.add(input_string[index])  # Add the new character to the window. 
        # first run iwlll add the first character to the set because the loop did not execute, see Comment A
        #                 0          , 0     -0            + 1
        # if  len(seenSet) !=  max(longest_len, index - right_index + 1) 
        # index is where we are in the input_string, right_index is where the window ends, so index - right_index + 1 gives the length of the current window.
        # # not always true because seen is updated even though its not the latest because we have to finish looking to the end
        longest_len = max(longest_len, index - right_index + 1) #update longest_len if the current window is longer than the previous longest.
        print(longest_len)
        print("string:  "+input_string[right_index:index+1])
        print(seenSet)
    return longest_len

if __name__ == "__main__":
    text = "abcdebcabayyybbabrtyucctyuibb"
    print(f"Set-based result: {lengthOfLongestSubstring_with_set(text)}")