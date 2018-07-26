import pygame
import socket
import json
from time import sleep
from DutyCycleGenV1p1 import get_duty_cycle

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Define some colors
BLACK    = (   0,   0,   0)
WHITE    = ( 0, 255, 0)

# This is a simple class that will help us print to the screen
# It has nothing to do with the joysticks, just outputting the
# information.
class TextPrint:
    def __init__(self):
        self.reset()
        self.font = pygame.font.Font(None, 20)

    def print(self, screen, textString):
        textBitmap = self.font.render(textString, True, BLACK)
        screen.blit(textBitmap, [self.x, self.y])
        self.y += self.line_height
        
    def reset(self):
        self.x = 10
        self.y = 10
        self.line_height = 15
        
    def indent(self):
        self.x += 175
        
    def unindent(self):
        self.x -= 175
    

pygame.init()
 
# Set the width and height of the screen [width,height]
size = [500, 600]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("DExTER's Control Setting")

#Loop until the user clicks the close button.
done = True

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Initialize the joysticks
pygame.joystick.init()
    
# Get ready to print
textPrint = TextPrint()

joystick = pygame.joystick.Joystick(0)
joystick.init()

x = joystick.get_axis(0)
y = -(joystick.get_axis(1))

change = False
orientation = 0
MaxS = 75
TurnS = 30
TurnT = 'A'
ori = 'Front'
rg = 0
chs = False

#msg = {'Change':change, 'Orientation':orientation, 'MaxS':MaxS,'TurnS':TurnS,'TurnT':TurnT, 'Coord':[x,y]}

while done:

    screen.fill(WHITE)
    textPrint.reset()
    textPrint.indent()

    for count in range(4):
        textPrint.print(screen, "" )


    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            done = False


    b1 = joystick.get_button(0)
    b2 = joystick.get_button(1)
    b3 = joystick.get_button(2)
    b4 = joystick.get_button(3)
    l3 = joystick.get_button(10)
    r1 = joystick.get_button(5)
    r2 = joystick.get_button(7)
    l1 = joystick.get_button(4)
    l2 = joystick.get_button(6)

    if l3:
        TurnT = 'D'
        textPrint.print(screen, "Turn Type: Differential" )

    
    else:
        TurnT = 'A'
        textPrint.print(screen, "Turn Type: Arc")

    for count in range(4):
        textPrint.print(screen, "" )

    if r1:

        if b4:
            flipper = [1,0]
            flt = "Flipping"

        elif b2:
            #print("Inside")
            grabber = [1,0]
            grt = "Right IN"
        
        else:
            elevator = [1,0]
            elv = "Ascending"

        change = True        

    elif l1:

        if b4:
            flipper = [0,1]
            flt = "Settling"

        elif b2:
            grabber = [0,1]
            grt = "Left IN"
        
        else:
            elevator = [0,1]
            elv = "Descending"

        change = True        

    else:
        flipper = [0,0]
        elevator = [0,0]
        grabber = [0,0]
        grt = "Idle"
        elv = "Idle"
        flt = "Idle"

    if r2:

        if b2:
            grabber = [-1,0]
            grt = "Right OUT"

        else:
            grabber = [1,1]
            grt = "IN"
            
        change = True
        
    elif l2:

        if b2:
            grabber = [0,-1]
            grt = 'Left OUT'

        else:
            grabber = [-1,-1]
            grt = "OUT"
        change = True
    '''
    else:
        grabber = [0,0]
        grt = "Idle"
    '''
    textPrint.print(screen, "Grabber: {}".format(grt) )

    for count in range(4):
        textPrint.print(screen, "" )

    textPrint.print(screen, "Flipper: {}".format(flt) )

    for count in range(4):
        textPrint.print(screen, "" )

    textPrint.print(screen, "Elevator: {}".format(elv) )

    
    if b1:

        MaxS += 20

        change = True

    if b3:

        MaxS -= 20

        change = True

    if MaxS>100:
        MaxS=100
    elif MaxS<0:
        MaxS=0

    for count in range(4):
        textPrint.print(screen, "" )

    textPrint.print(screen, "Max Speed: {}%".format(MaxS) )

    for count in range(4):
        textPrint.print(screen, "" )

    #textPrint.indent()

    textPrint.print(screen, "Turn Speed: {}%".format(TurnS) )

    for count in range(4):
        textPrint.print(screen, "" )

    x = (joystick.get_axis(0))
    y = -((joystick.get_axis(1)))

    x1 = (joystick.get_axis(2))
    y1 = ((joystick.get_axis(3)))

    if x1<0:
        x1-=0.1
    else:
        x1+=0.1

    if y1<0:
        y1-=0.1
    else:
        y1+=0.1

    x1 = int(x1)
    y1 = -int(y1)



    if x1 or y1:
        
        if x1==0 and y1==1:
            orientation = 0
            ori = 'Front'

        elif x1==0 and y1==-1:
            orientation = 2
            ori = 'Back'

        elif x1==1 and y1==0:
            orientation = 3
            ori = 'Right'

        elif x1==-1 and y1==0:
            orientation = 1
            ori = 'Left'

        change = True

    #textPrint.indent()
    textPrint.print(screen, "Orientation: {}".format(ori) )

    for count in range(4):
        textPrint.print(screen, "" )


    msg = {'Change':change,'Orientation':orientation, 'MaxS':MaxS,'TurnS':TurnS,'TurnT':TurnT,'Coord':[x,y],'flipper':flipper,'grabber':grabber,'elevator':elevator}

    msg_o = get_duty_cycle(msg)

    msg_es = json.dumps(msg_o)
    msg_eb = str.encode(msg_es)

    sock.sendto(msg_eb, ("192.168.7.2", 1234))

    if change:
        change = False
        chs = False
        sleep(0.2)
    
    pygame.display.flip()
    clock.tick(20)

pygame.quit()
