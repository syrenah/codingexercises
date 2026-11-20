import heapq

class Solution(object):
    def topKFrequent(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: List[int]
        """
        ans=[]
        freq = {}

        for n in nums:
            if n not in freq:
                freq[n]=1
            else:
                freq[n]=freq[n]+1
        
        #value is key
        for key,value in freq.items():
            if len(ans)<k:
                heapq.heappush(ans,[value,key])
            else:
                heapq.heappushpop(ans,[value,key])
        
        return [key for value,key in ans]
        