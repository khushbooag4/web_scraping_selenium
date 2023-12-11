import duckdb
import json

#CONNECT TO DATABASE
conn = duckdb.connect("webscrape.db")
cursor = conn.cursor()#
cursor.execute("describe TABLE delegate_info")
resu= cursor.fetchall()

#SHOW CONTENT OF DELEGATE_INFO TABLE
cursor.execute("SELECT * FROM delegate_info")
result = cursor.fetchall()

#CONVERT INTO JSON
columns = [desc[0] for desc in cursor.description]
data = [dict(zip(columns, row)) for row in result]
json_data = json.dumps(data, indent=2)
print(json_data)

#EXPORT TO CSV
csv_file_path = 'output1.csv'
cursor.execute("COPY (SELECT * FROM delegate_info) TO '{}' WITH HEADER".format(csv_file_path))
