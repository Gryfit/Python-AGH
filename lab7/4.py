# -*- coding: utf-8 -*-

from threading import Thread

import time
import random
import os

################################################################################

def printxy(x,y,s):
  print("\033["+str(y+1)+";"+str(x+1)+"f"+s) #ANSI TERMINAL
# end if

################################################################################

def clrscr():
  print(chr(27)+"[2J")
# end if

################################################################################

class Node(Thread):

  def __init__ (self,n,x,y):
    self.n=n
    self.x=x
    self.y=y
    Thread.__init__(self)
  # end def

  def run(self):
    while (True):
#    for i in range(10):
      time.sleep(1+random.randint(1,5)/10)
      printxy(self.x,self.y," ")
      nx = self.x+random.randint(-1,1) # tylko całkowite
      ny = self.y+random.randint(-1,1)
      if 0<nx<20: self.x = nx
      if 0<ny<20: self.y = ny
      printxy(self.x,self.y,self.n)

    # end while
  # end def

# end class

################################################################################

if __name__ == '__main__':
  clrscr()
  os.system('setterm -cursor off')

  tn = {}

  for n in "ABCDEF":
    tn[n]=Node(n,random.randint(5,20),random.randint(5,20))

  for n in "ABCDEF":
    tn[n].start()

  for n in "ABCDEF":
    tn[n].join()


#  w1 = Node("A",random.randint(5,20),random.randint(5,20))
#  w2 = Node("B",random.randint(5,20),random.randint(5,20))

#  w1.start()
#  w2.start()

#  w1.join()
#  w2.join()

  print("stop")
  os.system('setterm -cursor on')
# end if

################################################################################
