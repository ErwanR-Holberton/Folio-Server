#!/usr/bin/env python3
from flask import Flask, request, render_template
import json
from waitress import serve

app = Flask(__name__)

def get_tiles():
    try:
        with open("tiles.json", "r") as file:
            tiles = file.read()
            if tiles == None:
                return "{}"
            return tiles
    except Exception:
        return "{}"

@app.route('/tiles')
def all_tiles():
    return get_tiles()

@app.route('/status')
def status():
    return "OK"

@app.route('/post_tile', methods=['POST'], strict_slashes=False)
def post_tile():
    data = request.get_json()
    print(data)

    if data is None:
        return "Error"

    try:
        with open("tiles.json", "r") as file:
            tile_dict = json.load(file)
    except Exception:
        tile_dict = None

    if tile_dict is None:
        tile_dict = {}

    creator = data.get('creator')
    name = data.get('name')
    tile = data.get('tile')

    if creator is None:
        return "missing creator", 404
    if name is None:
        return "missing name", 404
    if tile is None:
        return "missing tile", 404

    if len(tile) != 16:
        return "wrong height", 404
    if len(tile[0]) != 16:
        return "wrong width", 404

    for i in range(15):
        for j in range(15):
            if len(tile[i][j]) != 3:
                return "wrong number of colors", 404

    tile_dict[creator + "." + name] = tile

    with open("tiles.json", "w+") as file:
        json.dump(tile_dict, file)

    return "OK", 200


@app.route('/jinja')
def jinja():
    tile_dict = json.loads(get_tiles())
    return render_template('jinja.html', tiles=tile_dict)

@app.route('/draw')
def draw():
    tile_dict = json.loads(get_tiles())
    return render_template('draw.html', tiles=tile_dict)

@app.route('/color')
def color():
    return render_template('color.html')

serve(app, host="0.0.0.0", port=8080)
