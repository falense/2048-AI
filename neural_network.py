from pybrain.structure import FeedForwardNetwork
from pybrain.structure import FullConnection
from pybrain.structure import LinearLayer, SigmoidLayer


from fast_neural_network import create_ann


import random

import numpy

from deap import algorithms
from deap import base
from deap import creator
from deap import tools


LAYOUT = [16,4,1]


IND_INIT_SIZE = 0
for i in xrange(1,len(LAYOUT)):
    IND_INIT_SIZE += LAYOUT[i-1]*LAYOUT[i]
    

# To assure reproductibility, the RNG seed is set prior to the items
# dict initialization. It is also seeded in main().
random.seed(64)


creator.create("Fitness", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.Fitness)

toolbox = base.Toolbox()

# Attribute generator
toolbox.register("weight", random.uniform, -1.0,1.0)

# Structure initializers
toolbox.register("individual", tools.initRepeat, creator.Individual, 
    toolbox.weight, IND_INIT_SIZE)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    
from main import gather_statistics
from GUI import GUI
from ai.ObjectiveAI import ObjectiveAI
from world import World

gui = None#GUI()
def evaluate_ann(individual):
    n = create_ann(LAYOUT)
    
    
    n._setParameters([x for x in individual])
    
    def evalution_helper(state):
        inputs = []
        for i in xrange(4):
            for j in xrange(4):
                if state.data[i][j] is None:
                    inputs.append(0)
                else:
                    inputs.append(2**(1+state.data[i][j]))
                
            
        return n.activate(inputs)
    
    ai = ObjectiveAI(1,finalstate_evaluator=evalution_helper)
    
    
    num_trials = 2
    fit = 0.0
    for trial in xrange(num_trials):
        w = World()
        while not w.loss():
            move = ai.get_move(w)
            w.apply_move(move)
            if gui is not None:
                gui.draw_world(w)
            
        fit += w.score()
        
    fit /= num_trials
    print fit
        
    return fit,

toolbox.register("evaluate", evaluate_ann)
toolbox.register("mate", tools.cxOnePoint)
toolbox.register("mutate", tools.mutGaussian, mu=0,sigma=0.5,indpb=0.1)
toolbox.register("select", tools.selRoulette)

def main():
    global gui
    random.seed(64)
    NGEN = 100
    MU = 20
    LAMBDA =40
    CXPB = 0.7
    MUTPB = 0.2
    
    pop = toolbox.population(n=MU)
    hof = tools.ParetoFront()
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean, axis=0)
    stats.register("std", numpy.std, axis=0)
    stats.register("min", numpy.min, axis=0)
    stats.register("max", numpy.max, axis=0)
    
    for x in xrange(NGEN):
        algorithms.eaMuPlusLambda(pop, toolbox, MU, LAMBDA, CXPB, MUTPB, 2, stats,
                                  halloffame=hof)
    
        for ind in hof:
            print ind
            
            gui = GUI()
            
            evaluate_ann(ind)
            gui = None
            
    
    return pop, stats, hof
                 
if __name__ == "__main__":
    main()                 


