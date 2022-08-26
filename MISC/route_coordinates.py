import pickle
import mysql.connector;
import sqlite3

# db_mysql = mysql.connector.connect(host="127.0.0.1",user="root",password="laRForeAUshIel",database="paastocht")
# c_mysql = db_mysql.cursor()
# sql = "DELETE FROM route_coordinates"
# c_mysql.execute(sql)
#
# filename = "map_data.mbtiles"
# db_mbtiles = sqlite3.connect(filename)
# c_mbtiles = db_mbtiles.cursor()
# sql = "SELECT * FROM route_coordinates WHERE day = ?"
# day = ("1", )
# c_mbtiles.execute(sql, day)
# myresult = c_mbtiles.fetchall()
#
# coordinates_list = eval(myresult[0][1][2:-1])
# print(eval(myresult[0][1][2:-1]))
#

# filename = "map_data.mbtiles"
# db_mbtiles = sqlite3.connect(filename)
# c_mbtiles = db_mbtiles.cursor()
# sql = "SELECT * FROM route_coordinates"
# c_mbtiles.execute(sql)
# myresult = c_mbtiles.fetchall()
# print(myresult)




routes_data = pickle.load(open("routes_data.pickle","rb"))
# print(len(routes_data))
print(routes_data)

# sql = "INSERT INTO route_coordinates (day,coordinate_string) VALUES (%s,%s)"
# val = ('1',bytes(str(routes_data['dag 1']),'utf-8'))
# c_mysql.execute(sql,val)
# sql = "INSERT INTO route_coordinates (day,coordinate_string) VALUES (%s,%s)"
# val = ('2',bytes(str(routes_data['dag 2']),'utf-8'))
# c_mysql.execute(sql,val)
# sql = "INSERT INTO route_coordinates (day,coordinate_string) VALUES (%s,%s)"
# val = ('3',bytes(str(routes_data['dag 3']),'utf-8'))
# c_mysql.execute(sql,val)
# sql = "INSERT INTO route_coordinates (day,coordinate_string) VALUES (%s,%s)"
# val = ('4-kort',bytes(str(routes_data['dag 4']),'utf-8'))
# c_mysql.execute(sql,val)
# sql = "INSERT INTO route_coordinates (day,coordinate_string) VALUES (%s,%s)"
# val = ('4',bytes(str(routes_data['dag 4']),'utf-8'))
# c_mysql.execute(sql,val)
# sql = "INSERT INTO route_coordinates (day,coordinate_string) VALUES (%s,%s)"
# val = ('5',bytes(str(routes_data['dag 5']),'utf-8'))
# c_mysql.execute(sql,val)
# sql = "INSERT INTO route_coordinates (day,coordinate_string) VALUES (%s,%s)"
# val = ('6',bytes(str(routes_data['dag 6']),'utf-8'))
# c_mysql.execute(sql,val)

# db_mysql.commit()
