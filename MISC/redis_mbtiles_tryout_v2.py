import redis
import sqlite3;

r = redis.Redis()

paastocht2020Str = r.get("paastocht2020").decode("utf-8")

##Strip the long string
list_tiles_strings = paastocht2020Str.split("sAndErnEst")
print(list_tiles_strings[-1])


# filename = "paastocht2020_readout.mbtiles"
# db = sqlite3.connect(filename)
# c = db.cursor()
