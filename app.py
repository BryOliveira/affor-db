import sys
import mysql.connector
import mysql.connector.errorcode as errorcode
import app_admin
import app_client
from mysql.connector.constants import ClientFlag

import os
from dotenv import load_dotenv
load_dotenv()

# Constants
# change within .env for mysql users
DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')
DB_PORT = os.getenv('DB_PORT')

DEBUG = False

def get_conn():
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            port=DB_PORT,
            password=DB_PASSWORD,
            database=DB_NAME,
            client_flags=[ClientFlag.LOCAL_FILES]
        )
        print('Successfully connected.')
        return conn
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR and DEBUG:
            sys.stderr('Incorrect username or password when connecting to DB.')
        elif err.errno == errorcode.ER_BAD_DB_ERROR and DEBUG:
            sys.stderr('Database does not exist.')
        elif DEBUG:
            sys.stderr(err)
        else:
            sys.stderr('An error occurred, please contact the administrator.')
        sys.exit(1)

def show_options(client, conn):
    print("What would you like to do?")
    print("  (s) - Search Job Listings")
    print("  (t) - View Top Annual Salary by State")
    print("  (c) - View Top Annual Salary by Sector")
    print("  (l) - Admin Login")
    print("  (q) - Quit")
    print()

    ans = input("Enter an option: ").lower()
    match ans:
        case 'q':
            quit_ui()
        case 's':
            client.search(conn)
        case 't':
            client.view_top_annual_salary_per_state()
            show_options(client, conn)
        case 'c':
            client.view_top_annual_salary_per_sector()
            show_options(client, conn)
        case 'l':
            admin = app_admin.Admin(client, conn)
            admin.login()
        case _:
            print("Invalid option, please try again.")
            show_options(client, conn)

def quit_ui():
    print('Good bye!')
    sys.exit()

def main():
    global conn
    global client
    conn = get_conn()
    client = app_client.Client(conn)
    show_options(client, conn)

if __name__ == '__main__':
    main()