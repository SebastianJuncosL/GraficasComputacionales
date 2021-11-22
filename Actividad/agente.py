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
    def __init__(self, unique_id, model, delivery_pos):
        super().__init__(unique_id, model)
        self.unique_id = unique_id
        self.delivery_pos = delivery_pos


class Collector(Agent):
    # Persona que recojera cajas.
    def __init__(self, unique_id, pos, delivery_pos, model):
        super().__init__(unique_id, pos, model)
        self.unique_id = unique_id
        self.pos = pos
        self.delivery_pos = delivery_pos
        self.box = -1

    def step(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=False,
            include_center=False)
        possible_box = []

        # check for obstacles
        for i in range(len(possible_steps)):
            cell = self.model.grid.get_cell_list_contents([possible_steps[i]])
            if (cell > 0):
                if (isinstance(cell[0], Collector)):
                    possible_steps.pop(i)
                elif(isinstance(cell[0], Box)):
                    possible_box.append(possible_steps.pop(i))
        # Drop box.
        if (self.box != -1 and self.pos == self.delivery_pos):
            self.box = -1