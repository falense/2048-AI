from pybrain.structure import FeedForwardNetwork
from pybrain.structure import FullConnection
from pybrain.structure import LinearLayer, SigmoidLayer




import random

import numpy

LAYOUT = [16,8,1]



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
    

random.seed(64)


    
from main import gather_statistics
from GUI import GUI
from ai.ObjectiveAI import ObjectiveAI
from world import World

from fast_neural_network import load_trainingset
TRAINING_SET = load_trainingset("logs/2048")

ANN = create_ann(LAYOUT)

    
def serialize_state(state):
    inputs = []
    for i in xrange(4):
        for j in xrange(4):
            if state.data[i][j] is None:
                inputs.append(0)
            else:
                inputs.append(2**(state.data[i][j]+1))
            
        
    return inputs
    
def train_ann(training_games):
    global ANN
    
    from pybrain.datasets import SupervisedDataSet
    from pybrain.supervised.trainers import BackpropTrainer
    
    ds = SupervisedDataSet(16, 1)

    DATASET_LENGTH = 10000
    
    
    for game in TRAINING_SET:
        for i in xrange(len(game)-10):
            
            cur_state = game[i]
            
            next_state = game[i+1]
            
            ds.addSample(serialize_state(next_state),1)
            
            for move in xrange(4):
                if move == cur_state.last_move:
                    continue
            
                cw = cur_state.copy()
                cw.apply_move(move,True)
                
                ds.addSample(serialize_state(cw),-1)
                
            if len(ds) > DATASET_LENGTH:
                break
                
        if len(ds) > DATASET_LENGTH:
            break
    print len(ds)
            
    trainer = BackpropTrainer(ANN, ds)
    
    error = 1.0
    breakout = 100
    while error > 1e-5:
        error = trainer.train()
        print "Error:",error
        breakout -= 1
        if breakout < 0:
            break
    
    return ANN.params
           
def test_vizualize(weights):
    ANN._setParameters(weights)
    
    def evalution_helper(state):
        return ANN.activate(serialize_state(state))
        
        
    ai = ObjectiveAI(4,finalstate_evaluator=evalution_helper)
    
    gui = GUI()
    
    while 1:
        w = World()
        while not w.loss():
            move = ai.get_move(w)
            if w.apply_move(move):
                gui.draw_world(w)
            
    
if __name__ == "__main__":
    training_set = load_trainingset("logs/2048")
    
    weights = train_ann(training_set)   
    print weights
    test_vizualize(weights)
    
