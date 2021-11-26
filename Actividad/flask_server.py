from flask import Flask, request, jsonify
from model import *

# Create the flask service

num_rovers = 0
num_boxes = 0

width = 10
height = 10
model = None

app = Flask("Collectors")


@app.route("/init", methods=['POST'])
def default():
    global num_rovers, num_boxes, height, width, model

    if request.method == 'POST':
        num_rovers = int(request.form.get('numRovers'))
        num_boxes = int(request.form.get('numBoxes'))
        width = int(request.form.get('width'))
        height = int(request.form.get('height'))

        print(request.form)
        model = CollectorsModel(num_rovers, num_boxes, height, width)
        return jsonify({"Ok": num_rovers})


@app.route("/getDelivery", methods=['GET'])
def getDelivery():
    global model
    (x, z) = model.delivery_pos

    return jsonify({'deliveryPos': {"x": x, "y": 0.04, "z": z}})


@app.route("/UpdatePositions", methods=['GET'])
def configure():
    """Set up the simulation"""
    global model

    if request.method == 'GET':
        boxes_pos = [{"x": x, "y": 1.02, "z": z} for (a, x, z) in model.grid.coord_iter() for agent in a if isinstance(agent, Box)]
        collecors_pos = [{"x": x, "y": -0.02, "z": z} for (a, x, z) in model.grid.coord_iter() for agent in a if isinstance(agent, Collector)]

        print(boxes_pos, collecors_pos)
        return jsonify({'boxesPositions': boxes_pos, 'collectorsPositions': collecors_pos})


@app.route("/updateModel", methods=['GET'])
def update_position():
    """Create a list of 3d Points"""
    global model

    if request.method == 'GET':
        model.step()
        return jsonify({'message': 'Model updated'})


if __name__ == '__main__':
    app.run(host="localhost", port=8585, debug=True)
