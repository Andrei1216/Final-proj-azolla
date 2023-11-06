# MySQL connection
import mysql.connector

db = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="expressdb"
)

cursor = db.cursor()