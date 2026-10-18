import statistics 
numbers = [3, 1, 5, 2, 4]
result = statistics.median(numbers)
# #regular binary search, but we are searching for the median of two sorted arrays. 
# def binary_search(nums, target):
#     left = 0
#     right = len(nums) - 1
#     while left <= right:
#         mid = (left + right) // 2
#         if nums[mid] == target:
#             return mid
#         elif nums[mid] < target:
#             left = mid + 1
#         else:
#             right = mid - 1
#     return -1

def median_if_partition_valid( num1_left_max : float, num2_left_max : float, num1_right_min : float, num2_right_min : float,  total_count : int,):
    #receives those infinity values as placeholders for missing partition boundaries. 

    print(bool(total_count % 2))
    if total_count % 2: #total is odd, the median is the average of the two middle values.
        return max(num1_left_max, num2_left_max) # so if num1_left_max is infinity, then num2_left_max is the median, and vice versa.
    return (
        max(num1_left_max, num2_left_max)
        + min(num1_right_min, num2_right_min)
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
        #num2_index and num1_index are complementary, meaning that they always add up to the total size of the left partition.
        #they are where the 2 sorted arrays are split 
        # print(f"nums1 left(smaller) partition: {nums1[:num1_index]}")
        # print(f"nums1 right partition: {nums1[num1_index:]}")
        # print(f"nums2 left partition: {nums2[:num2_index]}")
        # print(f"nums2 right partition: {nums2[num2_index:]}")
        # print(f"**************************************")
        # START Getting values at the edges of the partiotions
        # when a partition leaves one side of an array empty, the algorithm uses an infinity placeholder for that missing boundary value:
        num1_left_max = (float("-inf")    if num1_index == 0                         else nums1[num1_index - 1]  ) # max num1 value on left(smaller) side -inf if []
                                                                                                       # its ==0 so we cant subtract 1 so we set it to negative infinity                              
        # negative infinity is used for the left value of the first array when the partition is at the beginning, 
        # This ensures that comparisons can still be made without running into index errors.
        #smalles val left in num1 on bigger right side
        num1_right_min = (float("inf")    if num1_index == shorter_list_length       else nums1[num1_index] )
        # positive infinity is used for the right value of the first array when the partition is at the end. 
        num2_left_max = (float("-inf")   if num2_index == 0                        else nums2[num2_index - 1] )
        num2_right_min = (float("inf")   if num2_index == longer_list_length      else nums2[num2_index]
        )
        # print(num1_left_max)
        # print(num2_left_max)
        # print(num1_right_min)
        # print(num2_right_min)
        # END Getting values at the edges of the partiotions
        # nums1 left(smaller) partition: [1, 3, 4, 5]   /
        # nums1 right partition:                       /  []
        # nums2 left partition:                [2]    /
        # nums2 right partition:                     /    [6, 7, 8, 9]
        # **************************************
        #                                        5    /
        #                                        2  /
        #                                          /    inf
        #                                         /  6
        # True
        # The median of                   [1, 3, 4, 5] and [2, 6, 7, 8, 9] is: 5
        if (  num1_left_max <= num2_right_min  and num2_left_max <= num1_right_min     ):
            #we are comparing the values at the edges of the partitions to ensure that all elements in the left partitions are less than or equal to all elements in the right partitions.
            return median_if_partition_valid( num1_left_max,num2_left_max,num1_right_min,num2_right_min,total_count)

        if num1_left_max > num2_right_min:
            high_num1_index = num1_index - 1  #moving the high index down to search the left side of the first array for a valid partition.
        else:
            low_num1_index = num1_index + 1 #moving the low index up to search the right side of the first array for a valid partition.

    raise ValueError("Both input arrays must be sorted.")

if __name__ == "__main__":
    nums1 = [1, 3,4,5]

    nums2 = [2, 6, 7, 8, 9]
    median = solution(nums1, nums2)
    print(f"The median of {nums1} and {nums2} is: {median}")