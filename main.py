

from world import *

from ai.BasicAI import BasicAI
from ai.RepeatingAI import RepeatingAI
from ai.LookaheadAI import LookaheadAI
from ai.ObjectiveAI import ObjectiveAI

from GUI import GUI
        
        
def test_ai(ai, num_trials=100, timeout=5):
    seed(1)
    scores = []
    for trial in xrange(num_trials):
        w = World()
        tries = 0
        while not w.loss():
            move = ai.get_move(w)
            success = w.apply_move(move)
            if success:
                tries = 0
            else:
                tries += 1
                
            if tries >= timeout:
                break
        scores.append(w.greatest_tile)
    return scores
    
def calc_statistics(scores):
    scores = sorted(scores)
    median = scores[len(scores)/2]
    average = float(sum(scores))/len(scores)
    variance = sqrt(float(reduce(lambda y,x: (x-average)**2,scores,0))/len(scores))
    #print "Median", 2**(1+median)
    #print "Average", 2**(1+average)
    #print "Variance", 2**(1+variance)
    
    return median, average, variance


def test_sequence_ai(depth = 6):
    moves = [0]*depth
    tested = 0
    
    def increment():
        moves[-1] += 1
        for i in xrange(depth-1,-1,-1):
            if moves[i] > 3:
                moves[i] = 0
                moves[i-1] += 1
            
    mavg = 0
    mmoves = []
    while tested < 4**depth:
        increment()
        
        
    
        ai = RepeatingAI(moves)
        scores = test_ai(ai, timeout=depth)
        _,avg, _ = calc_statistics(scores)
        
        if mavg < avg:
            mavg = avg
            mmoves = moves[:]
            
            print "Moves", moves, avg
        
        tested += 1
        
        
        


def test_lookahead_ai():

    for depth in xrange(1,4):
    
        ai = ObjectiveAI(depth)
        scores = test_ai(ai)
        median,avg,var= calc_statistics(scores)

        print "Depth", depth
        print "Avg:", avg
        print "Var:", var
        print "Median:", median
        print scores
        print
        

#Highscore (d=3):
#512 5593
#1024 5305
#2048 143
#128 46
#256 941

#Highscore (d=3):
#512 152
#1024 228
#2048 11 2.6%
#256 26




#g = GUI()



def gather_statistics(ai, gui=None, log_data=False, trials=100):
    w = World()
    scores = [0]*12
    
    from time import time, sleep
    from os import path, mkdir

    for trial in xrange(trials):
        log = []
        
        log.append(w.store())
        
        while not w.loss():
            move = ai.get_move(w)
            move_applied = w.apply_move(move)
            #sleep(0.1)
            if move_applied:
                log.append(w.store())
                    
                if gui is not None:
                    gui.draw_world(w)
                    
                
        scores[w.greatest_tile]  =  scores[w.greatest_tile]   +1 
        
        folder = path.join("logs",str(2**(1+w.greatest_tile)))
        if not path.exists(folder):
            mkdir(folder)
        
        if log_data:
            f = open(path.join(folder, str(int(time()*100))), "w")
            
            for line in log:
                f.write(line + "\n")
            
            f.close()
        #print "Highscore:"
        #for key, value in scores.items():
            #print 2**(key+1), value
        #print
        #print
        w = World()
    return scores

def print_readable(scores):
    for key, value in enumerate(scores):
        print 2**(key+1), ":", value
        
if __name__=="__main__":
    g =  GUI()
    #w = World()
    #for i in xrange(4):
        #for j in xrange(4):
            #w.data[i][j] = i*4+(i%2)*j+(1-i%2)*(3-j)
    #g.draw_world(w)
    #sleep(5)
    for depth in xrange(3,6):
        print "Depth:", depth
        
        
        #ai = ObjectiveAI(depth, False)
        #print "Without pred. random:"
        #scores = gather_statistics(ai,g)
        #print_readable(scores)
        
        
        print 
        
        ai = ObjectiveAI(depth, True)
        print "With pred. random:"
        scores = gather_statistics(ai,g, trials=1000,log_data=True)
        print_readable(scores)
        
        print
        print
