def median_if_partition_valid( num1_left_max : float, num2_left_max : float, num1_right_min : float, num2_right_min : float,  total_count : int,):
    if total_count % 2: 
        return max(num1_left_max, num2_left_max) 
    return (
        max(num1_left_max, num2_left_max)
        + min(num1_right_min, num2_right_min)
    ) / 2

def solution(nums1, nums2):
    if len(nums1) > len(nums2):
        nums1, nums2 = nums2, nums1 # binary search runs on smaller array 

    total_count = len(nums1) + len(nums2)
    left_partition_size = (total_count + 1) // 2 

    low_num1_index = 0
    high_num1_index = len(nums1)

    while low_num1_index <= high_num1_index:
        num1_index = (   low_num1_index + high_num1_index  ) // 2 
        num2_index = left_partition_size - num1_index

        num1_left_max = (float("-inf")    if num1_index == 0                else nums1[num1_index - 1]  ) 
        num1_right_min = (float("inf")    if num1_index == len(nums1)       else nums1[num1_index] )
        num2_left_max = (float("-inf")    if num2_index == 0                else nums2[num2_index - 1] )
        num2_right_min = (float("inf")    if num2_index == len(nums2)       else nums2[num2_index] )
  
        if (  num1_left_max <= num2_right_min  and num2_left_max <= num1_right_min     ):
            return median_if_partition_valid( num1_left_max,num2_left_max,num1_right_min,num2_right_min,total_count)
        
        elif num1_left_max > num2_right_min:
            high_num1_index = num1_index - 1  
        elif num2_left_max > num1_right_min:
            low_num1_index = num1_index + 1 

if __name__ == "__main__":
    nums1 = [1, 3,4,5]
    nums2 = [2, 6, 7, 8, 9]
    median = solution(nums1, nums2)
    print(f"The median of {nums1} and {nums2} is: {median}")