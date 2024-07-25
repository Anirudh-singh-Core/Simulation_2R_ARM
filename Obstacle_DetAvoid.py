#path finding operation.py
import pygame
import math
from math import sin,cos,acos,pi,sqrt,radians
'''
Cx, Cy = 433, 257 # Circle parameters
Px, Py = 450, 287 # Starting point
Gx, Gy = 416, 230 # Goal point

'''	
r = 16.1  # Circle radius

# Function to calculate arc length
def arc_length(angle1, angle2, radius):
    angle_diff = abs(angle1 - angle2)
    if angle_diff > math.pi:
        angle_diff = 2 * math.pi - angle_diff
    return angle_diff * radius

# Calculate length between tangents
def t_length(x,y):
    global l
    l=math.sqrt((x[0] - y[0])**2 + (x[1] - y[1])**2)
    
    print(l)
    return l
    
# Calculate the angle of the arc
def arc_angle(r,l):
    global arc_theta
    arc_theta=acos(((2*(r**2))-l**2)/(2*(r**2)))
    #print(" The arc angle between : ",math.degrees(arc_theta))

# Calculate the arc length via formula
def arc_formula_length(arc_theta):
    global arc_formula_length
    arc_formula_length=2*pi*r*(math.degrees(arc_theta)/360)
    print("Length of arc via formula: ",arc_formula_length)

    
# Function to calculate points along the arc
def calculate_arc_points(center, radius, start_angle, end_angle, num_points):
    arc_points = []
    angle_step = (end_angle - start_angle) / num_points
    for i in range(num_points + 1):
        angle = start_angle + i * angle_step
        x = center[0] + radius * math.cos(angle)
        y = center[1] + radius * math.sin(angle)
        arc_points.append((x, y))

    #print(arc_points)  End points to reach 2R

    '''
    for i in arc_points:
        print(i)
    return arc_points
    '''
    return arc_points

# Function calculating whether the line inside circle or not

def points_on_line(x_start, y_start, x_end, y_end):
    global x,y,points
    points = []
    dx = x_end - x_start
    dy = y_end - y_start
    steps = max(abs(dx), abs(dy))
    
    if steps == 0:
        return [(x_start, y_start)]
    
    step_x = dx / steps
    step_y = dy / steps
    
    for i in range(int(steps) + 1):
        x = x_start + i * step_x
        y = y_start + i * step_y
        points.append((x, y))
    print("--------> all the points: " ,points)
    return points


def points_inside_circle(points, cx, cy, r):
    for x, y in points:
        if (x - cx)**2 + (y - cy)**2 == r**2:
            print("-----> points in circle : ", x,y)
            return True
    
    return False


# Function to calculate the points on an arc

def path_planning(Px, Py, Cx, Cy, Gx, Gy):
    global Tangent1, Tangent2, Tangent1_1, Tangent2_1, arc_points
    pc = math.sqrt((Px - Cx)**2 + (Py - Cy)**2) # Calculate distance between point P and circle center C

    thetapc = math.acos(r / pc) # Calculate angle thetapc between PT and PC

    direction_angle1 = math.atan2(Py - Cy, Px - Cx) # Calculate direction angle of vector from C to P

    tangency_angle1 = direction_angle1 + thetapc # Calculate tangency angles
    tangency_angle2 = direction_angle1 - thetapc # Calculate tangency angles 

    Tangent1 = (Cx + r * math.cos(tangency_angle1), Cy + r * math.sin(tangency_angle1)) # Calculate tangency points for P to T
    Tangent2 = (Cx + r * math.cos(tangency_angle2), Cy + r * math.sin(tangency_angle2)) # Calculate tangency points for P to T

    gc = math.sqrt((Gx - Cx)**2 + (Gy - Cy)**2) # Calculate distance between point G and circle center C
    
    thetacg = math.acos(r / gc) # Calculate angle thetapc for point G
   
    direction_angle2 = math.atan2(Gy - Cy, Gx - Cx)  # Calculate direction angle of vector from C to G
    
    tangency_angle1_1 = direction_angle2 - thetacg # Calculate tangency angles for G
    tangency_angle2_1 = direction_angle2 + thetacg # Calculate tangency angles for G

    Tangent1_1 = (Cx + r * math.cos(tangency_angle1_1), Cy + r * math.sin(tangency_angle1_1)) # Calculate tangency points for T to G
    Tangent2_1 = (Cx + r * math.cos(tangency_angle2_1), Cy + r * math.sin(tangency_angle2_1)) # Calculate tangency points for T to G

    

    # Arc length
    l1 = t_length(Tangent1,Tangent1_1)
    l2 = t_length(Tangent2,Tangent2_1)
    if l1 < l2:
        arc_points = calculate_arc_points((Cx, Cy), r, tangency_angle1, tangency_angle1_1, 50)
    else:
        arc_points = calculate_arc_points((Cx, Cy), r, tangency_angle2, tangency_angle2_1, 50)
    return arc_points

    

    '''
    print("Tangent1:",Tangent1)
    print("Tangent2:",Tangent2)
    print("Tangent1_1:",Tangent1_1)
    print("Tangent2_1:",Tangent2_1)

    
    Arc_length_1 = arc_length(tangency_angle1, tangency_angle1_1, r) # Calculate arc lengths between Tangent1 and Tangent2 for P   
   
    Arc_length_2 = arc_length(tangency_angle2, tangency_angle2_1, r) # Calculate arc lengths between Tangent1_1 and Tangent2_1 for G

    smallest_arc = min(Arc_length_1, Arc_length_2) # Determine the smallest arc length

    if smallest_arc == Arc_length_1:
        arc_points = calculate_arc_points((Cx, Cy), r, tangency_angle1, tangency_angle1_1, 50)

    elif smallest_arc == Arc_length_2:
        arc_points = calculate_arc_points((Cx, Cy), r, tangency_angle2, tangency_angle2_1, 50)
    return arc_points
    '''

