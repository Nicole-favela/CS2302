#CS2302
#Nicole Favela
#last modified: May 9, 2019
#Lab8
#purpose: to use randomized algorithms to test the equality of
# trigonometric expressions and use backtracking to determine if
# there is a valid partition of sets that equal the same sum
#instructor: Olac Fuentes
#TAs: Anindita Nath and Maliheh Zargaran
import random
import numpy as np
import mpmath

#used to determine if trig expressions are equal
#used in part 1 to test trig expressions
def equal(f1, f2,tries=1000,tolerance=0.0001):
    for i in range(tries):
        t = random.uniform(-(mpmath.pi), mpmath.pi)
        #x = random.random()
        y1 = eval(f1)
        y2 = eval(f2)
        if np.abs(y1-y2)>tolerance:
            return False
    return True
#used for part 2
def subsetsum(S,last,goal):
    if goal == 0:
        return True, []
    if goal<0 or last<0:
        return False, []

    res, subset = subsetsum(S,last-1,goal-S[last]) # Take S[last]
    if res:
        subset.append(S[last])
        return True, subset
    else:
        return subsetsum(S,last-1,goal) # Don't take S[last]
#used for part 2
def partition(s1):
    #checks if sum of s1 is odd, if it is, a partiton with equal sums is not possible
    if sum(s1)%2 != 0:
        return False
    #creates the goal
    goal = sum(s1)//2
    return goal

print()
print('part 1:')
T = ['mpmath.sin(t)','mpmath.cos(t)','mpmath.tan(t)','mpmath.sec(t)','-mpmath.sin(t)','-mpmath.cos(t)','-mpmath.tan(t)','mpmath.sin(-t)','mpmath.cos(-t)','mpmath.tan(-t)','mpmath.sin(t)/mpmath.cos(t)',
     '2*mpmath.sin(t/2)*mpmath.cos(t/2)','mpmath.sin(t)**2','1-mpmath.cos(t)**2','(1-mpmath.cos(2*t))/2','1/mpmath.cos(t)']
count = 0
for i in range(len(T)):
    for j in range(i,len(T)):

        if(equal(T[i], T[j])):
            print('-----------------------------------------------------------------------------------------------------------------------------------------')
            print (T[i],T[j])
            count+=1
print('total true expressions:',count)

print('******************************************************************************************************************************************')
#part 2
print('part 2')
print()

#set S
S = [2, 4, 5, 9, 12]
#p is the goal or false if no partiton possible
p = partition(S)

S2=[]

#returns boolean value res and list s1 which is 1/2 sum of set
res, s1= subsetsum(S,len(S)-1,p)

if p:
    print('s1',s1)
    #creates other partition set
    for j in S:
        if j not in s1:
            #adds values not in s1 to complete partition
            S2.append(j)
    print('s2',S2)
else:
    print('no partition exits')



