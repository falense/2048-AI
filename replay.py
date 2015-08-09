from world import World

from GUI import GUI

from time import sleep
import os

filename = os.sys.argv[1]

gui = None
def replay(filename):
    global gui
    
    f = open(filename,"r")
    
    if gui is None:
        gui = GUI()
        
    for line in f.readlines():
        w = World()
        w.load(line)
        gui.draw_world(w)
        
        sleep(0.01)
    
    f.close()

    sleep(1)
if os.path.exists(filename):
    replay(filename)
else:
    folder = os.path.dirname(filename)
    
    if not os.path.isfile(folder):
        for filename in [os.path.join(folder,f) for f in os.listdir(folder) if os.path.isfile(os.path.join(folder,f))]:
            replay(filename)
