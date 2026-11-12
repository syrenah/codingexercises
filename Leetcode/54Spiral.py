def solution(arr=[]):   
   if len(arr) == 0:
            return [] 
   sc = 0 
   sr= 0 
   er = len(arr)-1
   ec = len(arr[0])-1
   
   while sc <=ec and sr <=er:

       #left > right
       for x in range(sc,ec+1):
           print(arr[sr][x])

       sr+=1 #killed the top row

       #top > bottom (leftside) left most column
       for x in range(sr,er+1):
           print(arr[x][ec])

       ec-=1 # moving the right column left

       # right > left (bottom row)
       if sr <= er:
           for x in range(ec,sc-1,-1):
               print(arr[er][x])

           er-=1 # moving the bottom row up

         # bottom > top (left side)
       if sc <= ec:
            for x in range(er,sr-1,-1):
                print(arr[x][sc])
    
            sc+=1 #moving the left column right
       
if __name__ == "__main__":
    solution( arr = [[1, 2, 3],
                     [ 8, 9, 4],
                     [ 7, 6, 5]])