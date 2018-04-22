#!/usr/bin/python3
def sp(n):
  sum=1
  p=2
  while p*p<n:
    if n%p ==0: sum = sum+p+n//p
    p+=1
  #endwhile
  if p*p==n:
    sum +=p
  return sum
#enddef

if  __name__ == "__main__" :
  for i in range(1,30): #od 1 do 30 bez 30
    if sp(i)==i:
      print(i)

#po drugich ćwiczeniach będzie zadanie stanowi sposób zaliczenia

