import sqlite3;
import mysql.connector;
import base64

filename = "paastocht2020.mbtiles"
db_mbtiles = sqlite3.connect(filename)
c_mbtiles = db_mbtiles.cursor()

db_mysql = mysql.connector.connect(host="127.0.0.1",user="root",password="laRForeAUshIel",database="paastocht")
c_mysql = db_mysql.cursor()

##PRINT THE NUMBER OF TILES FROM MBTILES FILE
c_mbtiles.execute("SELECT * FROM tiles")
data = c_mbtiles.fetchall()
# print(str(data[0][3],encoding='utf-8',errors='strict'))

while row is not None:
    try:
        row = c_mbtiles.fetchone()
        sql = "INSERT INTO tiles (zoom_level,tile_column,tile_row,tile_data) VALUES (%s,%s,%s,%s)"
        val = (row[0],row[1],row[2],row[3])
        c_mysql.execute(sql,val)
        # break
    except:
        db_mysql.commit()

# print(all_tiles[-1])

# list_tile_len = [];
# for tile in all_tiles:
#     # print(len(tile[3]));
#     list_tile_len.append(len(tile[3]))
#
# print(max(list_tile_len))

# ##PRINT ALL COLUMN NAME OF THE TILES TABLE
# results = c.execute("SELECT name FROM PRAGMA_TABLE_INFO('tiles');")
# collumn_names = results.fetchall()
# print(collumn_names)
#


#
# print(c_mbtiles.rowcount, "record inserted.")




#
# ##PRINT ALL COLUMN NAME OF THE TILES TABLE
# results = c.execute("INSERT  FROM PRAGMA_TABLE_INFO('tiles');")
# collumn_names = results.fetchall()
# print(collumn_names)
