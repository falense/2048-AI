from random import randint, seed, choice
from math import sqrt
from time import sleep

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

def make_matrix(n,m):
    r = []
    for mi in xrange(m):
        row = [None]*n
        r.append(row)
    return r

class World(object):
    def __init__(self):
        self.data = make_matrix(4,4)
        self.open_tiles = 4*4 
        
        self.attempted_moves = set()
        
        self.populate_tile()
        self.populate_tile()
        
        self.greatest_tile = self.find_greatest_tile()
        
        self.last_move = None
        
    def find_greatest_tile(self):
        m = 0
        for i in xrange(4):
            for j in xrange(4):
                if self.data[i][j] > m:
                    m = self.data[i][j]
        return m
        
    def populate_tile(self):
        if self.open_tiles == 0:
            return 
            
        i,j = (randint(0,3), randint(0,3))
        
        if self.data[i][j] is None:
            self.data[i][j] = randint(0,1)
            self.open_tiles -= 1
        else:
            self.populate_tile()
        
    def __repr__(self):
        output = ""
        for row in self.data:
            output += "\t".join(map(self.tile_readable,row)) + "\n"
        return output
    
    def tile_readable(self, value):
        if value is not None:
            return str(2**(1+value))
        else:
            return str(value)
            
    def apply_rules(self, array, f, j, ff, df, merged):
        if array[j] is not None:
            if f == ff:
                #print "Rule 1"
                f += df
                array[f] = array[j]
                merged = False
                
            elif array[f] == array[j] and merged is False:
               # print "Rule 2"
                array[f] += 1
                self.open_tiles += 1
                self.greatest_tile = max(array[f], self.greatest_tile)
                self.attempted_moves = set()
                merged = True
                
            else:
                #print "Rule 3"
                f += df
                array[f] = array[j]
                merged = False
                
            if f != j:
                #print "Clearing"
                array[j] = None
                self.attempted_moves = set()
        return array, f, merged
            
    def concat_backwards(self, array):
        f = -1
        merged = False
        for j in xrange(4):
            array, f, merged = self.apply_rules(array,f,j, -1, 1, merged)
                    
        return array
        
    def concat_forward(self, array):
        f = 4
        merged = False
        for j in xrange(3, -1, -1):
            array, f, merged = self.apply_rules(array,f,j, 4, -1, merged)
            
        return array
        
    def slide_left(self):
        for i in xrange(4):
            self.data[i] = self.concat_backwards(self.data[i])
            
    def slide_right(self):
        for i in xrange(4):
            self.data[i] = self.concat_forward(self.data[i])
            
    def get_column(self,j):
        return map(lambda array: array[j], self.data)
        
    def slide_up(self):
        for j in xrange(4):
            col = self.get_column(j)
            col = self.concat_backwards(col)
            for i, value in enumerate(col):
                self.data[i][j] = value    
                
    def slide_down(self):
        for j in xrange(4):
            col = self.get_column(j)
            col = self.concat_forward(col)
            for i, value in enumerate(col):
                self.data[i][j] = value
        
    def apply_move(self, move, no_new_tile=False):
        self.attempted_moves.add(move)
        if move is UP:
            self.slide_up()
        if move is RIGHT:
            self.slide_right()
        if move is DOWN:
            self.slide_down()
        if move is LEFT:
            self.slide_left()
        
        if len(self.attempted_moves) == 0:
            self.last_move = move
            if not no_new_tile: 
                self.populate_tile()
            return True
        else:
            return False
        
    def loss(self):
        if self.open_tiles == 0:
            no_move = True
            for i in xrange(4):
                for j in xrange(4):
                    if i+1 < 4 and self.data[i][j] == self.data[i+1][j]:
                        no_move = False
                        
                    if i-1 >= 0 and self.data[i][j] == self.data[i-1][j]:
                        no_move = False
                        
                    if j+1 < 4 and self.data[i][j] == self.data[i][j+1]:
                        no_move = False
                        
                    if j-1 >= 0 and self.data[i][j] == self.data[i][j-1]:
                        no_move = False
            return no_move
        else:
            return False
    def __get_surrounding(self, i,j):
        r = []
        if i+1 < 4 and self.data[i+1][j] is not None:
            r.append(self.data[i+1][j])
                    
        if i-1 >= 0  and self.data[i-1][j] is not None:
            r.append(self.data[i-1][j])

        if j+1 < 4 and self.data[i][j+1]  is not None:
            r.append(self.data[i][j+1])

        if j-1 >= 0 and self.data[i][j-1] is not None:
            r.append(self.data[i][j-1])
                    
        return r
    def score(self):
        #return self.open_tiles
        
        s = 0
        for i in xrange(4):
            for j in xrange(4):
                if self.data[i][j] is not None:
                    t = 2**(1+self.data[i][j]+(j)) * (i+1)
                    #for value in self.__get_surrounding(i,j):
                        #if abs(value - self.data[i][j]) == 1:
                            #t *= 2
                    s += t 
        return s
        
    def copy(self):
        w = World()
        for i in xrange(4):
            w.data[i] = self.data[i][:]
        w.open_tiles = self.open_tiles
        w.attempted_moves = set(self.attempted_moves)
        w.greatest_tile = self.greatest_tile
        return w
        
    def find_open_tiles(self):
        tiles = []
        for i in xrange(4):
            for j in xrange(4):
                if self.data[i][j] is None:
                    tiles.append((i,j))
        return tiles

    def store(self):
        s = []
        for i in xrange(4):
            s.extend(self.data[i][:])
        
        s.append(self.open_tiles)
        s.append(self.greatest_tile)
        s.append(self.last_move)
        
        return " ".join(map(str,s))
    
    def load(self, data_str):
        data_temp = data_str.split(" ")
        assert len(data_temp) == 19
        
        for i in xrange(4):
            for j in xrange(4):
                try:
                    value = int(data_temp[i*4+j])
                    self.data[i][j] = value
                except:
                    self.data[i][j] = None
        
        self.open_tiles = int(data_temp[16])
        self.greatest_tile = int(data_temp[17])
        
        try:
            self.last_move = int(data_temp[18])
        except:
            pass
        
        #for i in xrange(4):
            #for j in xrange(4):
                #if self.data[i][j] is None:
                    #self.open_tiles += 1
                    
        #self.greatest_tile = self.find_greatest_tile()

            
if __name__=="__main__":
    w = World()
    string = w.store()
    print w
    print string
    w2 = World()
    w2.load(string)
    print w2
        
        
