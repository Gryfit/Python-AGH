#!/usr/bin/python3
#from math import * # nie zalecane
#from math import sqrt
#import math
import math as M
a = float(input("a="));
b = float(input("b="));
c = float(input("c="));
# 3.
# input() -> str
# print() jest funkcją
# 2. 
# input() -> int
# rawinput() -> str
# print nie jest funkcją, operator/ chuj wie co xd 

d = b**2 - 4*a*c
if d >= 0 :
  p = M.sqrt(d)
  x1 = (-b-p)/(2*a)
  x2 = (-b+p)/(2*a)
  print("x1 = ", x1, "x2 = ", x2)
  print("x1 = %0.4f"%x1)
  print("x1 = {:0.4f}".format(x1))
else:
  print("brak rozwiązań")
#endif -> wygodne ale nie konieczne

#eval("math."+ dir(math)[-5] +"(2)" ) ==> sqrt(2)


