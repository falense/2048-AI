
class RepeatingAI(object):
    def __init__(self, moves):
        self.moves = moves
        self.state = 0
        
    def get_move(self,world):
        self.state = (self.state+1)%len(self.moves)
        return self.moves[self.state]
