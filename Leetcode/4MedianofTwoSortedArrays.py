import statistics 

numbers = [3, 1, 5, 2, 4]
result = statistics.median(numbers)
#regular binary search, but we are searching for the median of two sorted arrays. 
def binary_search(nums, target):
    left = 0
    right = len(nums) - 1

    while left <= right:
        mid = (left + right) // 2

        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1


def median_if_partition_valid( num1_value_low : float, num2_value_high : float, num1_value_high : float, num2_value_low : float,  total_count : int,):
    #receives those infinity values as placeholders for missing partition boundaries. 

    print(bool(total_count % 2))
    if total_count % 2: #total is odd, the median is the average of the two middle values.
        return max(num1_value_low, num2_value_high) # so if num1_value_low is infinity, then num2_value_high is the median, and vice versa.
    return (
        max(num1_value_low, num2_value_high)
        + min(num1_value_high, num2_value_low)
    ) / 2


#left half needs to be less than or equal to the right half
#median is last element of the left 
    # if left_len + right_len == 0:
    #     raise ValueError("The median is undefined for two empty arrays.")
def solution(nums1, nums2):
    if len(nums1) > len(nums2):
        nums1, nums2 = nums2, nums1

    shorter_list_length = len(nums1)
    longer_list_length = len(nums2)
    total_count = shorter_list_length + longer_list_length
    left_partition_size = (total_count + 1) // 2 #floor of half the total count, ensuring that the left partition 
    # +1 because the left partition  has one more element than the right partition when the total count is odd.
    #THIS VALUE NEVER CHANGES, it is the total number of elements that should be in the left partition when we combine both arrays.
    #The total size of the left partition is fixed. What can vary is how those elements are split between the two arrays:
    #So yes, the left partition could contain only elements from either array
    # but only if that array has enough elements, and only if the resulting split satisfies the sorted-order checks.
    # the leeft_partition contains all thes smaller elements, and the right partition contains all the larger elements. 
    # which maybe all from one array or the other, or a mix of both.

    if total_count == 0:
        raise ValueError("The median is undefined for two empty arrays.")

    low_num1_index = 0
    high_num1_index = shorter_list_length
    #low_num1_index and high_num1_index mark the remaining range of possible partition positions in the first array.


    while low_num1_index <= high_num1_index:
        num1_index = (   low_num1_index + high_num1_index  ) // 2 
        #This calculates the midpoint of the remaining possible partition positions in the first (shorter) array
        num2_index = left_partition_size - num1_index
        
        # START Getting values at the edges of the partiotions
        # when a partition leaves one side of an array empty, the algorithm uses an infinity placeholder for that missing boundary value:
        num1_value_low = (float("-inf")    if num1_index == 0                         else nums1[num1_index - 1]  )
                                                                                                       # its ==0 so we cant subtract 1 so we set it to negative infinity                              
        # negative infinity is used for the left value of the first array when the partition is at the beginning, 
        # This ensures that comparisons can still be made without running into index errors.
        num1_value_high = (float("inf")    if num1_index == shorter_list_length       else nums1[num1_index] )
        # positive infinity is used for the right value of the first array when the partition is at the end. 
        num2_value_high = (float("-inf")   if num2_index == 0                        else nums2[num2_index - 1] )
        num2_value_low = (float("inf")   if num2_index == longer_list_length      else nums2[num2_index]
        )
        # print(num1_value_low,num2_value_high,num1_value_high,num2_value_low)
        # END Getting values at the edges of the partiotions

        if (  num1_value_low <= num2_value_low  and num2_value_high <= num1_value_high     ):
            #we are comparing the values at the edges of the partitions to ensure that all elements in the left partitions are less than or equal to all elements in the right partitions.
            return median_if_partition_valid( num1_value_low,num2_value_high,num1_value_high,num2_value_low,total_count)

        if num1_value_low > num2_value_low:
            high_num1_index = num1_index - 1  #moving the high index down to search the left side of the first array for a valid partition.
        else:
            low_num1_index = num1_index + 1 #moving the low index up to search the right side of the first array for a valid partition.

    raise ValueError("Both input arrays must be sorted.")

if __name__ == "__main__":
    nums1 = [1, 3]

    nums2 = [2]
    median = solution(nums1, nums2)
    print(f"The median of {nums1} and {nums2} is: {median}")