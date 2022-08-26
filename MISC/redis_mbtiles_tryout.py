import sqlite3;
import redis

#initialize Redis dB
r = redis.Redis()

#import mbtiles
filename = "paastocht2020.mbtiles"
db = sqlite3.connect(filename)
c = db.cursor()

#PRINT ALL TILES FROM MBTILES FILE
results = c.execute("SELECT * FROM tiles;")
all_tiles = results.fetchall() ##creates a list with tuples 0:zoom_level 1:tile_column 2:tile_row 3:tile_data
# print(all_tiles[0])
#
##CREATE ONE LARGE STRING
tiles_string = ""
for tile in all_tiles:
    tiles_string+="sAndErnEst"+str(tile)

##store string in Redis
r.mset({"paastocht2020": tiles_string})
# print(r.get("Bahamas").decode("utf-8"))
# print(r)
