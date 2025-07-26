import csv
import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Pawan2005@",
    database="chatbot_db"
)

cursor = conn.cursor()

with open('products.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        cursor.execute("""
            INSERT INTO products (product_id, name, category, price, stock)
            VALUES (%s, %s, %s, %s, %s)
        """, (row['product_id'], row['name'], row['category'], row['price'], row['stock']))

conn.commit()
conn.close()