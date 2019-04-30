#CS2302
#Nicole Favela
#last modified: April 29, 2019
#Lab7
#purpose: to build a maze and solve it using breadth first search and depth first search algorithms and show the paths created
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
import math
import queue
import time


def DisjointSetForest(size):
    return np.zeros(size,dtype=np.int)-1

def find(S,i):
    # Returns root of tree that i belongs to
    if S[i]<0:
        return i
    return find(S,S[i])
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

#builds maze with union by size
def buildMaze_with_union_by_size(cells,G):
    count = 0
    while cells!=count and numSets(S)>1:
        #d is a random integer in range of walls
        d = random.randint(0, len(walls) - 1)

        #wall is an list location in walls at d
        wall = walls[d]
        #grabs coordinates for cells
        c1 = wall[0]
        c2 = wall[1]
        #if not in same set
        if find_c(S,c1)!= find_c(S,c2):
            #puts adjaceny list in order
            if c1<c2 and c2 not in G[c1]:
                G[c1].append(c2)
                G[c2].append(c1)
            union_by_size(S,c1,c2) #make part of same set

            walls.pop(d) #remove wall
            count+=1
            d+=1
    #returns the walls remaining
    #used to draw later
    global walls2
    walls2=walls
    return G

#builds maze with standard union
def buildMaze(cells,G):
    count = 0

    while cells!=count and numSets(S)>1:
        #d is a random integer in range of walls
        d = random.randint(0, len(walls) - 1)
        #wall is an list location in walls at d
        wall = walls[d]
        #grabs coordinates for cells
        c1 = wall[0]
        c2 = wall[1]
        #if not in same set
        if find(S,c1)!= find(S,c2):
            # puts adjaceny list in order
            if c1 < c2 and c2 not in G[c1]:
                G[c1].append(c2)
                G[c2].append(c1)
            union(S, c1, c2)  # make part of same set
            walls.pop(d) #remove wall
            count += 1
            d += 1
    global walls2
    walls2 = walls
    return G

#breadth first search
def BFS(AL,v,target):
    #stores visitied vertices
    visited=[]
    #queue
    queue=[[v]]
    #vertex v is start
    #target is last cell in top right corner
    if v == target:
        return queue
    while queue:
        path=queue.pop(0)
        last=path[-1]
        #if last element in path has not been visited, add to list
        if last not in visited:
            adj=AL[last]
            #goes through adj and creates visit that is len of path
            for i in adj:
                visit=list(path)
                #appends to visit
                visit.append(i)
                queue.append(visit)
                #if target element reached, just append
                if i ==target:
                    return visit
            #adds to visited items
            visited.append(last)

#recursive version of DFS
def DFS_recursive(AL, vertex,destination,path=[]):
    # used to keep track of whether or not the vertex is found
    flag = True
    # adds vertex to path
    path += [vertex]
    # goes through length of adjacency list
    for i in AL[vertex]:
        #if destination found at vertex return path
        if vertex == destination:
            flag = False
            return path
        #recursively calls if i not in path and flag is true
        if not i in path and flag:
            path = DFS_recursive(AL, i, destination, path)
            # checks if the last item in the path is the destination
            if path[-1] == destination:
                return path
            else:
                #if doesn't lead to path
                path.pop(-1)
    return path

#iterative version of depth first search
#uses stack
def DFS_iterative(AL, start,destination):
    visited = []
    stack = [[start]]
    if start == destination:
        return stack
    #while stack not empty
    while stack:
        path = stack.pop(0)
        #last is the last item in path
        last = path[-1]
        #same as BFS only with stack
        if last not in visited:
            adj = AL[last]
            for i in adj:
                visit = list(path)
                visit.append(i)
                stack.append(visit)
                if i == destination:
                    return visit
            visited.append(last)

#changes list to edge list for maze
def Path_to_EL(path):
    #list of edges
    EL = []
    #goes through path created by algorithms
    for i in range (1,len(path)):
        #appends path[0],path[1]...
        EL.append([path[i-1], path[i]])
    return EL

