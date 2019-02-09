#CS2302
#Nicole Favela
#Lab1
#instructor: Olac Fuentes
#TAs: Anindita Nath and Maliheh Zargaran

import matplotlib.pyplot as plt
import numpy as np
import math 

#draws basic circles
def circle(center,rad):
    n = int(4*rad*math.pi)
    t = np.linspace(0,6.3,n)
    x = center[0]+rad*np.sin(t)
    y = center[1]+rad*np.cos(t)
    return x,y

 #draws concentric circles
def draw_circles(ax,n,center,radius,w):
    if n>0:
        x,y = circle(center,radius)
        ax.plot(x+radius,y,color='k')
        draw_circles(ax,n-1,center,radius*w,w)
     
#draws the basic circle
def circle2(center,rad):
    n = int(2*rad*math.pi)*2
    t = np.linspace(0,6.3,n) 
    x = center[0]+rad*np.sin(t) #center + y val
    y = center[1]+rad*np.cos(t) #center + x val
    return x,y

#draws fractal circles
def draw_circles2(ax,num_circles,center,rad):
    if num_circles>0:
        x,y = circle2([center[0],center[1]],rad)
        ax.plot(x,y,color='k')
        num_circles-=1
        
    if num_circles>0:
        rad2=rad/3
        moved=rad2*2
        draw_circles2(ax,num_circles,[center[0],center[1]],rad2)
        draw_circles2(ax,num_circles,[center[0]-moved,center[1]],rad2)
        draw_circles2(ax,num_circles,[center[0]+moved,center[1]],rad2)
        draw_circles2(ax,num_circles,[center[0],center[1]-moved],rad2)
        draw_circles2(ax,num_circles,[center[0],center[1]+moved],rad2)
#part 1
def draw_squares(ax,n,p,w):
    if n>0:
        q = p*w #array elements mulitplied by scalar w
        temparray =np.copy(p)    #creates copy of array
        temp1 =np.copy(p)   #creates copy 2
        temparray[:,1]+=1000 #stores copy of column 1
        temp1[:,0]+=1000 #stores copy of column 0
        q1 = temparray*w # modifies temp and stores it
        q2 = temp1*w
        ax.plot(p[:,0],p[:,1],color='k') #plots and colors graph
        draw_squares(ax,n-1,q,w)    
        draw_squares(ax,n-1,q+500,w) #recursive call up 500
        draw_squares(ax,n-1,q1,w)
        draw_squares(ax,n-1,q2,w)
#draws basic lines
def draw_line(ax, x1,y1,x2,y2):
        n = int(max(abs(x1-x2), abs(y1-y2)))
        x = np.linspace(x1,x2,n)
        y = np.linspace(y1,y2,n)
        ax.plot(x,y,color='k')
#draws binary tree
def recursive_graph(ax, x, y, w, h, height ):
	if height  > 0:
		draw_line(ax, x+w/2,y, x+w/4,y+h)
		draw_line(ax, x+w/2,y, x+w*3/4,y+h)
		
		height -= 1
		recursive_graph(ax, x, y+h, w/2, h, height)
		recursive_graph(ax, x+w/2, y+h, w/2, h, height)

def graph(ax, x, y, w, h, height):
	    level_height = h/height
	    recursive_graph(ax, x, y, w, level_height, height)
        
        

plt.close("all") 

#part a
fig, ax0 = plt.subplots() 
draw_circles(ax0, 80, [100,0], 100,.7)
ax0.set_aspect(1.0)
plt.show()

fig.savefig('concentric_circles_b.png')
fig, ax1 = plt.subplots() 
draw_circles(ax1, 100, [100,0], 100,.9)
ax1.set_aspect(1.0)
ax1.axis('on')
plt.show()
fig.savefig('concentric_circles_c.png')

#creates array to plot coorinates
p = np.array([[250,250],[250,750],[750,750],[750,250],[250,250]])
fig, ax = plt.subplots()
draw_squares(ax,3,p,.5)
ax.set_aspect(1.0)
ax.axis('on')
plt.show() #shows plot
fig.savefig('squares.png') #saves image

#part 3
fig, ax6 = plt.subplots()
graph(plt,0,0,100,-100,6)
ax6.set_aspect(1.0)
plt.show()
fig.savefig('triangle_a.png')
fig, ax7 = plt.subplots()
ax7.set_aspect(1.0)
fig, ax6 = plt.subplots()
graph(plt,0,0,100,-100,6)
plt.show()
fig.savefig('triangle_b.png')

#part 4
fig, ax9 = plt.subplots() 
draw_circles2(ax9, 3, [0,0], 30)
ax9.set_aspect(1.0)
plt.show()
fig.savefig('circles0.png')
fig, ax10 = plt.subplots() 
draw_circles2(ax10, 4, [0,0], 30)
ax10.set_aspect(1.0)
plt.show()
fig.savefig('circles1.png')
fig, ax11 = plt.subplots() 
draw_circles2(ax11, 5, [0,0], 30)
ax11.set_aspect(1.0)
plt.show()
fig.savefig('circles2.png')