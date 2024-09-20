# Importing the pygame module
import pygame
from pygame.locals import *

import numpy
import math
 
# Initiate pygame and give permission
# to use pygame's functionality
pygame.init()
 
# Create a display surface object
# of specific dimension
windowX =1100
windowY = 900
window = pygame.display.set_mode((windowX, windowY))
pygame.display.set_caption('Shuffleboard')

white = (255, 255, 255)
red = (255, 40, 40)
blue = (0, 0, 128)

color0 = (255,153,153)
color1 = (102,255,102)
color2 = (51, 255, 51)
color3 = (0, 204, 0)
color4 = (204, 0, 204)

font = pygame.font.Font('freesansbold.ttf', 20)
font2 = pygame.font.Font('Basketball.otf', 150)
text = font.render('Press "q" to quit' , True,white) 

text2 = font.render('Press "r" to restart', True, white)
text3 = font.render('Use arrows to change inital values', True, white)
text4 = font.render('Press SPACE to shoot', True, white)

text_out = font2.render('OUT OF BOUNDS', True, red)



 
 
# Create a list of different objects
# that you want to use in the animation
image_puck = pygame.image.load("puck.png")

image_board = pygame.image.load("board2.png")

image_arrow = pygame.image.load("arrow.png")

image_background = pygame.image.load("background5.png")

square = pygame.image.load("square.png")
 
 
# Creating a new clock object to
# track the amount of time
clock = pygame.time.Clock()
 
# Creating a new variable
# We will use this variable to
# iterate over the sprite list
value = 0
 
# Creating a boolean variable that
# we will use to run the while loop
run = True
play=True
 
# Creating a boolean variable to
# check if the character is moving
# or not
moving = False

# variable to check if shoot
shoot = False
shoot1 = 1
gameInMotion = False
outOfBounds = False


# Starting coordinates of the puck
x0 = (windowX/2)
y0 = 870

 #Limits input 'num' between minimum and maximum values.
#Default minimum value is 1 and maximum value is 255.
def limitx(num, minimum=(windowX/2)-60, maximum=(windowX/2)+60):
  return max(min(num, maximum), minimum)

def limitv(num, minimum=0, maximum=3):
  return max(min(num, maximum), minimum)

#Rotates image with given angle and sets postion
def rot_center(image, angle, x, y):
    
    rotated_image = pygame.transform.rotate(image, -angle*(180/math.pi))
    new_rect = rotated_image.get_rect(center = image.get_rect(center = (x, y)).center)

    return rotated_image, new_rect

#stop function
def calcStop(x,vx,y,vy,n):

    g = 9.8
    m = 0.25
    fk = 0.07

    for i in range(n-1):
        i = i-1
        v = math.sqrt((vx[i]*vx[i])+(vy[i]*vy[i]))

        ff = m*g*fk

        if v <= ff:
            vx[i:n+1] = 0
            vy[i:n+1] = 0

            x[i:n+1] = x[i]
            y[i:n+1] = y[i]
    
    return x,vx,y,vy


#Skiljer sig från Matlab, x-value från matlab = y-value i python
def odeX():
    m = 0.25
    g = -9.8
    fk = 0.07
    diffx = m*g*fk
    return diffx

#Skiljer sig från Matlab, x-value från matlab = y-value i python
def xEuler(tspan,v0,n,theta):
    a = tspan[0]
    b = tspan[1]
    t = numpy.linspace(a,b,n+1)
    h = t[2]-t[1]

    XPos = numpy.zeros(n)
    v = numpy.zeros(n)

    v[0] = v0*numpy.cos(theta)
    XPos[0]=y0


    for i in range(n-1):
        if v[i] + h*odeX() <= 0:
            v[i+1] = 0
            XPos[i+1] = XPos[i]
        else:
             v[i+1] = v[i] + h*odeX()
             XPos[i+1] = XPos[i] - 100*h*v[i+1]
    return XPos, v

