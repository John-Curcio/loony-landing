import math
#returns the dot product of A and B
#assuming A and B are vectors of the same length
def dot(A,B):
    dotProduct = 0
    for x in range(0,len(A)):
        dotProduct += (A[x] * B[x])
    return dotProduct


#returns a list B where every index of a 
#list A multiplied by a constant c
def scal_prod(c,A):
    B = []
    for x in A:
        B += [c * x]
    return B


#returns the magnitude of a vector A
def mag(A):
    sum = 0
    for x in A:
        sum += x**2
    return math.sqrt(sum)


#returns the sum of the vectors
def add(A,B):
    C = []
    for x in range(len(A)):
        C += [A[x]+B[x]]
    return C


#returns the vector projection of A onto B
def proj(A,B):
    return scal_prod(dot(A,B)/(mag(B)**2),B)


#returns a unit vector in the same direction of A
def unit_of(A):
    return scal_prod(1/mag(A),A)


#returns the determinant of a 2x2 matrix 
def det2x2(A,B):
    return (A[0]*B[1]-A[1]*B[0])

#finds the cross product of a 3x3 matrix
def cross(A,B):
    C = [] +[A[0]] + [A[2]]
    D = [] +[B[0]] + [B[2]]
    return [det2x2(A[1:3],B[1:3]),-det2x2(C,D),det2x2(A[0:2],B[0:2])]