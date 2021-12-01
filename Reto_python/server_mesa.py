from agent import *
from model import StreetModel
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer

light_color = {"red": "#FF0000", "yellow": "#FFFF00", "green": "#00FF00"}


def agent_portrayal(agent):
    if agent is None:
        return

    portrayal = {"Shape": "rect",
                 "Filled": "true",
                 "Layer": 1,
                 "w": 1,
                 "h": 1
                 }

    if (isinstance(agent, Road)):
        portrayal["Color"] = "grey"
        portrayal["Layer"] = 0

    if (isinstance(agent, Destination)):
        portrayal["Color"] = "lightgreen"
        portrayal["Layer"] = 0

    if (isinstance(agent, Stoplight)):
        portrayal["Color"] = light_color[agent.state]
        portrayal["Layer"] = 0
        portrayal["w"] = 0.8
        portrayal["h"] = 0.8

    if (isinstance(agent, Building)):
        portrayal["Color"] = "cadetblue"
        portrayal["Layer"] = 0
        portrayal["w"] = 0.8
        portrayal["h"] = 0.8

    if (isinstance(agent, Vehicle)):
        portrayal["Color"] = "blue"
        portrayal["Layer"] = 0
        portrayal["w"] = 0.9
        portrayal["h"] = 0.6

    return portrayal


width = 0
height = 0

with open('base.txt') as baseFile:
    lines = baseFile.readlines()
    width = len(lines[0])-1
    height = len(lines)

model_param = {}

canvas_element = CanvasGrid(agent_portrayal, width, height, 500, 500)

server = ModularServer(StreetModel, [canvas_element], "Street", model_param)

server.launch()
