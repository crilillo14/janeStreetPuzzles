import numpy as np
import sys


# given some p, and some tensor of probabilities that pitchers and batters at some point 
# attempt a strike or swing respectively, dp that shit and get q for the state b = 0, s = 0.

def getQ(xtable, p):
    # at state b , s,
    # f_{B , S} (b , s) = 
    #   P(b, s + 1) =  x^2(1 - p) + 2x(1-x)
    #   P(b + 1, s) = (1 - x)^2
    #   P(HR) = px^2


    qtable = np.zeros((5 , 4))
    # initiate probability at b = 4 and s = 3 to 0.
    
    
    for balls in range(4 , -1, -1):
        for strikes in range(3 , -1, -1): 
            
            if balls == 4 or strikes == 3:
                qtable[balls][strikes] = 0.0

            elif balls == 3 and strikes == 2:
                qtable[balls][strikes] = 1.0

            else:

                pnextStrike = qtable[balls][strikes + 1]
                pnextBall = qtable[balls + 1][strikes]


                x = xtable[balls][strikes]

                a = (x**2)*(1 - p) + 2*x*(1-x)
                b = (1 - x)**2

                qtable[balls][strikes] = a * pnextStrike + b*pnextBall

    return qtable[0][0] 

def dp(p):

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

    q = getQ(xtable, p)

    return q


def main():

    log = {}

    """
    try: 
        iterations = int(sys.argv[1])
    except Exception as e:
        iterations = 1
        raise e


    """
    iterations = 1
    l , h = 0.0 , 1.0

    qvals = np.zeros(10)

    for i in range(iterations): 
        print("entered iteration loop")
        # build new range for prange

        prange = np.arange(l, h, (h - l) / 10.0)
        print(prange)

        for i , pval in enumerate(prange):
            print("entered pval loop")
            qvals[i] = dp(pval)

            print(f"got q = {qvals[i]}")
            log[pval] = qvals[i]

        
        

        imax = np.argmax(qvals)
        # zoom in
        l = qvals[imax] - ((l - h) / 10.0)
        h = qvals[imax] + ((l - h) / 10.0)


    print("Finalized. Log of run is as follows: ")
    print(log)


if __name__ == "__main__":
    main()
