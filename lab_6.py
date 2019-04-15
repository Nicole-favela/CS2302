#CS2302
#Nicole Favela
#last modified: April 14, 2019
#Lab6
#purpose: to build a maze using disjoint set forests and to compare runtimes of union by size and regular union functions
#instructor: Olac Fuentes
#TAs: Anindita Nath and Maliheh Zargaran

# Starting point for program to build and draw a maze
# Modify program using disjoint set forest to ensure there is exactly one
# simple path joiniung any two cells
# Programmed by Olac Fuentes
# Last modified March 28, 2019

import random
from matplotlib import pyplot as plt
import numpy as np
import time

def DisjointSetForest(size):
    return np.zeros(size,dtype=np.int)-1

def find(S,i):
    # Returns root of tree that i belongs to
    if S[i]<0:
        return i
    return find(S,S[i])

#Find with path compression
def find_c(S,i):
    if S[i]<0:
        return i
    r = find_c(S,S[i])
    S[i] = r
    return r

#counts the number of sets in the dsf
def numSets(S):
    count = 0
    for i in range (len(S)):
        if S[i] <0 or S[i] == i:
            count+=1
    return count

#joins sets
def union(S,i,j):
    # Joins i's tree and j's tree, if they are different
    ri = find(S,i)
    rj = find(S,j)
    if ri!=rj: # Do nothing if i and j belong to the same set
        S[rj] = ri  # Make j's root point to i's root

#union by compression
def union_c(S,i,j):
    # Joins i's tree and j's tree, if they are different
    # Uses path compression
    ri = find_c(S,i)
    rj = find_c(S,j)
    if ri!=rj:
        S[rj] = ri
#union by size
def union_by_size(S,i,j):
    # if i is a root, S[i] = -number of elements in tree (set)
    # Makes root of smaller tree point to root of larger tree
    # Uses path compression
    ri = find_c(S,i)
    rj = find_c(S,j)
    if ri!=rj:
        if S[ri]>S[rj]: # j's tree is larger
            S[rj] += S[ri]
            S[ri] = rj
        else:
            S[ri] += S[rj]
            S[rj] = ri


def draw_maze(walls,maze_rows,maze_cols,cell_nums=False):
    fig, ax = plt.subplots()
    for w in walls:
        if w[1]-w[0] ==1: #vertical wall
            x0 = (w[1]%maze_cols)
            x1 = x0
            y0 = (w[1]//maze_cols)
            y1 = y0+1
        else:#horizontal wall
            x0 = (w[0]%maze_cols)
            x1 = x0+1
            y0 = (w[1]//maze_cols)
            y1 = y0
        ax.plot([x0,x1],[y0,y1],linewidth=1,color='k')
    sx = maze_cols
    sy = maze_rows
    ax.plot([0,0,sx,sx,0],[0,sy,sy,0,0],linewidth=2,color='k')
    if cell_nums:
        for r in range(maze_rows):
            for c in range(maze_cols):
                cell = c + r*maze_cols
                ax.text((c+.5),(r+.5), str(cell), size=10,
                        ha="center", va="center")
    ax.axis('off')
    ax.set_aspect(1.0)

def wall_list(maze_rows, maze_cols):
    # Creates a list with all the walls in the maze
    w =[]
    for r in range(maze_rows):
        for c in range(maze_cols):
            cell = c + r*maze_cols
            if c!=maze_cols-1:
                w.append([cell,cell+1])
            if r!=maze_rows-1:
                w.append([cell,cell+maze_cols])
    return w

#builds maze
def buildMaze():
    while numSets(S) > 1:
        #d is a random integer in range of walls
        d = random.randint(0, len(walls) - 1)
        #wall is an list location in walls at d
        wall = walls[d]
        #grabs coordinates for cells
        c1 = wall[0]
        c2 = wall[1]
        #if not in same set
        if find(S,c1)!= find(S,c2):
            union(S,c1,c2) #make part of same set
            walls.pop(d) #remove wall


#builds maze with union with compression
def buildMaze_withCompresssion():
    while numSets(S) > 1:
        # d is a random integer in range of walls
        d = random.randint(0, len(walls) - 1)
        # wall is an list location in walls at d
        wall = walls[d]
        # grabs coordinates for cells
        c1 = wall[0]
        c2 = wall[1]
        #if not in same set
        if find_c(S,c1)!= find_c(S,c2):
            union_c(S,c1,c2) #make part of same set
            walls.pop(d) #remove wall

def buildMaze_with_union_by_size():
    while numSets(S) > 1:
        # d is a random integer in range of walls
        d = random.randint(0, len(walls) - 1)
        # wall is an list location in walls at d
        wall = walls[d]
        # grabs coordinates for cells
        c1 = wall[0]
        c2 = wall[1]
        #if not in same set
        if find_c(S,c1)!= find_c(S,c2):
            union_by_size(S, c1, c2) #make part of same set
            walls.pop(d) #remove wall


plt.close("all")

maze_rows = 10
maze_cols = 15

#creates dsf of 150
S = DisjointSetForest(maze_rows*maze_cols)
#creates array of walls
walls = wall_list(maze_rows,maze_cols)
#draws empty maze
draw_maze(walls,maze_rows,maze_cols,cell_nums=True)

#records time taken to build maze
start = time.time()
buildMaze()
draw_maze(walls,maze_rows,maze_cols)
end = time.time()

print('time taken to build maze using regular union:', end-start)
#shows that the maze is one set
print('the number of sets in maze 1:')
print(numSets(S))
print()

#creates dsf for maze for union by size
S = DisjointSetForest(maze_rows*maze_cols)
#creates array of walls
walls = wall_list(maze_rows,maze_cols)
start = time.time()
buildMaze_withCompresssion()
draw_maze(walls,maze_rows,maze_cols)
end = time.time()

print('the number of sets in maze 2 (withCompresssion):')
print(numSets(S))
print('time taken to build maze using union by compression:', end-start)
print()

S = DisjointSetForest(maze_rows*maze_cols)
#creates array of walls
walls = wall_list(maze_rows,maze_cols)
start = time.time()
#builds maze using union by size
buildMaze_with_union_by_size()
draw_maze(walls,maze_rows,maze_cols)
end = time.time()

print('the number of sets in maze 3 (union_by_size):')
print(numSets(S))
print('time taken to build maze using union by size:', end-start)
plt.show()
