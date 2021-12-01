from os import read
from flask import Flask, request, jsonify
from model import *

# Create the flask service

num_destinations = 0

city_map = []

width = 10
height = 10
model = None

app = Flask("Traffic")


def readModel():
    global city_map, width, height
    city_map = []
    f = open("base.txt", "r")
    for line in f:
        line = line.rstrip()
        city_map.append(line)
    width = len(city_map[0])
    height = len(city_map)
    # print(city_map)


@app.route("/", methods=['GET'])
def default():
    global model
    if request.method == 'GET':
        readModel()
        model = StreetModel()
        return jsonify({"cityMap": city_map})


@app.route("/updatePositions", methods=['GET'])
def updatePositions():
    global model
    if request.method == 'GET':
        vehicles_pos = [{"x": x, "y": 0, "z": z} for a, x, z in model.grid.coord_iter(
        ) for agent in a if isinstance(agent, Vehicle)]
        stoplights_stat = [agent.state for a, x, z in model.grid.coord_iter(
        ) for agent in a if isinstance(agent, Stoplight)]
        return jsonify({"vehiclesPositions": vehicles_pos, "stoplightsStates": stoplights_stat})


@app.route("/updateModel", methods=['GET'])
def updateModel():
    global model
    if request.method == 'GET':
        model.step()
        return jsonify({"message": "Model Updated"})


@app.route("/getMap", methods=['GET'])
def getMap():
    global city_map
    if request.method == 'GET':
        return jsonify({"updatedMap": city_map})


# generateVehicle -> will call model that generates a new car in a random pos
# separate stoplight and vehicle states


if __name__ == '__main__':
    app.run(host="localhost", port=8585, debug=True)
