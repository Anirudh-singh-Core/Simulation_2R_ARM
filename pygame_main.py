#single window hexagon plot operation.txt
from kin import *
from Obstacle_DetAvoid import *
import pygame

FPS = 60
fpsClock = pygame.time.Clock()

def direct_motion(window):
    
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
                             [x_pos[i+1]+450,y_pos[i+1]+400,
                             5)
    Px = x_pos[N]+450   
    Py = y_pos[N]+400
    pygame.display.update()
    fpsClock.tick(FPS) 

