

##CS2302
#Nicole Favela
#last modified: April 3, 2019
#Lab5
#purpose: to compare runtimes of 2 implementaions of tables and compute similarities of embeddings 
#and to practice working with hash tables and binary search trees 
#instructor: Olac Fuentes
#TAs: Anindita Nath and Maliheh Zargaran


#import numpy as np
import math
import time

#BST constructor
class BST(object):
    # Constructor
    def __init__(self, item, left=None, right=None):  
        self.item = item
        self.left = left 
        self.right = right   
        
#inserts new items to bst
def Insert(T,newItem):
    if T == None:
        T =  BST(newItem)
    elif (T.item[0])> (newItem[0]):
        T.left = Insert(T.left,newItem)
    else:
        T.right = Insert(T.right,newItem)
    return T
#prints structure of bst
def InOrderD(T,space):
    # Prints items and structure of BST
    if T is not None:
        InOrderD(T.right,space+'   ')
        print(space,T.item)
        InOrderD(T.left,space+'   ')
#BST 
def bstImplementation():
     try:
        with open("glove.6B.50d.txt",encoding='utf-8') as f:
            line=f.readline()
            T=None
            while line:
                lists=[]
                lists=line.split(" ")
                if lists[0].isalpha():
                    embedding=((lists[1:]))
#                    embedding=[float(i) for i in embedding]
                    T=Insert(T,(lists[0],embedding))
                line=f.readline()
            return T
     except:
       print("File not found")
# Implementation of hash tables with chaining using strings       
class HashTableC(object):
    # Builds a hash table of size 'size'
    # Item is a list of (initially empty) lists
    # Constructor
    def __init__(self,size):  
        self.item = []
        for i in range(size):
            self.item.append([])
        
def InsertC(H,k,l):
    # Inserts k in appropriate bucket (list) 
    # Does nothing if k is already in the table
    b = h(k,len(H.item))
    H.item[b].append([k,l]) 
   
def FindC(H,k):
    # Returns bucket (b) and index (i) 
    # If k is not in table, i == -1
    b = h(k,len(H.item))
    for i in range(len(H.item[b])):
        if H.item[b][i][0] == k:
            return b, i, H.item[b][i][1]
    return b, -1, -1
#hashes based on ascii
def h(s,n):
    r = 0
    for c in s:
        r = (r*n + ord(c))% n
    return r
#counts lines in file to test
def countlines():
    count = 0
    filename = "glove.6B.50d.txt"
    with open(filename,encoding='utf-8') as f:
        for line in f:
            count+=1
    return count
#gets dot product for e0 and e1
def dotProduct(emb):
     mag = vectorMagnitudes(emb,emb)
     total = 0
     for i in range (len(emb)):
         total+= (mag)*(mag)
     return total
#computes the magnitudes of the items 
def vectorMagnitudes(e0,e1):
    sum = 0
    mag = 0
    for i in e0:
        sum += ((e0[i])**2) + ((e1[i])**2)    
    mag = math.sqrt(sum)
    return mag
    
#get similarities
def computeSimilaritiesForHash(w0,w1):
    #FindC(H,k)
    sim = 0
    w0 = Find(H,w0)
    w1 = Find(H,w1)
    sim = dotProduct(w0,w1)/(vectorMagnitudes(w0,w1))
    return sim
#gets similities for bst
def computeSimilaritiesForBST(w0,w1):
   
    sim = 0
    w0 = Find(T,w0) #finds w0 in tree
    w1 = Find(T,w1)
    sim = dotProduct(w0,w1)/(vectorMagnitudes(w0,w1)) #computes the dot product
    return sim

#reads file of pairs for comparison and compares similarities
def CompareWithBST(T):
     try:
        with open("similarities.txt",encoding='utf-8') as f:       
            line= f.readline()
            while line:
                lists=[]
                lists=line.split(" ")
                #finds words in tree
                w0 = Find(T, lists[0])
                w1 =Find(T,lists[1])
#                sim = computeSimilaritiesForBST(w0,w1)
#                print('similarites are: ',sim)
                line=f.readline() 
     except: 
        print('file not found')
     finally:
        f.close()      
#doubles size of hash table
def doubleSize(H):
        H2=HashTableC(2*len(H.item)+1)
        for i in range(len(H.item)):
            for j in range(len(H.item[i])):
                #rehashes values
                InsertC(H2,((H.item[i])[j])[0], ((H.item[i])[j])[1])
        return H2  

#computes load factor for hash
def loadfactor(H):
    if H is None:
        return -1
    counter = 0
    for i in range(len(H.item)): #goes through len of hash and adds to counter
        counter+=len(H.item[i])
    return counter/len(H.item)

#counts all nodes in bst
def countAllNodes(T):
    if T is None:
        return 0
    else: #count nodes of L and nodes of R
        return 1 +  countAllNodes(T.left)+ countAllNodes(T.right)
#gets height of bst
def DepthCounter(T):
    if T is None:
        return 0
    CountL=1
    CountR=1
    CountL+=DepthCounter(T.left) #gets count of depth in L tree
    CountR+=DepthCounter(T.right) #gets count of depth in R tree
    if CountL>CountR:
        return 1+CountL #returns larger count
    return 1+CountR

#find for bst
def Find(T,k):
    # Returns the address of k in BST, or None if k is not in the tree
    if T is None or str(T.item[0]) == str(k):
        return T
    #compares order to determine location
    if str(T.item[0])<str(k):
        #checks right
        return Find(T.right,k)
    return Find(T.left,k)
#gets percentage empty of hash
def percentageOfEmptyLists(H):
    empty=0 
    for i in H.item:
        if len(i)==0: # if empty add to counter
            empty+=1
    empty=empty/2    #list double size needed
    return (empty/len(H.item))*100 # multiply by 100 to get percentage
#hash table implementation
def HashImplementation():
    try:
        # reads file
        with open("glove.6B.50d.txt",encoding='utf-8') as f:
            line= f.readline()
            word=[]
            embedding=[]
            while line:
                lists=[]
                lists=line.split(" ")
                if lists[0].isalpha():
                    #stores words
                    word.append(lists[0])
                    #stores embeddings
                    embedding = lists[1:]
                    #inserts word followed by embedding in hash
                    InsertC(H,lists[0],embedding)
                    
                line=f.readline()
            return H
 
    except IOError:
        print('file not found')
    finally:
        f.close()
   

##menu
print('choose a table implementaion:')
#prompt user
print('1. binarysearch tree ')
print('2. hash table with chaining ')
#get choice input
choice = int(input('select one: '))
if choice == 1:
     print('building binary search tree')
     start = time.time() 
     T = bstImplementation()
     end= time.time() 
     print('running time for bst construction:',end - start)
     print()
     print('height:')
     print(DepthCounter(T))
     print()
     print('the number of nodes are:')
     print(countAllNodes(T))
     print()
   
     print('reading word file to determine similarities')
     
#     print(CompareWithBST(T))
   

#reads file
if choice == 2:
    H = HashTableC(97)
    print('hash table stats:')
    start = time.time() 
    H=HashImplementation()
    end= time.time() 
    print('running time for hashing:',end - start)
    print()

    print('Initial table size')
    print(len(H.item))
    print()
    
    print('Final table size:')
    while loadfactor(H)>=1:
        H=doubleSize(H)
    print(len(H.item))
    print()
    
    print('Load factor:')
    print(loadfactor(H))
    print()
    
    
    
    print('percentage of empty lists:',percentageOfEmptyLists(H))
    
    