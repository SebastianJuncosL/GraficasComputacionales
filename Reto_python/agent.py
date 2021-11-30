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


class Vehicle(Agent):

    """
    Agent that moves randomly.
    Attributes:
        unique_id: Agent's ID 
        direction: Randomly chosen direction chosen from one of eight directions
    """

    def __init__(self, unique_id, model):
        """
        Creates a new random agent.
        Args:
            unique_id: The agent's ID
            model: Model reference for the agent
        """
        super().__init__(unique_id, model)

    def move(self):
        """ 
        Determines if the agent can move in the direction that was chosen
        """
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            # Boolean for whether to use Moore neighborhood (including diagonals) or Von Neumann (only up/down/left/right).
            moore=True,
            include_center=True)

        # Checks which grid cells are empty
        freeSpaces = list(map(self.model.grid.is_cell_empty, possible_steps))

        next_moves = [p for p, f in zip(
            possible_steps, freeSpaces) if f == True]

        next_move = self.random.choice(next_moves)
        # Now move:
        if self.random.random() < 0.1:
            self.model.grid.move_agent(self, next_move)
            self.steps_taken += 1

        # If the cell is empty, moves the agent to that cell; otherwise, it stays at the same position
        # if freeSpaces[self.direction]:
        #     self.model.grid.move_agent(self, possible_steps[self.direction])
        #     print(f"Se mueve de {self.pos} a {possible_steps[self.direction]}; direction {self.direction}")
        # else:
        #     print(f"No se puede mover de {self.pos} en esa direccion.")

    def step(self):
        """ 
        Determines the new direction it will take, and then moves
        """
        # self.direction = self.random.randint(0,8)
        # print(f"Agente: {self.unique_id} movimiento {self.direction}")
        # self.move()
        pass