#Skiljer sig från Matlab, y-value från matlab = x-value i python
def odeY(pos,a):
    g = 9.8
    m = 0.25
    fk = 0.07
    c = 1/5
    mid = 0

    if pos >= 0 and a >= 0:
       dy = m*(a - c*numpy.exp(pos)*g*fk)
    elif pos >= 0:
       dy = m*(-a - c*numpy.exp(pos)*g*fk)
    elif a >= 0:
       dy = m*(a + c*numpy.exp(abs(pos))*g*fk)
    else :
       dy = m*(-a + c*numpy.exp(abs(pos))*g*fk)

    return dy


#Skiljer sig från Matlab, y-value från matlab = x-value i python
def yEuler(tspan,y0,v0,n,theta):
    
    a = tspan[0]
    b = tspan[1]
    t = numpy.linspace(a,b,n+1)
    h = t[2]-t[1]
    mid = 0

    max =552
    min=372
    
    scaledPos = (y0-(windowX/2))/120
    y = numpy.zeros(n+1)
    v = numpy.zeros(n+1)
    
    y[0] = scaledPos   

    v[0] = v0*numpy.sin(theta)

    for i in range(n):
        pos = y[i]

        if i == 0:
            v[i+1] = v[i] + h*odeY(pos,0)
        else:
            v[i+1] = v[i] + h*odeY(pos,v[i]-v[i-1])
        
        y[i+1] = (y[i]+ h*v[i+1])

    for i in range(n+1):
        i = i-1
        y[i] = (y[i]*120)+(windowX/2)
    return y, v

#set inital values
tspan=[0,10]
i=0
n =250
v0 = 1.60
y = y0
x = x0
theta = 0 




