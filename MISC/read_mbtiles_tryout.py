import sqlite3;
import numpy as np

filename = "paastocht_map_data.mbtiles"
db = sqlite3.connect(filename)
c = db.cursor()




# sql = "SELECT COUNT(tile_data) FROM tiles"
# c.execute(sql)
# myresult = c.fetchall()
# print(myresult[0][0])
# row_number_split = np.linspace(0,myresult[0][0],21).astype(int)
# print(row_number_split)


#[   0 1013 2026 3039 4052 5065 6078 7091 8104 9118]
table = "tiles";
SPLIT_TILES = [0,455,911, 1367, 1823, 2279, 2735, 3191, 3647, 4103, 4559, 5014, 5470, 5926, 6382, 6838, 7294, 7750, 8206, 8662, 9118]


for index,i in enumerate(SPLIT_TILES):
    print(index,i)
    sql = "SELECT * FROM "+table+" WHERE rowid>"+str(SPLIT_TILES[index])+" AND rowid<="+str(SPLIT_TILES[index+1])
    c.execute(sql)
    myresult = c.fetchall()

    print(len(myresult))

c.close()
# print(len(myresult))
#
# sql = "SELECT * FROM tiles"
# c.execute(sql)
# myresult = c.fetchall()
#
# ##CREATE ONE LARGE STRING
# tiles_string = ""
# i=0
# while i < 1013:
#     tiles_string+="sAndErnEstrow"
#     for value in myresult[i]:
#         try:
#             tiles_string+="sAndErnEstcol" + base64.b64encode(value).decode('utf-8')
#         except:
#             tiles_string+="sAndErnEstcol" + str(value)
#     i+=1
# print(tiles_string)


# sql = "SELECT * FROM tiles"
# c.execute(sql)
# myresult = c.fetchall()
#
#
# ##CREATE ONE LARGE STRING
# tiles_string = ""
# for (i,tile_row) in enumerate(myresult):
#     tiles_string+="sAndErnEstrow"
#     print(i)
#     if i>len(myresult)/10:
#         break
#     for value in tile_row:
#         try:
#             tiles_string+="sAndErnEstcol" + base64.b64encode(value).decode('utf-8')
#         except:
#             tiles_string+="sAndErnEstcol" + str(value)
# print(tiles_string)






# c.execute("CREATE TABLE `secret` (`password` string NOT NULL)")
# sql = "INSERT INTO secret (password) VALUES('ZWeRFBoND')"
# # val = str('ZWeRFBoND')
# c.execute(sql)
# db.commit()
# db.close()

# ## PRINT METADATA FROM MBTILES FILE
# metadata = dict(c.execute("SELECT * FROM metadata"))
# print(metadata)


##PRINT ALL TABLE NAMES SQLITE DATABASE
# results = c.execute("SELECT name FROM sqlite_master WHERE type = 'table' AND name NOT LIKE 'sqlite_%' ORDER BY 1;")
# all_tables = results.fetchall()
# print(all_tables)

# ##PRINT THE NUMBER OF TILES FROM MBTILES FILE
# results = c.execute("SELECT count(*) FROM tiles")
# nr_rows = results.fetchall()
# print(nr_rows)

##PRINT ALL COLUMN NAME OF THE TILES TABLE
# results = c.execute("SELECT name FROM PRAGMA_TABLE_INFO('secret');")
# collumn_names = results.fetchall()
# print(collumn_names)

# ##EXPORT MBTILES TO CSV FILE TO UNDERSTAND THE STRUCTURE
# import pandas as pd
# conn = sqlite3.connect(filename, isolation_level=None,
#                        detect_types=sqlite3.PARSE_COLNAMES)
# db_df = pd.read_sql_query("SELECT * FROM tiles", conn)
# db_df.to_csv('database.csv', index=False)


# PRINT ALL TILES FROM MBTILES FILE
# results = c.execute("SELECT * FROM secret;")
# secret = results.fetchall() ##creates a list with tuples 0:zoom_level 1:tile_column 2:tile_row 3:tile_data
# print(secret[0][0])



# ##Strip the long string
# list_tiles_strings = tiles_string.split("sAndErnEst")
# print(len(list_tiles_strings[-1]))
