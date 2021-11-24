from mesa import Agent


class Delivery(Agent):
    # Donde van a poner las cajas.
    def __init__(self, pos, model):
        super().__init__(pos, model)
        self.pos = pos

    def step(self):
        pass


class Box(Agent):
    # Cajas a recolectar.
    def __init__(self, unique_id, pos, delivery_pos, model):
        super().__init__(unique_id, model)
        self.unique_id = unique_id
        self.pos = pos
        self.delivery_pos = delivery_pos
        self.state = False
    
    def step(self):
        pass
    
    def take_box(self):
        self.state = True
    
    def drop_box(self):
        self.state = False

    def move(self, pos):
        print("Move Box", self.unique_id, "to:", pos)
        self.model.grid.move_agent(self, pos) # Checar con servidor


class Collector(Agent):
    # Persona que recojera cajas.
    def __init__(self, unique_id, pos, delivery_pos, model):
        super().__init__(unique_id, model)
        self.unique_id = unique_id
        self.pos = pos
        self.delivery_pos = delivery_pos
        self.box = -1
        self.impossible_steps = set()
    
    def move(self, next_pos):
        #print("Move Collector", self.unique_id, "to:", next_pos)
        self.model.grid.move_agent(self, next_pos) # Checar con servidor

    def step(self):
        steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=False,
            include_center=False)
        possible_box = []
        possible_steps = []

        # check for obstacles
        for i in range(len(steps)):
            cell = self.model.grid.get_cell_list_contents([steps[i]])
            if (len(cell) == 0):
                possible_steps.append(steps[i])
            elif(isinstance(cell[0], Box)):
                possible_box.append(steps[i])
        
        # Comunication (Tentativo)
        
        # Drop box.
        for pos in steps:
            cell = self.model.grid.get_cell_list_contents(pos)
            if (self.box != -1 and len(cell) > 0 and isinstance(cell[0], Delivery)):
                print(f"Collector {self.unique_id} drop in delivery box {self.box.unique_id}")
                self.box.move(pos)
                self.box = -1
                pass

        # Go to delivery
        if (self.box != -1):
            possible_steps = list(set(possible_steps) - self.impossible_steps)
            min_step = possible_steps[0]
            min_dist = self.getDistance(min_step)
            for step in possible_steps:
               current_dist = self.getDistance(step)
               if (current_dist < min_dist):
                   min_step = step
                   min_dist = current_dist
            if (min_dist > self.getDistance(self.pos)):
                self.impossible_steps.add(self.pos)
            self.move(min_step)
            self.box.move(min_step)
        
        # Take box
        elif (len(possible_box)):
            cell = self.model.grid.get_cell_list_contents([possible_box[0]])[0]
            self.box = cell
            cell.take_box()
            self.box.move(self.pos)
        
        # Move randomly
        else:
            direction = self.random.randint(0,len(possible_steps)-1)
            self.move(possible_steps[direction])

    def getDistance(self, dest):
        return ((dest[0]-self.delivery_pos[0])**2+(dest[1]-self.delivery_pos[1])**2)**(1/2)
