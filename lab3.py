
#CS2302
#Nicole Favela
#last modified: March 8, 2019
#Lab3
#instructor: Olac Fuentes
#TAs: Anindita Nath and Maliheh Zargaran
import math
import numpy as np
import matplotlib.pyplot as plt


class BST(object):
    # Constructor
    def __init__(self, item, left=None, right=None):  
        self.item = item
        self.left = left 
        self.right = right      
        
def Insert(T,newItem):
    if T == None:
        T =  BST(newItem)
    elif T.item > newItem:
        T.left = Insert(T.left,newItem)
    else:
        T.right = Insert(T.right,newItem)
    return T

def Delete(T,del_item):
    if T is not None:
        if del_item < T.item:
            T.left = Delete(T.left,del_item)
        elif del_item > T.item:
            T.right = Delete(T.right,del_item)
        else:  # del_item == T.item
            if T.left is None and T.right is None: # T is a leaf, just remove it
                T = None
            elif T.left is None: # T has one child, replace it by existing child
                T = T.right
            elif T.right is None:
                T = T.left    
            else: # T has two chldren. Replace T by its successor, delete successor
                m = Smallest(T.right)
                T.item = m.item
                T.right = Delete(T.right,m.item)
    return T
         
def InOrder(T):
    # Prints items in BST in ascending order
    if T is not None:
        InOrder(T.left)
        print(T.item,end = ' ')
        InOrder(T.right)
  
def InOrderD(T,space):
    # Prints items and structure of BST
    if T is not None:
        InOrderD(T.right,space+'   ')
        print(space,T.item)
        InOrderD(T.left,space+'   ')
  
def SmallestL(T):
    # Returns smallest item in BST. Returns None if T is None
    if T is None:
        return None
    while T.left is not None:
        T = T.left
    return T   
 
def Smallest(T):
    # Returns smallest item in BST. Error if T is None
    if T.left is None:
        return T
    else:
        return Smallest(T.left)

def Largest(T):
    if T.right is None:
        return T
    else:
        return Largest(T.right)   

def Find(T,k):
    # Returns the address of k in BST, or None if k is not in the tree
    if T is None or T.item == k:
        return T
    if T.item<k:
        return Find(T.right,k)
    return Find(T.left,k)
    
def FindAndPrint(T,k):
    f = Find(T,k)
    if f is not None:
        print(f.item,'found')
    else:
        print(k,'not found')

#iterative search for part 2
def IterativeFind(T,k):
    # Returns the address of k in BST, or None if k is not in the tree
    if T is None or T.item == k:
        return T
   
    while T is not None:
        if k > T.item:
            T = T.right
        elif k < T.item:
            T = T.left
        elif k == T.item:
            print('key found')
            return T
        else:
            print('key not found')
            return None
          
#part 3     
#builds a bst from sorted array
def buildBST(A):
    if not A:
        return None
    
    middle = (len(A))//2
    root = BST(A[middle]) #makes root the middle element
    root.left = buildBST(A[:middle]) #makes items less than left the, L subtree
    
    root.right = buildBST(A[middle+1:]) #makes items greater, the R subtree
    return root #returns reference to root

##part 4
#extracts the elements of bst in order
def extractInOrder(T,arr):
    if T is not None:
        extractInOrder(T.left,arr)
        arr+=[T.item] #accumulates data in array
        extractInOrder(T.right,arr)
        return arr #returns array

###############################################
#prints all nodes at a every depth for part 5
def ShowDepths(T):
    counter=DepthCounter(T) #gets the depth of the tree
    for i in range(counter): #prints cycled index and calls method to print keys at certain level
        print('keys at depth',i,':',end=' '),findAtLevel(T,i)
        print()
    
def DepthCounter(T):
    if T is None:
        return 0
    CountL=DepthCounter(T.left) #gets count of depth in L tree
    CountR=DepthCounter(T.right) #gets count of depth in R tree
    if CountL>CountR:
        return 1+CountL #returns larger count
    return 1+CountR
#gets items at particular depths 
def findAtLevel(T,Height):
    if T is None:
        return
    if Height==0:
        print(T.item,end=' ')
    else:
        findAtLevel(T.left,Height-1)
        findAtLevel(T.right,Height-1)
        
####################################################
#finds the max depth of the tree
def countDepth(T):
    if T is None:
        return 0
    
    else:
        depthOfLeft = 1+countDepth(T.left)
        depthOfRight = 1+countDepth(T.right)
        if depthOfLeft < depthOfRight:
            return depthOfRight-1 
        else:
            return depthOfLeft
    
#part 1 dispay figure 
###################################################
def DrawTree(ax,x,y,size,depth,T):
    rad = 4
    if T is not None:
        draw_circle(ax,[x,y],rad)
        ax.text(x+2.2,y-1.8,T.item,size=10)
    if T.left is not None:
        draw_line(ax,x,y,x-(2.5**depth),y-10)
        DrawTree(ax,x-(2.5**depth),y-10,size,depth-1,T.left)
    if T.right is not None:
        draw_line(ax,x+rad*2,y,x+(2.5**depth),y-10)
        DrawTree(ax,x+(2.5**depth),y-10,size,depth-1,T.right)
#draws lines equidistant aprt      
def draw_line(ax, x1,y1,x2,y2):
    n = int(max( abs(x1-x2), abs(y1-y2)) )#the range of the lines
    x = np.linspace(x1,x2,n)
    y = np.linspace(y1,y2,n)
    ax.plot(x,y,color='k')

def draw_circle(ax,center,radius):
    x,y = circle(center,radius)
    ax.plot((x+radius),y,color=(0,0,0))


def circle(center,rad):
    n = int(4*rad*math.pi)#radius of each circle
    t = np.linspace(0,6.3,n)#creating the circles
    x = center[0]+rad*np.sin(t)
    y = center[1]+rad*np.cos(t)
    return x,y 
###################################################
T = None
A = [10,4,15,2,8,12,18,1,3,5,9,7]
sortedArray = [1,2,3,4,6,7,8,9]

#creates tree form array A
for a in A:
    T = Insert(T,a)
    
InOrder(T)

#part 2 iterative search
result = IterativeFind(T,9)

print()

#returns the total depth of the tree
depthMax = countDepth(T)
print('depth of tree is:', depthMax)
print()

#draws tree image in graph
fig, ax = plt.subplots()
ax.set_aspect(1.0)
#draws tree for part 1
DrawTree(ax,0,0,30,depthMax,T)

plt.show()
plt.axis('off')
print()

#part 4 extracting elements form BST to create array of sorted items
extractionArray = []
array = extractInOrder(T,extractionArray)

print('printing array extracted from bst:')
print(array)
print()
    
#part 5
ShowDepths(T)

#part 3 builds bst form sorted array
print('building bst from sorted array')
T = buildBST(sortedArray)
InOrderD(T,' ')

