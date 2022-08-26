import base64
import json
from flask import Flask,request
import sqlite3;

app = Flask(__name__)

@app.route('/verify', methods=['POST'])
def verify():
    if request.method == "POST":
        req_data = request.get_json()
        filename = "paastocht_map_data.mbtiles"
        db = sqlite3.connect(filename)
        c = db.cursor()
        sql = "SELECT * FROM secret"
        c.execute(sql)
        myresult = c.fetchall()
        print(myresult)
        if req_data['password']==myresult[0][0]:
            return json.dumps(1)
        else:
            return json.dumps(0)


@app.route('/tiles', methods=['GET'])
def getTiles():
    if request.method == "GET":
        filename = "paastocht_map_data.mbtiles"
        db = sqlite3.connect(filename)
        c = db.cursor()
        sql = "SELECT * FROM tiles"
        c.execute(sql)
        myresult = c.fetchall()

        # ##CREATE ONE LARGE STRING
        tiles_string = ""
        for tile_row in myresult:
            tiles_string+="sAndErnEstrow"
            for value in tile_row:
                try:
                    tiles_string+="sAndErnEstcol" + base64.b64encode(value).decode('utf-8')
                except:
                    tiles_string+="sAndErnEstcol" + str(value)

        c.close()
        db.close()
        return json.dumps(tiles_string)
        
@app.route('/metadata', methods=['GET'])
def getMetadata():
    if request.method == "GET":
        filename = "paastocht_map_data.mbtiles"
        db = sqlite3.connect(filename)
        c = db.cursor()
        sql = "SELECT * FROM metadata"
        c.execute(sql)
        myresult = c.fetchall()

        # ##CREATE ONE LARGE STRING
        metadata_string = ""
        for metadata_row in myresult:
            metadata_string+="sAndErnEstrow"
            for value in metadata_row:
                try:
                    metadata_string+="sAndErnEstcol" + str(value)
                except:
                    pass

        c.close()
        db.close()
        return json.dumps(metadata_string)


@app.route('/route/info', methods=['GET'])
def getRouteInfo():
    if request.method == "GET":
        filename = "paastocht_map_data.mbtiles"
        db = sqlite3.connect(filename)
        c = db.cursor()
        sql = "SELECT * FROM route_info"
        c.execute(sql)
        myresult = c.fetchall()

        # ##CREATE ONE LARGE STRING
        route_info_string = ""
        for route_info_row in myresult:
            route_info_string+="sAndErnEstrow"
            for value in route_info_row:
                try:
                    route_info_string+="sAndErnEstcol" + str(value)
                except:
                    pass

        c.close()
        db.close()
        return json.dumps(route_info_string)

@app.route('/route/coordinates', methods=['GET'])
def getRouteCoordinates():
    if request.method == "GET":
        filename = "paastocht_map_data.mbtiles"
        db = sqlite3.connect(filename)
        c = db.cursor()
        sql = "SELECT * FROM route_coordinates"
        c.execute(sql)
        myresult = c.fetchall()

        # ##CREATE ONE LARGE STRING
        route_coordinates_string = ""
        for route_coordinates_row in myresult:
            route_coordinates_string+="sAndErnEstrow"
            for value in route_coordinates_row:
                try:
                    route_coordinates_string+="sAndErnEstcol" + str(value)
                except:
                    pass

        c.close()
        db.close()
        return json.dumps(route_coordinates_string)

@app.route('/')
def hello_name():
    return "Hello!"

if __name__ == '__main__':
    app.run(host='0.0.0.0')