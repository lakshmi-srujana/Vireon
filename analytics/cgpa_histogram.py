import mysql.connector
import matplotlib.pyplot as plt


# ---------- DATABASE CONNECTION ---------- #

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="vireon"
)

cursor = connection.cursor()


# ---------- FETCH CGPA DATA ---------- #

query = "SELECT cgpa FROM students"

cursor.execute(query)

data = cursor.fetchall()


# ---------- CONVERT TUPLES TO LIST ---------- #

cgpas = []

for row in data:
    cgpas.append(float(row[0]))


# ---------- HISTOGRAM ---------- #

plt.figure(figsize=(8, 5))

plt.hist(cgpas, bins=5)

plt.title("CGPA Distribution")

plt.xlabel("CGPA")

plt.ylabel("Number of Students")

plt.grid(True)

plt.show()


# ---------- CLOSE CONNECTION ---------- #

cursor.close()

connection.close()