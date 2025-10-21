import numpy as np
import sys


# given some p, and some tensor of probabilities that pitchers and batters at some point 
# attempt a strike or swing respectively, dp that shit and get q for the state b = 0, s = 0.

def getQ(xtable, p):


    # at state b , s,
    # f_{B , S} (b , s) = 
    # / (b, s + 1) =  x^2(1 - p) + 2x(1-x)
    # | b(b + 1, s) = (1 - x)^2
    # \ b(HR) = px^2


    qtable = np.zeros((5 , 4))
    # initiate probability at b = 4 and s = 3 to 0.
    
    
    for b in range(4 , -1, -1):
        for s in range(3 , -1, -1): 
            
            if b == 4 or s == 3:
                qtable[b][s] = 0.0

            elif b == 3 and s == 2:
                qtable[b][s] = 1.0

            else:

                pnextStrike = qtable[b][s + 1]
                pnextBall = qtable[b + 1][s]


                x = xtable[b][s]

                a = (x**2)*(1 - p) + 2*x*(1-x)
                b = (1 - x)**2

                qtable[b][s] = a * pnextStrike + b*pnextBall

    return qtable[0][0]

                




def dp(p : np.float64):

    evtable = np.zeros((5 , 4))
    xtable = np.zeros((5, 4))

    for b in range(4 , -1, -1):
        for s in range(3 , -1, -1): 


            if b == 4 and s == 3:
                continue
            elif b == 4:
                evtable[b][s] = 1
            elif s == 3:
                evtable[b][s] = 0
            else:

                nextBall = evtable[b + 1][s]
                nextStrike = evtable[b][s + 1]

                y = 1 - nextStrike / (2 * nextStrike - nextBall + 4*p)
                x = y

                evtable[b][s] = ((1 - x)**2) * nextBall + 2 * x * (1 - x) * nextStrike + (x**2)*(4*p + (1 - p)*nextStrike) 
                xtable[b][s] = x

    q = getQ(xtable)

    return q


def main():

    iterations = sys.argv[1]

    l , h = 0.0 , 1.0

    qvals = np.zeros(10)
    for i in range(iterations): 

        # build new range for prange
        prange = np.arange(l, h, (l - h) / 10.0)

        for i , pval in enumerate(prange):
            qvals[i] = dp(pval)

        
        imax = np.argmax(qvals)
        # zoom in
        l = qvals[imax] - ((l - h) / 10.0)
        h = qvals[imax] + ((l - h) / 10.0)

