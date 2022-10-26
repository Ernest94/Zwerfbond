from flask import Flask,request,g,send_from_directory
import sqlite3
import json

app = Flask(__name__)

PATH = '.'
# FILE = 'map_data_Pt_2022.mbtiles'
FILE = 'map_data_HH_2022.mbtiles'
DATABASE = PATH + "/" + FILE

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

def get_all_data_from_table_for_columnNameIsValue(database,table,column_name,value):
    c_mbtiles = get_db().cursor()
    sql = "SELECT * FROM "+table+" WHERE "+column_name+" = ?"
    sql_day = (value, )
    c_mbtiles.execute(sql, sql_day)
    myresult = c_mbtiles.fetchall()
    c_mbtiles.close()
    return myresult

@app.route('/get_mbtiles', methods=['GET'])
def getMbtiles():
    if request.method == "GET":
        return send_from_directory(PATH, FILE, as_attachment=True)

@app.route('/get_mbtiles_name', methods=['GET'])
def getNameOfMbtilesFile():
    if request.method == "GET":
        return get_all_data_from_table_for_columnNameIsValue(DATABASE,"metadata","name","name")[0][1]

@app.route('/verify', methods=['POST'])
def verify():
    if request.method == "POST":
        req_data = request.get_json()
        if req_data['password']=="ZWeRFBoND":
            return json.dumps(1)
        else:
            return json.dumps(0)

@app.route('/')
def hello_name():
    return "Hello!"

if __name__ == '__main__':
    app.run(host='0.0.0.0')
