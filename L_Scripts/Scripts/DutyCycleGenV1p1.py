

#n = 0 #orientation
MaxS = 0.5
TurnS = 0.5
c = [0,0]

def orient(c,n):

    #print('inside orient')
    

    #global c,n

    for i in range(n):
        #z = c[0]
        #c[0] = c[1]
        #c[1] = -z
        c[0],c[1] = c[1],-c[0]
        #print('Changed to:',n)

    return c


def get_duty_cycle(msg):

    global n,MaxS,TurnS,c

    c = msg['Coord']

    change = msg['Change']

    
    #print(x,y)


    n = msg['Orientation']
    #print(n)
    MaxS = msg['MaxS']/100
    TurnS = msg['TurnS']/100

    c = orient(c,n)

    x,y = c[0],c[1]

    '''
    if x<0:
        x-=0.1
    else:
        x+=0.1

    if y<0:
        y-=0.1
    else:
        y+=0.1
    '''
    
    x = int(x*100)
    y = int(y*100)
    flipper = msg['flipper']
    grabber = msg['grabber']


    if msg['TurnT'] == 'A':

        if y>0:

            if x == 0:

                return {'p1':(MaxS*y),'p2':0,'p3':(MaxS*y),'p4':0,'flipper':flipper,'grabber':grabber,'ch':change,'elevator':msg['elevator']} #Forward Straight

            elif x>0:

                return {'p1':(MaxS*y*TurnS*(x/100)),'p2':0,'p3':(MaxS*y),'p4':0,'flipper':flipper,'grabber':grabber,'ch':change,'elevator':msg['elevator']} #Forward Right (Arc)

            else:

                return {'p3':(MaxS*y*TurnS*(-x/100)),'p2':0,'p1':(MaxS*y),'p4':0,'flipper':flipper,'grabber':grabber,'ch':change,'elevator':msg['elevator']} #Forward Left (Arc)

        elif y<0:

            if x == 0:

                return {'p1':0,'p2':-MaxS*(y),'p3':0,'p4':-MaxS*(y),'flipper':flipper,'grabber':grabber,'ch':change,'elevator':msg['elevator']} #Reverse Straight

            elif x>0:

                return {'p1':0,'p2':-MaxS*(y)*TurnS*(x/100),'p3':0,'p4':-MaxS*(y),'flipper':flipper,'grabber':grabber,'ch':change,'elevator':msg['elevator']} #Reverse Right (Arc)

            else:

                return {'p3':0,'p2':-MaxS*(y),'p1':0,'p4':MaxS*(y)*TurnS*(x/100),'flipper':flipper,'grabber':grabber,'ch':change,'elevator':msg['elevator']} #Reverse Left (Arc)

        else:

            return {'p1':0,'p2':0,'p3':0,'p4':0,'flipper':flipper,'grabber':grabber,'ch':change,'elevator':msg['elevator']} #Stop


    else:

        if x>0:

            return {'p1':0,'p2':MaxS*x,'p3':(MaxS*x),'p4':0,'flipper':flipper,'grabber':grabber,'ch':change,'elevator':msg['elevator']} #Differential Right

        elif x<0:

            return {'p1':(MaxS*(-x)),'p4':-MaxS*(x),'p3':0,'p2':0,'flipper':flipper,'grabber':grabber,'ch':change,'elevator':msg['elevator']} #Differential Left

        else:

            return {'p1':0,'p2':0,'p3':0,'p4':0,'flipper':flipper,'grabber':grabber,'ch':change,'elevator':msg['elevator']} #Stop


def main():

    change = True
    orientation = 0
    MaxS = 50
    TurnS = 50
    TurnT = 'A'

    msg = {'Change':change, 'Orientation':orientation, 'MaxS':MaxS,'TurnS':TurnS,'TurnT':TurnT, 'Coord':[0,0.99]}

    print(get_duty_cycle(msg))

if __name__ == '__main__':

    main()






























    
