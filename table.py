import mysql.connector

conn = mysql.connector.connect(
    host="localhost", 
    user="user",
    password="password",  
    database="dbname"
)

cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE Personne (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nom VARCHAR(50) NOT NULL,
        prenom VARCHAR(50) NOT NULL,
        date_naissance DATE NOT NULL
    )
""")
               
conn.commit()
cursor.close()
conn.close()