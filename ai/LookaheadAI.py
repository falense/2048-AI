from random import choice

class LookaheadAI(object):
    def __init__(self, depth=1):
        self.depth = depth
    
    def get_move(self, world):
        current_states = [([],world.copy())]
        
        for d in xrange(self.depth):
            new_states = []
            for history,state in current_states:
                for move in xrange(4):
                    chistory = history[:]
                    chistory.append(move)
                    cstate = state.copy()
                    cstate.apply_move(move, no_new_tile=True)
                    new_states.append((chistory,cstate))
            current_states = new_states
        
        best_score = None
        best_list = []
        for  history, state in current_states:
            score = state.score()
            if best_score is None or best_score < score:
                best_score = score
                best_list = [history[0]]
            elif best_score <= score:
                best_list.append(history[0])
        return choice(best_list)
