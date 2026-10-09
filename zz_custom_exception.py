from typing import Any
import pickle
class MyError(Exception):
    """Base class for other exceptions"""
    def __init__(self,message:str,value:Any)->None:
        super().__init__(message)
        self.value = value
        self.message = message
    
    #dunder methods

    def __str__(self) ->str: #used for human readable or display to users
        return f'{self.message} (value: {self.value}) anything else i want to add to the string representation of the error'

    def __reduce__(self) -> tuple[Any,tuple[str,Any]]:
         return self.__class__,(self.message,self.value)

    def __repr__(self) -> str: #used for debugginfg and logging, used for developers fallback to __str__ if not implemented
        return f"MyClass ( {self.__class__.__name__}({self.message!r}, {self.value!r})"


myexception: MyError =MyError(message='cusomt_text',value=137)

myexception2: MyError =MyError('cusomt_text',199)

print(myexception)  # Output: cusomt_text (value: 137)
print(repr(myexception))  # Output: MyError('cusomt_text', 137)
print(myexception2)  # Output: cusomt_text (value: 137)
print(repr(myexception2))  # Output: MyError('cusomt_text', 137)

try:
    raise MyError("An error occurred", 42) 
except MyError as e:
        print(f"caught some error: {e}")
        print(f"error value: {e.value}")
        print(f"error message: {e.message}")

oe: MyError = MyError("Anything i want", 9999)
print(f' representation:{repr(oe)}') # no vlaue

pickled:bytes = pickle.dumps(oe)
unpickled :MyError = pickle.loads(pickled)
print(f"unpickled error: {unpickled.value}")