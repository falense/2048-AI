from random import choice

class ObjectiveAI(object):
    def __init__(self, depth, predict_random=False, finalstate_evaluator=None):
        self.depth = depth
        self.predict_random = predict_random
        self.finalstate_evaluator = finalstate_evaluator
        
        self.available_moves = xrange(3)
        
    def evaluate_state(self, state, depth):
        if depth <= 0:
            if state.loss():
                return 0
            else:
                if self.finalstate_evaluator is not None:
                    return self.finalstate_evaluator(state)
                else:
                    return state.score()
                
        if self.predict_random and state.open_tiles < 4:
            open_tiles = state.find_open_tiles()
            
            score = 0
            for tile in open_tiles:
                for value in xrange(2):
                    for move in self.available_moves:
                        cstate = state.copy()
                        i,j = tile
                        cstate.data[i][j] = value
                        
                        if cstate.apply_move(move, no_new_tile=True):
                            score += self.evaluate_state(cstate, depth-1)
                            
            return score/(2.0*4.0*state.open_tiles)
        
        else:
            score = 0
            for move in self.available_moves:
                cstate = state.copy()
              
                
                if cstate.apply_move(move, no_new_tile=True):
					score += self.evaluate_state(cstate, depth-1)
            
            return score/4.0
            
        
    def get_move(self, world):
        #if world.open_tiles  <= 10:
            #self.depth = 3
        #if world.open_tiles  <= 4:
            #self.depth = 4
        #if world.open_tiles <= 3:
            #self.depth = 6
        #if world.open_tiles <= 2:
            #self.depth = 7
            
        #if world.open_tiles < 4:
        #    self.available_moves = xrange(4)
        #if world.open_tiles > 8:
        #    self.available_moves = xrange(3)
        
        best_score = 0
        best_list = []
        
        for move in self.available_moves:
            cstate = world.copy()
            
            if not cstate.apply_move(move, no_new_tile=True):
                continue
                
            score = self.evaluate_state(cstate, self.depth-1)
            
            if best_score == 0 or best_score < score:
                best_list = [move]
                best_score = score
                
            elif abs(best_score-score) < 0.1:
                best_list.append(move)
                
        if len(best_list) == 0:
            print "Found no move, defaulting"
            return 3
        
        return choice(best_list)
