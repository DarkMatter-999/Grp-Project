import sqlite3
from os.path import exists


def doesnt_exist():
    #Connecting to sqlite
    conn = sqlite3.connect('database.db')

    #Creating a cursor object using the cursor() method
    cursor = conn.cursor()

    sql='''CREATE TABLE IF NOT EXISTS USERS (
        UID TEXT PRIMARY KEY,
        USERNAME TEXT,
        PHNO TEXT,
        PASSWD TEXT,
        UEMAIL TEXT
    ) 
    '''
    cursor.execute(sql)
    sql ='''CREATE TABLE IF NOT EXISTS DATA (
        DID TEXT PRIMARY KEY,
        UID TEXT,
        IMG TEXT,
        TITLE TEXT,
        CONTENT TEXT,
        TIME TIMESTAMP,
        FOREIGN KEY (UID)
        REFERENCES USERS(UID)
    )'''
    cursor.execute(sql)
    SQL ='''CREATE TABLE IF NOT EXISTS CITIES (
        CITY TEXT,
        ADDRESS TEXT,
        TYPE TEXT,
        REFERENCES DATA(DID)

    )'''

    print("Table created successfully........")

    


    # Commit your changes in the database
    conn.commit()

    #Closing the connection
    conn.close()

 #Inserting values function
def insdata(DID,UID,IMG,TITLE,CONTENT,TIMESTAMP):
        sql=f'''INSERT INTO DATA VALUES({DID},{UID},{IMG},{TITLE},{CONTENT},{TIMESTAMP})'''
        cursor.execute(sql)
def inscities(CITY,ADDRESS,TYPE):
        sql=f'''INSERT INTO CITIES VALUES({CITY},{ADDRESS},{TYPE})'''
        cursor.execute(sql)

if not exists("database.db"):
    doesnt_exist()
