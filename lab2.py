#CS2302
#Nicole Favela
#Lab2
#instructor: Olac Fuentes
#TAs: Anindita Nath and Maliheh Zargaran

import random
size = 0
import copy
#Node Functions
class Node(object):
    # Constructor
    def __init__(self, item, next=None):  
        self.item = item
        self.next = next 
        
def PrintNodes(N):
    if N != None:
        print(N.item, end=' ')
        PrintNodes(N.next)
        
def PrintNodesReverse(N):
    if N != None:
        PrintNodesReverse(N.next)
        print(N.item, end=' ')
        
#List Functions
class List(object):   
    # Constructor
    def __init__(self): 
        self.head = None
        self.tail = None
        
def IsEmpty(L):  
    return L.head == None     
        
def Append(L,x): 
    global size
    # Inserts x at end of list L
    
    if IsEmpty(L):
        size+=1
        L.head = Node(x)
        L.tail = L.head
    else:
        size+=1
        L.tail.next = Node(x)
        L.tail = L.tail.next
        
def Print(L):
    # Prints list L's items in order using a loop
    temp = L.head
    while temp is not None:
        print(temp.item, end=' ')
        temp = temp.next
    print()  # New line 

def PrintRec(L):
    # Prints list L's items in order using recursion
    PrintNodes(L.head)
    print() 
    
def Remove(L,x):
    # Removes x from list L
    # It does nothing if x is not in L
    if L.head==None:
        return
    if L.head.item == x:
        if L.head == L.tail: # x is the only element in list
            L.head = None
            L.tail = None
        else:
            L.head = L.head.next
    else:
         # Find x
         temp = L.head
         while temp.next != None and temp.next.item !=x:
             temp = temp.next
         if temp.next != None: # x was found
             if temp.next == L.tail: # x is the last node
                 L.tail = temp
                 L.tail.next = None
             else:
                 temp.next = temp.next.next
         
def PrintReverse(L):
    # Prints list L's items in reverse order
    PrintNodesReverse(L.head)
    print()   
    
#gets length of list
def getLength(L):
    temp = L.head
    count = 0
    while temp is not None:
        count = count+1
        temp = temp.next
    return count

#gets element at specific index
def getElementAt(L,i):
    index = 0
    temp = L.head
    while temp != None:
        if index == i:
            return temp.item
        index = index+1
        temp = temp.next
        
#get median element of list
def Median(L):
    C = copy.copy(L)
    temp = (getLength(C))//2
    return temp

#get median element of list for bubblesort
def Median1(L):
    C = copy.copy(L)
    bubblesort(C)
    temp = (getLength(C))//2
    return temp

#get median element of list for merge
def Median2(L):
    C = copy.copy(L)
    mergeSort(C.head)
    temp = (getLength(C))//2
    return temp

#get median element of list for quick
def Median3(L):
    C = copy.copy(L)
    quicksort(C)
    temp = (getLength(C))//2
    return temp

#combines lists
def mergeLists(L1, L2):
    temp = None
    if L1 is None: #if one list in None returns other
        return L2
    if L2 is None:
        return L1
    if L1.item <= L2.item: #compares items
        temp = L1 #stores temp and calls mergeList on rest of list
        temp.next = mergeLists(L1.next, L2)
    else:
        temp = L2
        temp.next = mergeLists(L1, L2.next) #stores temp and moves to l2
    return temp

#merge sorts list 
def mergeSort(head):
    if head is None or head.next is None:
        return head
    L1, L2 = divideLists(head) #calls divideList
    L1 = mergeSort(L1) #recursive call to l1
    L2 = mergeSort(L2) #recursive call to l2
    head = mergeLists(L1, L2) #returns head of merged list
    return head

#divides list for mergesort
def divideLists(head):
    curr = head                     
    quick = head                    
    if quick:
        quick = quick.next  #starts at next element         
    while quick:
        quick = quick.next  #moves to next next element        
        if quick: #if fast is not None
            quick = quick.next #move to next
            curr = curr.next
    mid = curr.next
    curr.next = None
    return head, mid      
 
