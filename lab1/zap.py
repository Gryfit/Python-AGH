#!/usr/bin/python3
from p2 import sp
for i in range(1, 100000):
  j = sp(i)
  k = sp(j)
  if i == k and i !=j:
    print(i,j)
print("END")
