
import pygame

class GUI(object):
    def __init__(self):
        pygame.init()
        self.square_size = 100
        
        width = self.square_size*4+10
        height = self.square_size*4+10
        self.window_size = [width,height]
        self.surface = pygame.display.set_mode(self.window_size)
    
    def get_color(self, value):
        #return (255,0,0)
        if value is None:
            return (30,30,30)
            
        return (50,min(250,int(50+ 200/11.0 * value)), 50)
        
    def draw_number(self, square_x, square_y, number):
        font = pygame.font.Font(None,48)
        white = (255,255,255)
        text = font.render(str(number), 1, white)
        offset_x = self.square_size*0.5-text.get_width()*0.5
        offset_y = (self.square_size-text.get_height())*0.5
        self.surface.blit(text, (int(square_x*self.square_size+offset_x), int((square_y)*self.square_size+offset_y)))   
        
    def draw_world(self, world):
        for i in xrange(4):
            for j in xrange(4):
                color = self.get_color(world.data[i][j])
                
                self.draw_square( i, j, color)
                if world.data[i][j] is not None:
                    self.draw_number(i,j, 2**(1+world.data[i][j]))
        pygame.display.flip()
    
    def draw_square(self,square_x,square_y, color, offset_x = 0, offset_y = 0):
        x = 5 + square_x* (self.square_size ) + offset_x
        y = 5 + square_y* (self.square_size ) + offset_y
        pygame.draw.rect(self.surface, color, (x,y,self.square_size,self.square_size))

        x = 5 + square_x* (self.square_size) + offset_x + 2
        y = 5 + square_y* (self.square_size) + offset_y + 2
        pygame.draw.rect(self.surface, map(lambda x: x*0.6, color), (x,y,self.square_size - 4,self.square_size - 4))
    def run(self,world):
        from time import time
        from os import path
        
        f = open(path.join("logs", str(int(time()))), "w")
        
        
        self.draw_world(world)
        f.write(world.store() + "\n")

        while not world.loss():
        

            for event in pygame.event.get(): 
                
                if event.type == pygame.QUIT: 
                    pygame.quit()
                    return
                elif event.type == pygame.KEYDOWN:
                    move_applied = False
                    print event.key
                    if event.key == 273:
                        move_applied = world.apply_move(LEFT)
                        
                    elif event.key == 274:
                        move_applied = world.apply_move(RIGHT)
                    
                    elif event.key == 275:
                        move_applied = world.apply_move(DOWN)
                    
                    elif event.key == 276:
                        move_applied = world.apply_move(UP)
                            
                    if move_applied:
                        self.draw_world(world)
                        f.write(world.store() + "\n")
                        
        self.draw_world(world)
        f.write(world.store() + "\n")
        f.close()
    
        while True:
        
            for event in pygame.event.get(): 
                
                if event.type == pygame.QUIT: 
                    pygame.quit()
                    return


if __name__=="__main__":
    from world import *
    w = World()
    g = GUI()
    g.run(w)
