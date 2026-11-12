def solution(arr=[]):
    
   sc = 0 
   sr= 0 
   er = len(arr)-1
   ec = len(arr[0])-1


   while sc <=ec and sr <=er:

       # 0,0  0,1  0,2
       #left > right
       for x in range(sc,ec+1):
        #    print(str(sc) + "," + str(x))
           print(arr[sc][x])

       sr+=1 #killed the top row

       #top > bottom (leftside) left most column

       for r in range(sr,er+1):
        #    print(str(x) + "," + str(r))
           print(arr[r][ec])

       ec-=1

       # right > left (bottom row)
       # flipping through columns 
       if sr <= er:
           for x in range(ec,sc-1,-1):
            #    print(str(er) + "," + str(x))
               print(arr[er][x])

           er-=1

         # bottom > top (left side)
       if sc <= ec:
            for r in range(er,sr-1,-1):
                #    print(str(x) + "," + str(r))
                print(arr[r][sc])
    
            sc+=1
       

if __name__ == "__main__":
    solution( arr = [[1, 2, 3],
                     [ 8, 9, 4],
                     [ 7, 6, 5]])