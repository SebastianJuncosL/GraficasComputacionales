from model import CollectorsModel, Delivery, Box, Collector
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer

def agent_portrayal(agent):
    portrayal = { "Filled": "true"}

    if (isinstance(agent,Collector)):
        portrayal["Shape"] = "circle"
        portrayal["Color"] = "orange"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.7

    elif (isinstance(agent,Box)):
        portrayal["Shape"] = "rect"
        portrayal["Color"] = "blue"
        portrayal["Layer"] = 2
        portrayal["h"] = 0.5
        portrayal["w"] = 0.5
    
    else:
        portrayal["Shape"] = "rect"
        portrayal["Color"] = "green"
        portrayal["Layer"] = 0
        portrayal["h"] = 1
        portrayal["w"] = 1

    return portrayal

grid = CanvasGrid(agent_portrayal, 10, 10, 500, 500)
server = ModularServer(CollectorsModel, [grid], "Collectors", {"N" : 5, "N_boxes" : 5,  "height" : 10, "width" : 10})

server.port = 8521
server.launch()