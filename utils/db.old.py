import sqlite3
from os.path import exists
import random
import string

def generate_random(length):
    letters = string.ascii_lowercase + string.ascii_uppercase + string.digits
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

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
    ) '''
    cursor.execute(sql)

    sql ='''CREATE TABLE IF NOT EXISTS CITIES (
        CITY TEXT PRIMARY KEY,
        ADDRESS TEXT,
        TYPE TEXT
    )'''
    cursor.execute(sql)

    sql ='''CREATE TABLE IF NOT EXISTS DATA (
        DID TEXT PRIMARY KEY,
        UID TEXT,
        IMG TEXT,
        TITLE TEXT,
        CONTENT TEXT,
        TIME TIMESTAMP,
        CITY TEXT,
        FOREIGN KEY (CITY) REFERENCES CITIES(CITY),
        FOREIGN KEY (UID) REFERENCES USERS(UID)
    )'''
    cursor.execute(sql)

    print("Table created successfully........")

    conn.commit()
    conn.close()

#Inserting values function
def insuser(conn, USERNAME, PHNO, PASSWD, UEMAIL):
    UID = generate_random(32)
    cursor = conn.cursor()
    sql=f'''INSERT INTO USERS VALUES("{UID}","{USERNAME}","{PHNO}","{PASSWD}","{UEMAIL}")'''
    cursor.execute(sql)
    conn.commit()

def insdata(conn, UID,IMG,TITLE,CONTENT,TIMESTAMP, CITY):
    DID = generate_random(32)
    cursor = conn.cursor()
    sql=f'''INSERT INTO DATA VALUES("{DID}","{UID}","{IMG}","{TITLE}","{CONTENT}","{TIMESTAMP}","{CITY}")'''
    cursor.execute(sql)
    conn.commit()

def inscity(conn, CITY,ADDRESS,TYPE):
    cursor = conn.cursor()
    sql=f'''INSERT INTO CITIES VALUES("{CITY}","{ADDRESS}","{TYPE}")'''
    print(sql)
    cursor.execute(sql)
    conn.commit()

if __name__ == '__main__':
    if not exists("database.db"):
        doesnt_exist()