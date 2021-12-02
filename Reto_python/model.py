from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa import Model
from agent import *
import json
import random

class StreetModel(Model):
    def __init__(self, N = 5):
        self.running = True
        self.num_steps = 0
        self.num_vehicles = 0

        dataDictionary = json.load(open("mapDictionary.txt"))

        with open('base.txt') as baseFile:
            lines = baseFile.readlines()
            self.width = len(lines[0])-1
            self.height = len(lines)

            self.grid = MultiGrid(self.width, self.height, torus=False)
            self.schedule = RandomActivation(self)
            self.destinations = []

            for r, row in enumerate(lines):
                for c, col in enumerate(row):
                    if col in ["v", "^", ">", "<", "X"]:
                        agent = Road(f"r{r*self.width+c}",
                                     self, dataDictionary[col])
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                    elif col in ["S", "s"]:
                        agent = Stoplight(
                            f"tl{r*self.width+c}", self, "green" if col == "S" else "red", int(dataDictionary[col]))
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                        self.schedule.add(agent)
                    elif col == "#":
                        agent = Building(f"ob{r*self.width+c}", self)
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                    elif col == "D":
                        agent = Destination(f"d{r*self.width+c}", self)
                        self.destinations.append((c, self.height - r - 1))
                        self.grid.place_agent(agent, (c, self.height - r - 1))

        for i in range(N):

            self.generateVehicle()


    def step(self):
        '''Advance the model by one step.'''
        self.schedule.step()

    def pos_gen(self, w, h):
        return (self.random.randrange(w), self.random.randrange(h))

    def generateVehicle(self):
        self.num_vehicles += 1
        pos = self.pos_gen(self.grid.width, self.grid.height)
        while (not isinstance(self.grid.get_cell_list_contents(pos)[0], Road) or self.grid.get_cell_list_contents(pos)[0].direction == "None"):
            pos = self.pos_gen(self.grid.width, self.grid.height)
        
        a = Vehicle(2000 + self.num_vehicles, self, pos, random.choice(self.destinations), self.grid.get_cell_list_contents(pos)[0].direction)
        self.schedule.add(a)
        self.grid.place_agent(a, pos)
