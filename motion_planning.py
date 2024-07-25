#Main loop and function calls operation.py
from kin import *
from Obstacle_DetAvoid import *

import pygame

# Animation

pygame.init()

FPS = 60
fpsClock = pygame.time.Clock()
window = pygame.display.set_mode((900,800))
window.fill((255,255,255))
pygame.draw.circle(window,(0,0,255),[450,400],6.3,0)
for n in range(1,15):
    for h in range(6*n):
        cntr = goal(n,h)
        if cntr == 0:
            continue
        cntr = [cntr[0]+450,cntr[1]+400]
        pygame.draw.circle(window,(0,0,255),cntr,6.3,0)

x_pos,y_pos,di_1_list = get_hmgns()

for i in range(N):
    pygame.draw.line(window,(0,0,0),
                     [x_pos[i]+450,y_pos[i]+400],
                     [x_pos[i+1]+450,y_pos[i+1]+400],
                     5)
    
Px = int(x_pos[N]+450)  
Py = int(y_pos[N]+400)
P = (Px,Py)
  

pygame.display.update()

########################################################################

# Create List for Blocked points
Blocked=[]

# List for the goal point
Goal=[]
# list for the Initial point
Initial=[]

while True:
    switch1 = 0
    switch2 = 0
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                print("Goal Selected")
                global Gx, Gy, G
                x,y = event.pos
                g = np.array([[x-450,y-400]])
                g = is_g_tube(g,15)
                Gx, Gy = x, y
                G = (Gx,Gy)
                lclick = True
                pygame.draw.circle(window,(255,0,0),[g[0][0]+450,g[0][1]+400],15,4)
                pygame.display.update()
                
            if event.button == 3 and lclick == True:
                print("Obstacle Selected")
                r = 16.1
                a,b = event.pos
                Cx, Cy = a, b
                C = (Cx,Cy)
                lclick = False
                points = path_planning(Px,Py,Cx,Cy,Gx,Gy)    
                draw_circles(window,Px,Py,Cx,Cy,Gx,Gy)
                points_on_line(Px, Py, Cx, Cy)

                if path_block(G,P,C,r):
                    switch = 1
                    continue
                else:
                    print("Not in Path")
                    switch = 1
                
                

                
                    

            

                
        
    if switch1 == 0:
        continue

    waiting = True

    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    switch2 = 1
                    waiting = False
                elif event.key == pygame.K_x:
                    waiting = False

    if switch2 == 0:
        continue

    g = np.append(g,[[0]],axis=1)
    check = 0
    while True :
        check += 1

        window.fill((255,255,255))
        pygame.draw.circle(window,(0,0,255),[450,400],6.3,0)
        for n in range(1,15):
            for h in range(6*n):
                cntr = goal(n,h)
                if cntr == 0:
                    continue
                cntr = [cntr[0]+450,cntr[1]+400]
                pygame.draw.circle(window,(0,0,255),cntr,6.3,0)

        x_pos,y_pos,di_1_list = get_hmgns()
        for i in range(N):
            pygame.draw.line(window,(0,0,0),
                             [x_pos[i]+450,y_pos[i]+400],
                             [x_pos[i+1]+450,y_pos[i+1]+400],
                             5)
        Px = int(x_pos[N]+450)   
        Py = int(y_pos[N]+400)
        pygame.display.update()
        fpsClock.tick(FPS)
        if check == 1000:
            print('Failed to converge...')
            break
        e = di_1_list[N]
        err = g - e
        E = np.linalg.norm(err)
        if tol<E:
            t = E/spd
            eff_vel = err/t
            delta_t = beta*t
            jnt_vel = get_jnt_vel(eff_vel)
            for i in range(len(theta_var)):
                theta[theta_var[i]] = theta[theta_var[i]] + delta_t*jnt_vel[0,i]
            for i in range(len(d_var)):
                d[d_var[i]] = d[d_var[i]] + delta_t*jnt_vel[0,len(theta_var)+i]
        else:
            break




