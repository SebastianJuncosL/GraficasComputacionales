from mesa import Agent

class Road(Agent):
    """
    Obstacle agent. Just to add obstacles to the grid.
    """
    """Directions:
        up ^
        down v
        left <
        right >
        none X
    """

    def __init__(self, unique_id, model, direction="None"):
        super().__init__(unique_id, model)
        self.direction = direction

    def step(self):
        pass


class Building(Agent):
    """
    Obstacle agent. Just to add obstacles to the grid.
    """

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass


class Stoplight(Agent):
    """
    Obstacle agent. Just to add obstacles to the grid.
    """

    def __init__(self, unique_id, model, state="green", timeToChange=10):
        super().__init__(unique_id, model)
        self.state = state
        self.timeToChange = timeToChange
        self.current = 0
        if self.state == "red":
            self.current = 10

    def step(self):
        self.current += 1
        if self.current == 8:
            self.state = "yellow"
        elif self.current == 10:
            self.state = "red"
        elif self.current == 20:
            self.current = 0
            self.state = "green"

class Destination(Agent):
    """
    Obstacle agent. Just to add obstacles to the grid.
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass


class Vehicle(Agent):

    """
    Agent that moves randomly.
    Attributes:
        unique_id: Agent's ID 
        direction: Sets next direction to advance
    """

    def __init__(self, unique_id, model, pos, destination_pos, direction = "up"):
        """
        Creates a new random agent.
        Args:
            unique_id: The agent's ID
            model: Model reference for the agent
        """
        super().__init__(unique_id, model)
        self.pos = pos
        self.destination_pos = destination_pos
        self.impossible_steps = set()
        self.direction = direction

    def step(self):
        """ 
        Determines if the agent can move in the direction that was chosen
        """
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            # Boolean for whether to use Moore neighborhood (including diagonals) or Von Neumann (only up/down/left/right).
            moore=True,
            include_center=False)
        
        cell = self.model.grid.get_cell_list_contents(self.pos)[0]
        if (isinstance(cell, Road) and cell.direction != "None"):
            self.direction = cell.direction

        #Check direction and quit back spaces.
        if (self.direction == "Up"):
            possible_steps = list(filter(lambda x : (x[1] == self.pos[1]+1), possible_steps))
        elif (self.direction == "Down"):
            possible_steps = list(filter(lambda x : (x[1] == self.pos[1]-1), possible_steps))
        elif (self.direction == "Left"):
            possible_steps = list(filter(lambda x : (x[0] == self.pos[0]-1), possible_steps))
        else:
            possible_steps = list(filter(lambda x : (x[0] == self.pos[0]+1), possible_steps))
        
        if (self.destination_pos in possible_steps):
            print("Llegue a mi destino!")
            self.model.grid.move_agent(self, self.destination_pos)
            return

        free_spaces = []
        # Quit obstacles.
        for i in range(len(possible_steps)):
            cell_agents = self.model.grid.get_cell_list_contents(possible_steps[i])
            for agent in cell_agents:
                if (isinstance(agent, Road) or (isinstance(agent, Stoplight) and (agent.state == "green"))):
                    free_spaces.append(possible_steps[i])
        
        if (len(free_spaces) == 0):
            print(f"Vehicle {self.unique_id} don't move this step.")
            return
        
        # Check distance.
        min_distance = self.distance(free_spaces[0])
        min_pos = free_spaces[0]

        for pos in free_spaces:
            distance = self.distance(pos)
            if (distance < min_distance):
                min_distance = distance
                min_pos = pos
        
        # Now move:
        print(f"Se mueve de {self.pos} a {min_pos} direction", self.direction, f"y quiere ir a {self.destination_pos}" )
        self.model.grid.move_agent(self, min_pos)

        if (self.pos == self.destination_pos):
            self.model.running = False


    # def move(self, next_pos):
    #     #print("Move Collector", self.unique_id, "to:", next_pos)
    #     self.model.grid.move_agent(self, next_pos)  # Checar con servidor
    
    def distance(self, next_pos):
        return ((next_pos[0]-self.destination_pos[0])**2 + (next_pos[1]-self.destination_pos[1])**2)**(1/2)