#quicksorts L recursively  
def quicksort(L):
    if getLength(L) > 1: #List of length 1 is already sorted
         L2 = List() #less than pivot
         L3 = List() #greater than pivot
         currpivot = L.head.item #pivot value
         temp = L.head.next #used to iterate
        
         while temp is not None:
             if currpivot > temp.item: #appends smaller items to L2
                x = temp.item
                Append(L2,x)
             else:
                x = temp.item #creates list of items greater
                Append(L3,x)
             temp = temp.next
         quicksort(L2) #recursively gets rest of lists
         quicksort(L3)
         #puts pivot in correct location
         if L2.head != None:
             prepend(L3,currpivot)
         else:
             Append(L2,currpivot)
         if L2.head != None: #connects lists
             L.head = L2.head
             L.tail = L3.tail
             L2.tail.next = L3.head
         else:
             L.head = L3.head
             L.tail = L3.tail
     
#modied quicksort           
def ModQuickSort(L,mid):
    if IsEmpty(L):
        return
    else:
        lo = List() #strores items less than pivot
        maximum = List() #stores items greater than pivot 
        pivot=L.head.item #pivot is first item
        temp=L.head.next 
        while temp!=None:
            if pivot<temp.item: # if item is bigger tha pivot
                Append(lo,temp.item) #stores larger item in greater list
            else:
                Append(maximum, temp.item)
            temp=temp.next #moves to next
        if getLength(lo)>mid: #if length of least is greater than index of mid
            return ModQuickSort(lo,mid) # get middle of smaller list
        elif (getLength(lo))==mid: #if they are equal
            return pivot #return pivot value
        else:
            return ModQuickSort(maximum,mid-getLength(lo)-1)
        
#adds item to beginning of list
def prepend(L,x):
    if L.head is None:
        L.head = Node(x)
        L.tail = Node(x)
    else:
        newNode = Node(x)
        newNode.next = L.head
        L.head = newNode

#bubble sorts list
def bubblesort(L):
    if IsEmpty(L): #if list is empty return
        return
    exchanged = False #checks for exchanges
    temp=L.head
    while temp.next is not None:
        if temp.item>temp.next.item: #compares adjacent elements
            temp2=temp.item #stores that element in temp
            temp.item=temp.next.item #swaps
            temp.next.item=temp2
            exchanged= True
        temp=temp.next #noves to next
    if exchanged == True:
        bubblesort(L)   #recursively goes though list

#creates lists 
        
L1 = List()    
for i in range(5): #populates list
    t = random.randrange(100)
    Append(L1,t)
L2 = List()    
for i in range(5): 
    t = random.randrange(100)
    Append(L2,t)
L3 = List()    
for i in range(5):
    t = random.randrange(100)
    Append(L3,t)
L4= List()    
for i in range(5):
    t = random.randrange(100)
    Append(L4,t)

print('************************************')
Print(L1)
print('************************************')

print('printing merge sorted list')
L1.head = mergeSort(L1.head)

Print(L1)
print('************************************')
print('printing bubble sorted list:')
bubblesort(L2)
Print(L2)
print('************************************')
print('before quicksort')
Print(L3)
print('quicksorting list')
C = copy.copy(L3)
quicksort(C)

Print(C)
print('************************************')
mid = getLength(L4)//2
print('list before modquicksort')
Print(L4)
print('mod quicksorting list')
print(ModQuickSort(L4,mid))
print('mergesort median')
print(getElementAt(L1,Median1(L1)))
print('bubblesortlist')
Print(L2)
print('bubblesort median')
print(getElementAt(L2,Median2(L2)))
print('quicksort list')
Print(L3)
print('quicksort median')
print(getElementAt(L3,Median3(L3)))

