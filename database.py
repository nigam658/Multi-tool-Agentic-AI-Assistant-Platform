import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()


def get_mysql():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "db"),
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQLPASSWORD"),
        database=os.getenv("MYSQL_DATABASE", "reminder_tool")
    )