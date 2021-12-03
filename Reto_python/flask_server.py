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


@app.route("/", methods=['POST'])
def default():
    global model
    if request.method == 'POST':
        readModel()
        N = int(request.form.get('NAgents'))
        model = StreetModel(N)
        return jsonify({"cityMap": city_map})

@app.route("/updatePositions", methods=['GET'])
def updatePositions():
    global model
    if request.method == 'GET':
        vehicles_pos = [{"x": x, "y": 0.5, "z": z} for a, x, z in model.grid.coord_iter(
        ) for agent in a if isinstance(agent, Vehicle)]
        vehicles_id = [agent.unique_id for a, x, z in model.grid.coord_iter(
        ) for agent in a if isinstance(agent, Vehicle)]

        vehicles = {}
        for i in range(len(vehicles_id)):
            vehicles[vehicles_id[i]] = vehicles_pos[i]
        
        sorted_pos = []
        for i in sorted(vehicles.keys()):
            sorted_pos.append(vehicles[i])

        return jsonify({"vehiclesPositions" : sorted_pos})
        # "vehiclesPositions": vehicles_pos, "vehiclesIds": vehicles_id, "sortedDict" : vehicles, 


@app.route("/updateStates", methods=['GET'])
def updateStates():
    global model
    if request.method == 'GET':
        stoplights_stat = [agent.state for a, x, z in model.grid.coord_iter(
        ) for agent in a if isinstance(agent, Stoplight)]
        stoplights_id = [agent.unique_id for a, x, z in model.grid.coord_iter(
        ) for agent in a if isinstance(agent, Stoplight)]
        newIDs = []
        for i in stoplights_id:
            if len(i) <= 4:
                newString = i[:2] + '0' + i[2:]
                newIDs.append(newString)
            else:
                newIDs.append(i)

        stoplights = {}
        for i in range(len(newIDs)):
            stoplights[newIDs[i]] = stoplights_stat[i]

        sortedStoplights = {}
        for i in sorted(stoplights.keys()):
            sortedStoplights[i] = stoplights[i]

        sortedIds = []
        sortedStates = []
        for i in sortedStoplights.keys():
            sortedIds.append(i)
            sortedStates.append(sortedStoplights[i])

        return jsonify({"ids": sortedIds, "states": sortedStates})


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


@app.route("/generateVehicle", methods=['GET'])
def generateVehicle():
    global model
    model.generateVehicle()


if __name__ == '__main__':
    app.run(host="localhost", port=8585, debug=True)
