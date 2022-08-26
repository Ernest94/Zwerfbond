import base64
import json
from flask import Flask,request,jsonify,g
import sqlite3;

app = Flask(__name__)

DATABASE = 'paastocht_map_data.mbtiles'
##sql = "SELECT COUNT(tile_data) FROM tiles"  row_number_split = np.linspace(0,myresult[0][0],11).astype(int)
# SPLIT_TILES = [0,  911, 1823, 2735, 3647, 4559, 5470, 6382, 7294, 8206, 9118]
SPLIT_TILES = [0,455,911, 1367, 1823, 2279, 2735, 3191, 3647, 4103, 4559, 5014, 5470, 5926, 6382, 6838, 7294, 7750, 8206, 8662, 9118]

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def select_all_from_table_in_db(table):
    c = get_db().cursor()
    sql = "SELECT * FROM "+table
    c.execute(sql)
    myresult = c.fetchall()
    c.close()
    return myresult

def select_rows_from_table_in_db(table,id_start_row,id_end_row):
    c = get_db().cursor()
    sql = "SELECT * FROM "+table+" WHERE rowid>"+id_start_row+" AND rowid<="+id_end_row
    c.execute(sql)
    myresult = c.fetchall()
    c.close()
    return myresult

@app.route('/verify', methods=['POST'])
def verify():
    if request.method == "POST":
        req_data = request.get_json()
        result = select_all_from_table_in_db("secret")
        if req_data['password']==result[0][0]:
            return json.dumps(1)
        else:
            return json.dumps(0)

@app.route('/tiles', methods=['GET'])
def getTiles():
    if request.method == "GET":
        result = select_all_from_table_in_db("tiles")

        ##CREATE ONE LARGE STRING
        tiles_string = ""
        for tile_row in result:
            tiles_string+="sAndErnEstrow"
            for value in tile_row:
                try:
                    tiles_string+="sAndErnEstcol" + base64.b64encode(value).decode('utf-8')
                except:
                    tiles_string+="sAndErnEstcol" + str(value)
        return json.dumps(tiles_string)

@app.route('/metadata', methods=['GET'])
def getMetadata():
    if request.method == "GET":
        result = select_all_from_table_in_db("metadata")
        metadata_string = ""
        for metadata_row in result:
            metadata_string+="sAndErnEstrow"
            for value in metadata_row:
                try:
                    metadata_string+="sAndErnEstcol" + str(value)
                except:
                    pass
        return json.dumps(metadata_string)

@app.route('/route/info', methods=['GET'])
def getRouteInfo():
    if request.method == "GET":
        result = select_all_from_table_in_db("route_info")

        ##CREATE ONE LARGE STRING
        route_info_string = ""
        for route_info_row in result:
            route_info_string+="sAndErnEstrow"
            for value in route_info_row:
                try:
                    route_info_string+="sAndErnEstcol" + str(value)
                except:
                    pass
        return json.dumps(route_info_string)

@app.route('/route/coordinates', methods=['GET'])
def getRouteCoordinates():
    if request.method == "GET":
        result = select_all_from_table_in_db("route_coordinates")

        ##CREATE ONE LARGE STRING
        route_coordinates_string = ""
        for route_coordinates_row in result:
            route_coordinates_string+="sAndErnEstrow"
            for value in route_coordinates_row:
                try:
                    route_coordinates_string+="sAndErnEstcol" + str(value)
                except:
                    pass
        return json.dumps(route_coordinates_string)

@app.route('/tiles/<int:tile_number>', methods=['GET'])
def getTilesNew(tile_number):
    if request.method == "GET":
        result = select_rows_from_table_in_db("tiles",str(SPLIT_TILES[tile_number-1]),str(SPLIT_TILES[tile_number]))
        ##CREATE ONE LARGE STRING
        tiles_string = ""
        for i,tile_row in enumerate(result):
            tiles_string+="sAndErnEstrow"
            for value in tile_row:
                try:
                    tiles_string+="sAndErnEstcol" + base64.b64encode(value).decode('utf-8')
                except:
                    tiles_string+="sAndErnEstcol" + str(value)
        return json.dumps(tiles_string)

@app.route('/')
def hello_name():
    return "Hello!"

if __name__ == '__main__':
    app.run(host='0.0.0.0')