'''
path_planning(Px, Py, Cx, Cy, Gx, Gy)


# Calculate points along the smallest arc

arc_triangle(Tangent1,Tangent2_1)

arc_angle(r,l)

arc_formula_length(arc_theta)

pygame.init()

WIDTH, HEIGHT = 900, 800
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tangent Points and Lines on Circle")

'''
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
'''
# Main loop

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                x, y = event.pos
                print(f"Mouse clicked at: ({x}, {y})")

    window.fill(WHITE)
    
'''
def draw_circles(window ,Px , Py, Cx, Cy,Gx , Gy):
    # Draw the Starting point (P) and Goal point (G)
    pygame.draw.circle(window, RED, (Px, Py), 6)
    pygame.draw.circle(window, RED, (Gx, Gy), 6)

    # Draw the circle
    pygame.draw.circle(window, BLACK, (Cx, Cy), int(r), 2)

    # Draw the tangent points and lines for P
    pygame.draw.circle(window, BLACK, (int(Tangent1[0]), int(Tangent1[1])), 2)
    pygame.draw.circle(window, BLACK, (int(Tangent2[0]), int(Tangent2[1])), 2)
    pygame.draw.line(window, BLACK, (Cx, Cy), (int(Tangent1[0]), int(Tangent1[1])), 2)
    pygame.draw.line(window, BLACK, (Cx, Cy), (int(Tangent2[0]), int(Tangent2[1])), 2)
    pygame.draw.line(window, BLACK, (int(Tangent1[0]), int(Tangent1[1])), (Px, Py), 2)
    pygame.draw.line(window, BLACK, (int(Tangent2[0]), int(Tangent2[1])), (Px, Py), 2)

    # Draw the tangent points and lines for G
    pygame.draw.circle(window, BLACK, (int(Tangent1_1[0]), int(Tangent1_1[1])), 2)
    pygame.draw.circle(window, BLACK, (int(Tangent2_1[0]), int(Tangent2_1[1])), 2)
    pygame.draw.line(window, BLACK, (Cx, Cy), (int(Tangent1_1[0]), int(Tangent1_1[1])), 2)
    pygame.draw.line(window, BLACK, (Cx, Cy), (int(Tangent2_1[0]), int(Tangent2_1[1])), 2)
    pygame.draw.line(window, BLACK, (int(Tangent1_1[0]), int(Tangent1_1[1])), (Gx, Gy), 2)
    pygame.draw.line(window, BLACK, (int(Tangent2_1[0]), int(Tangent2_1[1])), (Gx, Gy), 2)

    # Draw the smallest arc in color <---------------------------------------------------
    pygame.draw.lines(window, RED, False, arc_points, 1)

    pygame.display.flip()
'''
pygame.quit()
'''

def path_block(g,p,c,r):
    A = -((g[1] - p[1])/(g[0]-p[0]))
    B = 1
    C = -A*p[0]-p[1]

    if abs((A*c[0]+B*c[1]+C)/(sqrt((A**2)+(B**2)))) < r :
        print("Passes")
        return True

