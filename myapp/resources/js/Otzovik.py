import mysql.connector
from mysql.connector import connection

host="94.103.95.118"
dbuser="remote"
password="Voennii2017!"
dbname="app"

def create_connection(host_name,user_name,user_password,db_name):
    connection=None
    try:
        connection=mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        mycursor = connection.cursor()
        mycursor.execute("SELECT * FROM accounts")

        myresult = mycursor.fetchall()

        for x in myresult:
            print(x)
        print("Database connected")
    except:
        print("Database Error")
    return connection

connection=create_connection(host,dbuser,password,dbname)