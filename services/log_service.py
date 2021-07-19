import config
import mysql.connector
from mysql.connector import Error
from views.admin.usermanagement.user_data import *
import time
import datetime

########################################### ABOUT CONECTION ########################################### 


def mysqlconnect():
    try:
        return mysql.connector.connect(host=config.db["host"], database=config.db["database"], user=config.db["user"], password=config.db["password"])
        # if connection.is_connected():
        #     db_Info = connection.get_server_info()
        #     print("Connected to MySQL Server version ", db_Info)
        #     cursor = connection.cursor()
        #     cursor.execute("select database();")
        #     record = cursor.fetchone()
        #     print("You're connected to database: ", record)
    except Error as e:
        return e

########################################### ABOUT LOG ###########################################

def getdate():
    try:
        date = datetime.datetime.now()
        day = date.day
        month = date.month
        year = date.year
        hour = date.hour
        minute = date.minute
        second = date.second
        print("datetime : ", date)
        print("day : ", day)
        print("month : ", month)
        print("year : ", year)
        print("hour : ", hour)
        print("minute : ", minute)
        print("second : ", second)
    except Error as e:
        print("Error : ", e)


def getlog():
    try:
        connection = mysqlconnect()

        mySql_select_query = "select * from log"

        cursor = connection.cursor()
        cursor.execute(mySql_select_query)
        # get all records
        records = cursor.fetchall()
        date = records[0][1]
        day = date.day
        print("log ", records[0][1])
        print("day ", day)
        return

    except mysql.connector.Error as e:
        print("Error reading data from MySQL table", e)
    finally:
        if connection.is_connected():
            connection.close()
            cursor.close()
            print("MySQL connection is closed")


def getlogbydate(date):
    try:
        connection = mysqlconnect()
        print("date ", date)
        mySql_select_query = "select * from log WHERE date= %s"

        cursor = connection.cursor()
        cursor.execute(mySql_select_query, (date,))
        # get all records
        records = cursor.fetchall()
        return records

    except mysql.connector.Error as e:
        print("Error reading data from MySQL table", e)
    finally:
        if connection.is_connected():
            connection.close()
            cursor.close()
            print("MySQL connection is closed")

# request[part_no, part_name, drawing_no, quantity, locker, activity]
def insertlog(employee, request, activity):
    try:

        connection = mysqlconnect()
        mySql_insert_query = """INSERT INTO log (id, date, time, employeeid, name, lastname, part_no, part_name, drawing_no, quantity, locker, activity) 
                                VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """

        for x in range(len(request)):
            results = getmedicallocker(medical[x][3])
            lockernumber = results[1]
            for y in range(len(lockernumber)):
                locker = lockernumber[y][2]
                record = (
                datetime.datetime.now().date(), datetime.datetime.now().time(), employee[0], employee[1], employee[2],
                medical[x][1], locker, activity)
                cursor = connection.cursor()
                cursor.execute(mySql_insert_query, record)
                connection.commit()

        return True

    except mysql.connector.Error as e:
        print("Failed to update columns of table: {}".format(e))
        return False
    finally:
        if connection.is_connected():
            connection.close()
            cursor.close()
            print("MySQL connection is closed")
#getlog()
#getdate()