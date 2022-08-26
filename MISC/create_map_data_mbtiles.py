import sqlite3;

filename = "map_data.mbtiles"
db = sqlite3.connect(filename)
c = db.cursor()


c.execute("CREATE TABLE `tiles` (`zoom_level` int NOT NULL, `tile_column` int NOT NULL, `tile_row` int NOT NULL, `tile_data` BLOB NOT NULL)")
c.execute("CREATE TABLE `metadata` (`name` string NOT NULL, `value` string NOT NULL)")
c.execute("INSERT INTO `metadata` (name, value) VALUES ('bounds','5.274382,49.994698,5.849791,50.24916'),('maxzoom','16'),('name','xyz-to-mbtiles'),('type','overlay'),('version','1'),('minzoom','12'),('description',''),('format','png')")
db.commit()



# ##PRINT ALL TABLE NAMES SQLITE DATABASE
# results = c.execute("SELECT name FROM sqlite_master WHERE type = 'table' AND name NOT LIKE 'sqlite_%' ORDER BY 1;")
# all_tables = results.fetchall()
# print(all_tables)

# ##PRINT ALL COLUMN NAME OF THE TILES TABLE
# results = c.execute("SELECT name FROM PRAGMA_TABLE_INFO('tiles');")
# collumn_names = results.fetchall()
# print(collumn_names)

# ##PRINT THE NUMBER OF TILES FROM MBTILES FILE
# results = c.execute("SELECT * FROM tiles")
# nr_rows = results.fetchall()
# print(nr_rows)


# ##Strip the long string
# list_tiles_strings = paastocht2020Str.split("sAndErnEst")
# print(list_tiles_strings[-1])
