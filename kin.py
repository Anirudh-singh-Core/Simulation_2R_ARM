
kinematics operation.py


path = r"" #file location
from Obstacle_DetAvoid import *

import numpy as np
import pygame
from pygame.locals import *
import pandas as pd
import math
from math import sin,cos,acos,pi,sqrt,radians

spd = 0.01
tol = 0.01
beta = 0.05
p = 32.2
q = 16.1
df = pd.read_excel(path)
RED = (255, 0, 0)

theta = list(df.Theta)
d = list(df.z_displace)
alpha = list(df.Alpha)
a = list(df.x_displace)
N = len(d)

theta_var = []
for i in range(N):
    if math.isnan(float(theta[i])):
        theta[i] = radians(float(input(f'Enter value of theta{i+1}: ')))
        theta_var.append(i)
    else:
        theta[i] = radians(theta[i])

d_var = []
for i in range(N):
    if math.isnan(float(d[i])):
        d[i] = float(input(f"Enter value of d{i+1}: "))
        d_var.append(i)

def get_hmgns():               
    global Ri_1_list,di_1_list,x_pos,y_pos,Ti_list
    Ti_list = []
    Ti = np.array([[1,0,0,0],
                   [0,1,0,0],
                   [0,0,1,0],
                   [0,0,0,1]])
    Ti_list.append(Ti)
    for i in range(N):
        i_1Ti = np.array([[cos(theta[i]),sin(theta[i]),0,0],
                          [-sin(theta[i])*cos(alpha[i]),cos(theta[i])*cos(alpha[i]),sin(alpha[i]),0],
                          [sin(theta[i])*sin(alpha[i]),-cos(theta[i])*sin(alpha[i]),cos(alpha[i]),0],
                          [a[i]*cos(theta[i]),a[i]*sin(theta[i]),d[i],1]])
        Ti = np.dot(i_1Ti,Ti)
        Ti_list.append(Ti)
        
    Ri_1_list = []
    di_1_list = []
    x_pos = []
    y_pos = []
    for i in range(N):
        Ri_1 = np.array([np.delete(Ti_list[i][2],[3])])
        Ri_1_list.append(Ri_1)
        x_pos.append(Ti_list[i][3][0])
        y_pos.append(Ti_list[i][3][1])
        di_1 = np.array([np.delete(Ti_list[i][3],[3])])
        di_1_list.append(di_1)
    di_1 = np.array([np.delete(Ti_list[N][3],[3])])
    di_1_list.append(di_1)
    x_pos.append(Ti_list[N][3][0])
    y_pos.append(Ti_list[N][3][1])
    return x_pos,y_pos,di_1_list

def get_jcbn():
    jcbn = np.array([[0,0,0]])
    for i in theta_var:
        R = Ri_1_list[i]
        disp = di_1_list[N] - di_1_list[i]
        Rxd = np.cross(R,disp)
        jcbn = np.append(jcbn,Rxd,axis=0)
    for i in d_var:
        R = Ri_1_list[i]
        jcbn = np.append(jcbn,R,axis=0)
    jcbn = np.delete(jcbn,(0),axis=0)
    return jcbn

def get_jnt_vel(eff_vel):
    jmat = get_jcbn()
    j_mat = np.linalg.pinv(jmat)
    jnt_vel = np.dot(eff_vel,j_mat)
    return jnt_vel
    
def goal(n,h):
    k = int(h/n)
    h = h%n
    r = p*sqrt(n**2+h**2-n*h)
    theta = acos(p*(2*n-h)/(2*r)) + k*pi/3
    phi = round(math.degrees(theta))
    if n == 12 and phi%60 == 0:
        return 0
    elif n == 13 and r > 395.7:
        return 0
    elif n == 14 and (r >= 395.7 or (phi-30)%60 <= 0.01):
        return 0
    x = r*cos(theta)
    y = r*sin(theta)
    return [x,y]

def is_g_tube(g,marg):
    
    O = np.array([[0,0]])
    if np.linalg.norm(g-O)<marg:
        return O
    for n in range(1,15):
        for h in range(6*n):
            cntr = goal(n,h)
            if cntr == 0:
                continue
            cntr = np.array([cntr])
            r = np.linalg.norm(g-cntr)
            if r<marg:
                g = cntr
                return g
    print('Select vaible location...')


