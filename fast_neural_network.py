from pybrain.structure import FeedForwardNetwork
from pybrain.structure import FullConnection
from pybrain.structure import LinearLayer, SigmoidLayer




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
    
    
def create_ann(layout):
    n = FeedForwardNetwork()
    
    num_in = layout[0]
    
    inLayer = LinearLayer(num_in)
    n.addInputModule(inLayer)
    
    last_layer = inLayer
    
    for node_count in layout[1:-1]:
        current_layer = SigmoidLayer(node_count)
        n.addModule(current_layer)    
        last_to_current = FullConnection(last_layer, current_layer)
        n.addConnection(last_to_current)
        last_layer = current_layer
        
    
    outLayer = LinearLayer(layout[-1])
    n.addOutputModule(outLayer)
    hidden_to_out = FullConnection(last_layer, outLayer)
    n.addConnection(hidden_to_out)
    
    n.sortModules()
    
    return n
    




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

def load_trainingset(folder, number_of_games=None):
    
    from os import listdir
    from os.path import isfile, join 
    
    games = []
    
    
    for filename in [join(folder,f) for f in listdir(folder) if isfile(join(folder,f))]:
        states = []
        
        f = open(filename)
        for line in f.readlines():
            w = World()
            w.load(line)
            states.append(w)
        
        games.append(states)
        
        if number_of_games is not None and len(games) > number_of_games:
            break
        
    return games
    
TRAINING_SET = load_trainingset("logs/2048",1)

ANN = create_ann(LAYOUT)

gui = None#GUI()
def evaluate_ann(individual):
    global ANN
    
    ANN._setParameters([x for x in individual])
    
    def evalution_helper(state):
        inputs = []
        for i in xrange(4):
            for j in xrange(4):
                if state.data[i][j] is None:
                    inputs.append(0)
                else:
                    inputs.append(state.data[i][j]+1)
                
            
        return ANN.activate(inputs)
    
    fit = 1.0
    rounds = 0
    
    for game in TRAINING_SET[:1]:
        for i in xrange(len(game)-10):
            
            cur_state = game[i]
            
            next_state = game[i+1]
            evaluation = evalution_helper(next_state)
            fit += evaluation
            
            for move in xrange(4):
                if move == cur_state.last_move:
                    continue
            
                cw = cur_state.copy()
                cw.apply_move(move,True)
                
                evaluation = evalution_helper(cw)
                
                fit -= evaluation
        rounds += (len(game)-10)*4
        
    
    fit /= rounds
    #print fit
    return fit,

toolbox.register("evaluate", evaluate_ann)
toolbox.register("mate", tools.cxOnePoint)
toolbox.register("mutate", tools.mutGaussian, mu=0,sigma=0.5,indpb=0.1)
toolbox.register("select", tools.selRoulette)

def main():
    global gui
    random.seed(64)
    NGEN = 100
    MU = 100
    LAMBDA = 200
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
            
    
    return pop, stats, hof
           
def test_vizualize(weights):
    
    ANN._setParameters(weights)
    
    def evalution_helper(state):
        inputs = []
        for i in xrange(4):
            for j in xrange(4):
                if state.data[i][j] is None:
                    inputs.append(-1)
                else:
                    inputs.append(state.data[i][j])
                
            
        return ANN.activate(inputs)
        
        
    ai = ObjectiveAI(3,finalstate_evaluator=evalution_helper)
    
    gui = GUI()
    
    for trial in xrange(10):
        w = World()
        while not w.loss():
            move = ai.get_move(w)
            if w.apply_move(move):
                gui.draw_world(w)
    
if __name__ == "__main__":
    main()                 
    #test_vizualize([-0.63326265570817, 0.32332123347403474, -0.2921571427782797, -0.25639110983437563, -0.1718894635137278, 0.5706571657658108, -0.9597955894078642, 0.5664840027952338, 0.6493569403746713, 0.5551551640829158, 0.6449118068855639, -0.4240090759077886, 0.908443825008902, -0.1291095705838181, 1.1560146589620408, 0.37255623182135444, -0.621188050278497, -0.6833208657798422, -0.7012558569959397, 0.7949807438579874, -0.6851435688400374, -0.6566411437122146, 0.3983183656051372, -0.6712410742403672, 0.49650515532913575, 0.11962424268553473, 0.1722607293307425, -0.6462562655398616, -0.1871457461209567, -0.07709075265702214, -0.5120079082856313, -0.5201333695183296, 0.2765981058202096, -0.09778777622972679, -0.6126352879562122, 0.5420380940295875, 0.6247756615106612, -0.585853564460656, 0.3882904943715848, 0.1971189465183909, -0.7499005947035491, 0.7788152772196213, 0.537224756389687, 0.8869159362373213, -0.010328521457709225, 0.7854698546414112, 0.8844917853773147, -0.012293173872309882, 0.483313947706965, 0.6513440780571946, 0.5200351255842683, -0.4696918007223019, -0.22775729632572062, 0.6308599858711976, 0.6978603542071229, -1.703058888068534, 0.6213328336106865, 0.6480097918877554, 0.18188510737356522, 0.4995737691731803, -0.9417552907312612, 0.8502552584783039, 0.5965788702147241, 0.15819614334197118, -0.9602982275658469, -0.8606096061669462, -1.1468050042650926, -0.8449753990241282])
