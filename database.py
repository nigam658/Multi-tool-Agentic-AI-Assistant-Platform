import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()


def get_mysql():

    return mysql.connector.connect(
        host="localhost",
        user="root",
        password=os.getenv("MYSQLPASSWORD"),
        database="reminder_tool"
    )