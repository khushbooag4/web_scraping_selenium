import pandas as pd
import glob
import time
import duckdb

conn = duckdb.connect("webscrapedb.db")
cursor = conn.cursor()
#cursor.execute("DROP TABLE delegate_info")

# cursor.execute('SELECT * FROM delegate_info')
cursor.execute("SELECT * FROM delegate_info")
result = cursor.fetchall()
print(result)
