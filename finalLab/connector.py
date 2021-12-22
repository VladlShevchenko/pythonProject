import mysql.connector
from mysql.connector import Error

config = {
    'user': 'admin',
    'password': 'admin',
    'host': '127.0.0.1',
    'database': 'mydbpy'
}


class DbConnector:
    """Class for establishing connection with database"""

    @staticmethod
    def getConnection():
        """Function which connect app to MySql database"""
        try:
            connection = mysql.connector.connect(**config)
            if connection.is_connected():
                db_Info = connection.get_server_info()
                print("Connected to MySQL Server version ", db_Info)
                cursor = connection.cursor()
                cursor.execute("select database();")
                record = cursor.fetchone()
                print("You're connected to database: ", record)
                return connection

        except Error as e:
            print("Error while connecting to MySQL", e)

