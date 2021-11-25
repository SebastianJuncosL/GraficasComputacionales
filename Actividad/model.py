from mesa.time import SimultaneousActivation
from mesa.space import MultiGrid
from mesa import Model
from agent import Delivery, Box, Collector

class CollectorsModel(Model):
    def __init__(self, N, N_boxes,  height, width):
        self.num_agents = N
        self.grid = MultiGrid(width, height, torus = False) 
        self.schedule = SimultaneousActivation(self)
        self.running = True 
        self.num_steps = 0
        
        pos_gen = lambda w, h: (self.random.randrange(w), self.random.randrange(h))
        # Add Delivery to a random empty grid cell
        delivery_pos = pos_gen(self.grid.width, self.grid.height)
        a = Delivery(delivery_pos, self)
        self.schedule.add(a)
        self.grid.place_agent(a, delivery_pos)
        
        # Add the agent to a random empty grid cell
        for i in range(self.num_agents):
            pos = pos_gen(self.grid.width, self.grid.height)
            while (not self.grid.is_cell_empty(pos)):
                pos = pos_gen(self.grid.width, self.grid.height)

            a = Collector(i+1000, pos, delivery_pos, self) 
            self.schedule.add(a)
            self.grid.place_agent(a, pos)
        
        for i in range(N_boxes):
            pos_gen = lambda w, h: (self.random.randrange(w), self.random.randrange(h))

            pos = pos_gen(self.grid.width, self.grid.height)
            while (not self.grid.is_cell_empty(pos)):
                pos = pos_gen(self.grid.width, self.grid.height)

            a = Box(i+2000, pos, delivery_pos, self) 
            self.schedule.add(a)
            self.grid.place_agent(a, pos)
    
    def step(self):
        self.schedule.step()
        self.num_steps += 1