# Creating an infinite loop
# to run our  
while play:
    while run:
        # Setting the framerate to 100fps just
        # to see the result properly
        clock.tick(100)
    
        # iterate over the list of Event objects
        # that was returned by pygame.event.get() method.
        for event in pygame.event.get():
    
            # Closing the window and program if the
            # type of the event is QUIT
            if event.type == pygame.QUIT:
                play = False
                pygame.quit()
                quit()
    
            # Checking event key if the type
            # of the event is KEYUP i.e.
            # keyboard button is released
            if event.type == pygame.KEYUP:
    
                # Setting the value of moving to False
                # and the value f value variable to 0
                # if the button released is
                # Left arrow key or right arrow key
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT :
                    moving = False
                    value = 0

                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

                if event.key == pygame.K_r:
                    y = y0
                    x0= (windowX/2)
                    i = 0
                    theta = 0
                    print("restart")
                    gameInMotion = False
                    shoot1=1
                    shoot =False
                    
                if event.key == pygame.K_SPACE:
                    shoot1 +=1
                    if shoot1%2 == 0:
                        shoot = True
                        gameInMotion = True
                        outOfBounds =False
                        print("shoot")
                    elif i ==n or outOfBounds == True:
                        y = y0
                        x= windowX/2
                        i = 0
                        print("restart")
                        gameInMotion = False
                        shoot1=1
                        shoot =False
                        outOfBounds = False
                    else:
                        shoot = False
                        print("not-shoot")

                if gameInMotion != True:

                    if event.key == pygame.K_UP:
                        v0 += 0.01
                        

                    if event.key == pygame.K_DOWN:
                        v0 -= 0.011
                        

            


        # Storing the key pressed in a
        # new variable using key.get_pressed()
        # method
        key_pressed_is = pygame.key.get_pressed()
    
        # Changing the x coordinate
        # of the player and setting moving
        # variable to True
        #changeing theta variable

        if key_pressed_is[K_LEFT] and gameInMotion == False and pygame.key.get_mods() & pygame.KMOD_SHIFT == False:
            x0 -= 1
            moving = True

        if key_pressed_is[K_RIGHT] and gameInMotion == False and pygame.key.get_mods() & pygame.KMOD_SHIFT == False:
            x0 += 1
            moving = True

        if key_pressed_is[K_LEFT] and pygame.key.get_mods() & pygame.KMOD_SHIFT and gameInMotion == False:
            theta -= math.pi/300
            moving = True

        if key_pressed_is[K_RIGHT] and pygame.key.get_mods() & pygame.KMOD_SHIFT and gameInMotion == False:
            theta += math.pi/300
            moving = True

        # Stops if list of positions has ended
        if i >= n:
            shoot = False

        if gameInMotion == False:
            x=x0
        
        #Stores lists of posistions and velocity over time
        [yFirst, vyFirst] = xEuler(tspan,v0,n,theta)
        [xFirst, vxFirst] = yEuler(tspan,x0,v0,n,theta)

        [xPos,vx,yPos,vy] = calcStop(xFirst,vxFirst,yFirst,vyFirst,n)
        
        #sets the pucks postions to next value in list every loop
        if shoot == True:
            y= yPos[i]
            x =  xPos[i]

            i +=1
        
            moving = True

        
       
        # If moving variable is True
        # then increasing the value of
        # value variable by 1
        if moving:
            value += 1
    
    
        # limiting startvalues
        v0 = math.ceil(v0*100)/100
        v0 = limitv(v0) 
        x0 = limitx(x0)

        #displays theta in degrees
        theta_disp = math.ceil((theta*(180/(numpy.pi)))*100)/100

        #displays theta in form of arrow to show the direction of the puck
        image_arrow = pygame.transform.scale(image_arrow, (200, 300))
        [Arrow_image_rot,Arrow_rect_rot] = rot_center(image_arrow, theta, x0, y0)

        #inital values displayed in text
        textv0 = font.render('Initial Velocity: '+ str(v0), True,white)
        textx0 = font.render('Start position: '+ str(x0-windowX/2), True,white)
        textTheta = font.render('Angle: '+ str(theta_disp) + "°", True,white)


    
        # Scaling the image
        image_puck = pygame.transform.scale(image_puck, (20, 20))
        image_puckRect=image_puck.get_rect()
        image_puckRect.center = ((x, y))

        image_board = pygame.transform.scale(image_board, (120, 850))
        image_boardRect=image_board.get_rect()
        image_boardRect.center = (windowX/2, windowY/2)

        image_background = pygame.transform.scale(image_background, (windowX, windowY))
    
        # Displaying the image in our game window
        window.blit(image_background,(0,0))
        window.blit(image_board,image_boardRect)
        window.blit(Arrow_image_rot,Arrow_rect_rot)

        window.blit(image_puck, image_puckRect)


        pointText = str("")
        pointColor = red
        #limit bounds of board
        if (x > ((windowX/2)+60) or x < ((windowX/2)-60) or y < (900-850)/2 ) and gameInMotion == True:
            pointText = str("OUT OF BOUNDS")
            pointColor = red
            shoot = False
            outOfBounds = True

        #Point system
        
        if (y > 186) and i ==n:
            pointText = str("0 POINTS")
            pointColor = color0

        elif (y > 88) and i ==n:
            pointText = str("1 POINT")
            pointColor = color1

        elif (y > 65) and i ==n:
            pointText = str("2 POINTS")
            pointColor = color2

        elif (y > 45) and i ==n:
            pointText = str("3 POINTS")
            pointColor = color3
        
        elif ((y > 25 and y > (900-850)/2 ) ) and i ==n:
            pointText = str("4 POINTS")
            pointColor = color4
        
        #Render visuals    

        text_out = font2.render(pointText, True, pointColor)
        textRect_out = text_out.get_rect()
        textRect_out.center = ((windowX/2), (windowY/2))
        window.blit(text_out, textRect_out)

        window.blit(text, (10,30))
        window.blit(text2, (10, 60))
        window.blit(text3, (10, 90))
        window.blit(text4, (10, 120))
        window.blit(square, (650, 720))
        window.blit(textx0, (670, 750))
        window.blit(textv0, (670, 780))
        window.blit(textTheta, (670, 810))


    
        # Updating the display surface
        pygame.display.update()
    
        # Filling the window with black color
        window.fill((30, 60, 20))