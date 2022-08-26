import sqlite3;

def get_all_data_from_table_for_columnNameIsValue(database,table,column_name,value):
    db_mbtiles = sqlite3.connect(database)
    c_mbtiles = db_mbtiles.cursor()
    sql = "SELECT * FROM "+table+" WHERE "+column_name+" = ?"
    sql_day = (value, )
    c_mbtiles.execute(sql, sql_day)
    myresult = c_mbtiles.fetchall()
    db_mbtiles.close()
    return myresult
