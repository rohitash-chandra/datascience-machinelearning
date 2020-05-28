#!/usr/bin/env python

'''
A Python program  

'''
import numpy as np  
import random
 


def nested_loops():

  print(' nested loops function')

  #https://www.ict.social/python/basics/multidimensional-lists-in-python

  length = 3
  width = 4
  height = 3

  two_dimen = np.random.rand(length, width)


  print(two_dimen)

  first_row = two_dimen[0,:]

  second_col =   two_dimen[:,1] 

  print(first_row, ' first_row') 
  print(second_col, ' second_col') 

  three_dimen = np.zeros((length, width, height))


  print(three_dimen)

  for i in range(length):
    for j in range(width):
      two_dimen[i,j] = i*j

  print (two_dimen)  
 
  print (' 3 nested ')
  for i in range(1,3):
    for j in range(1,3):
      for k in range(1,3):
        z = i*j * k
        print (z)  # end refers new line 

  print (' 3 nested save to np array ')

  for i in range(length):
    for j in range(width):
      for k in range(height):
        three_dimen[i,j,k] = i*j * k
  print(three_dimen)
 
  

 


def main(): 
 
 
    nested_loops()





if __name__ == '__main__':
    main()
