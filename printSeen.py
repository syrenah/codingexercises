

def solution(arr=[]):
    
   

    seen = {}

    for index, number  in enumerate(arr): #on
       
        if number not in seen:  # not seen
            seen[number]=index
            print(seen[number])
        else :  # has been seen
            return print(f"the number is {number}")  #return the first repeating element
           
    print(seen)


if __name__ == "__main__":
    solution( arr = [1, 5, 3, 4, 3, 5, 6])