#draws maze path
def draw_path(EL,walls2,maze_rows,maze_cols):
    fig, ax = plt.subplots()
    #draws path
    for w in EL:
        if w[1] - w[0] == 1:  #horizontal
            x0 = (w[0] % maze_cols) + .5
            y0 = (w[0] // maze_cols) + .5
            x1 = (w[1] % maze_cols) + .5
            y1 = (w[1] // maze_cols) + .5
        else:  #vertical
            x0 = (w[0] % maze_cols) + .5
            y0 = (w[0] // maze_cols) + .5
            x1 = (w[1] % maze_cols) + .5
            y1 = (w[1] // maze_cols) + .5
            #plots in red with linewidth 3
        ax.plot([x0, x1], [y0, y1], linewidth=3, color='r')
    sx = maze_cols
    sy = maze_rows

    #draws the maze
    for w in walls2:
        if w[1] - w[0] == 1:  #vertical wall
            x0 = (w[1] % maze_cols)
            x1 = x0
            y0 = (w[1] // maze_cols)
            y1 = y0 + 1
        else:  # horizontal wall
            x0 = (w[0] % maze_cols)
            x1 = x0 + 1
            y0 = (w[1] // maze_cols)
            y1 = y0
        ax.plot([x0, x1], [y0, y1], linewidth=1, color='k')

    ax.plot([0, 0, sx, sx, 0], [0, sy, sy, 0, 0], linewidth=2, color='k')

    ax.axis('off')
    ax.set_aspect(1.0)

plt.close("all")

maze_rows = 10
maze_cols = 15

#creates dsf of 150
S = DisjointSetForest(maze_rows*maze_cols)
#creates array of walls
walls = wall_list(maze_rows,maze_cols)
#draws empty maze
draw_maze(walls,maze_rows,maze_cols,cell_nums=True)

n = len(S)
#last index in top right
destination = n-1
print('destination is ', destination)
print('the number of cells are: ', n)

print('enter the number of walls you want to remove')
m = int(input())

print('please enter 1 to build with union by size or 2 the build with regular union')
choice = int(input())

if m < n-1:
    print('path from source to destination is not guaranteed')
    if choice == 1:
        print('building adjacency list:')
        G = [[] for i in range(n)]
        print(buildMaze_with_union_by_size(n, G))
        draw_maze(walls, maze_rows, maze_cols)
        #M is the adjacency list returned
        M = buildMaze_with_union_by_size(n, G)

        print('testing DFS recursive')

        print(DFS_recursive(M, 0,destination))
        EL_path_from_DFS = Path_to_EL(DFS_recursive(M, 0, destination))
        # removes last line
        EL_path_from_DFS.pop()
        draw_path(EL_path_from_DFS, walls2, maze_rows, maze_cols)

        print('testing DFS iterative')
        print(DFS_iterative(M, 0,destination))
        EL = Path_to_EL(DFS_iterative(M, 0, destination))
        draw_path(EL, walls2, maze_rows, maze_cols)

        print('testing bfs')
        print(BFS(M, 0,destination))
        EL_path_from_BFS = Path_to_EL(BFS(M, 0, destination))
        draw_path(EL_path_from_BFS, walls2, maze_rows, maze_cols)

        plt.show()

    elif choice == 2:
        print('building adjacency list:')
        G = [[] for i in range(n)]
        print(buildMaze(n, G))
        draw_maze(walls, maze_rows, maze_cols)
        M = buildMaze(n, G)

        print('testing DFS recursive')

        print(DFS_recursive(M, 0, destination))
        EL_path_from_DFS = Path_to_EL(DFS_recursive(M, 0, destination))
        #removes last line
        EL_path_from_DFS.pop()
        draw_path(EL_path_from_DFS, walls2, maze_rows, maze_cols)

        print('testing DFS iterative')
        print(DFS_iterative(M, 0, destination))
        EL = Path_to_EL(DFS_iterative(M, 0, destination))
        draw_path(EL, walls2, maze_rows, maze_cols)

        print('testing bfs')
        print(BFS(M, 0, destination))
        EL_path_from_BFS = Path_to_EL(BFS(M, 0, destination))
        draw_path(EL_path_from_BFS, walls2, maze_rows, maze_cols)
        plt.show()

if m == n-1:
    print('there is a unique path from source to destination')
    if choice == 1:
        print('building adjacency list:')
        G = [[] for i in range(n)]
        print(buildMaze_with_union_by_size(n,G))
        draw_maze(walls, maze_rows, maze_cols)
        M = buildMaze_with_union_by_size(n,G)

        print('testing DFS recursive')
        print(DFS_recursive(M,0,destination))
        EL_path_from_DFS = Path_to_EL(DFS_recursive(M,0,destination))
        EL_path_from_DFS.pop()
        draw_path(EL_path_from_DFS, walls2, maze_rows, maze_cols)

        print('testing DFS iterative')
        print(DFS_iterative(M, 0,destination))
        EL = Path_to_EL(DFS_iterative(M, 0,destination))
        draw_path(EL, walls2, maze_rows, maze_cols)

        print('testing bfs')
        print(BFS(M, 0,destination))
        EL_path_from_BFS = Path_to_EL(BFS(M, 0,destination))
        draw_path(EL_path_from_BFS , walls2, maze_rows, maze_cols)

        plt.show()
    elif choice == 2:
        print('building adjacency list:')
        G = [[] for i in range(n)]
        print(buildMaze(n, G))
        draw_maze(walls, maze_rows, maze_cols)
        M = buildMaze(n, G)

        print('testing DFS recursive')

        print(DFS_recursive(M, 0, destination))
        EL_path_from_DFS = Path_to_EL(DFS_recursive(M, 0, destination))
        EL_path_from_DFS.pop()
        draw_path(EL_path_from_DFS, walls2, maze_rows, maze_cols)

        print('testing DFS iterative')
        print(DFS_iterative(M, 0, destination))
        #draws the  path depth first search takes
        EL = Path_to_EL(DFS_iterative(M, 0, destination))
        draw_path(EL, walls2, maze_rows, maze_cols)

        print('testing bfs')
        print(BFS(M, 0, destination))
        #draws the path breadth first search takes
        EL_path_from_BFS = Path_to_EL(BFS(M, 0, destination))
        draw_path(EL_path_from_BFS, walls2, maze_rows, maze_cols)

        plt.show()
if m > n-1:
    print('there is at least one path from source to destination')
    if choice == 1:
        print('building adjacency list:')
        G = [[] for i in range(n)]
        print(buildMaze_with_union_by_size(n, G))
        draw_maze(walls, maze_rows, maze_cols)

        M = buildMaze_with_union_by_size(n, G)


        print('testing DFS recursive')
        print(DFS_recursive(M, 0,destination))
        EL_path_from_DFS = Path_to_EL(DFS_recursive(M, 0, destination))
        EL_path_from_DFS.pop()
        draw_path(EL_path_from_DFS, walls2, maze_rows, maze_cols)

        print('testing DFS iterative')
        print(DFS_iterative(M, 0,destination))
        EL = Path_to_EL(DFS_iterative(M, 0, destination))
        draw_path(EL, walls2, maze_rows, maze_cols)

        print('testing bfs')
        print(BFS(M, 0,destination))
        EL_path_from_BFS = Path_to_EL(BFS(M, 0, destination))
        draw_path(EL_path_from_BFS, walls2, maze_rows, maze_cols)

        plt.show()
    elif choice == 2:
        print('building adjacency list:')
        G = [[] for i in range(n)]
        print(buildMaze(n, G))
        draw_maze(walls, maze_rows, maze_cols)
        M = buildMaze(n, G)

        print('testing DFS recursive')

        print(DFS_recursive(M, 0, destination))
        EL_path_from_DFS = Path_to_EL(DFS_recursive(M, 0, destination))
        EL_path_from_DFS.pop()
        draw_path(EL_path_from_DFS, walls2, maze_rows, maze_cols)

        print('testing DFS iterative')
        print(DFS_iterative(M, 0, destination))
        EL = Path_to_EL(DFS_iterative(M, 0, destination))
        draw_path(EL, walls2, maze_rows, maze_cols)

        print('testing bfs')
        print(BFS(M, 0, destination))
        EL_path_from_BFS = Path_to_EL(BFS(M, 0, destination))
        draw_path(EL_path_from_BFS, walls2, maze_rows, maze_cols)

        plt.show()

plt.show()
