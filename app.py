'''
Is just having a helper function for each key press the simplest way
to handle the options or is there a less repetitive way?

Is the cmd interface user-friendly enough? Are the options
ordered in a simple enough manner?
'''

import sys  # to print error messages to sys.stderr
import mysql.connector
# To get error codes from the connector, useful for user-friendly
# error-handling
import mysql.connector.errorcode as errorcode

# Debugging flag to print errors when debugging that shouldn't be visible
# to an actual client. ***Set to False when done testing.***
DEBUG = True


# ----------------------------------------------------------------------
# SQL Utility Functions
# ----------------------------------------------------------------------
def get_conn():
    """"
    Returns a connected MySQL connector instance, if connection is successful.
    If unsuccessful, exits.
    """
    try:
        conn = mysql.connector.connect(
          host='localhost',
          user='appadmin',
          # Find port in MAMP or MySQL Workbench GUI or with
          # SHOW VARIABLES WHERE variable_name LIKE 'port';
          port='3306',  # this may change!
          password='adminpw',
          database='shelterdb' # replace this with your database name
        )
        print('Successfully connected.')
        return conn
    except mysql.connector.Error as err:
        # Remember that this is specific to _database_ users, not
        # application users. So is probably irrelevant to a client in your
        # simulated program. Their user information would be in a users table
        # specific to your database; hence the DEBUG use.
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR and DEBUG:
            sys.stderr('Incorrect username or password when connecting to DB.')
        elif err.errno == errorcode.ER_BAD_DB_ERROR and DEBUG:
            sys.stderr('Database does not exist.')
        elif DEBUG:
            sys.stderr(err)
        else:
            # A fine catchall client-facing message.
            sys.stderr('An error occurred, please contact the administrator.')
        sys.exit(1)

# ----------------------------------------------------------------------
# Functions for Command-Line Options/Query Execution
# ----------------------------------------------------------------------
def example_query():
    param1 = ''
    cursor = conn.cursor()
    # Remember to pass arguments as a tuple like so to prevent SQL
    # injection.
    sql = 'SELECT col1 FROM table WHERE col2 = \'%s\';' % (param1, )
    try:
        cursor.execute(sql)
        # row = cursor.fetchone()
        rows = cursor.fetchall()
        for row in rows:
            (col1val) = (row) # tuple unpacking!
            # do stuff with row data
    except mysql.connector.Error as err:
        # If you're testing, it's helpful to see more details printed.
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr('An error occurred, please try again later')

# ----------------------------------------------------------------------
# Command-Line Functionality
# ----------------------------------------------------------------------
def show_options():
    """
    Displays options users can choose in the application.
    Currently accounting for switching to a search screen,
    an admin login screen, and quitting the app entirely.
    """
    print('What would you like to do? ')
    print('  (s) - (S)earch Job Listings')
    print('  (l) - Admin (L)ogin')
    print('  (q) - quit')
    print()
    ans = input('Enter an option: ').lower()
    match ans:
        case 'q':
            quit_ui()
        case 's':
            print('s pressed')
            quit_ui()
        case 'l':
            print('l pressed')
            show_admin_options()
        case _:
            print('Other key pressed')
            show_options()

def show_admin_options():

    """
    Displays options specific for admins and parses key inputs in this dash.
    Current options include managing job listings, mortgage rates,
    house prices, entering client mode, and quitting the app.
    """
    print('What would you like to do? ')
    print('  (j) - Manage (J)ob listings')
    print('  (m) - Manage (M)ortgage Rates')
    print('  (h) - Manage (H)ouse Prices')
    print('  (c) - Switch to (C)lient Mode')
    print('  (q) - (q)uit')
    print()
    ans = input('Enter an option: ').lower()
    match ans:
        case 'q':
            quit_ui()
        case 'j':
            print('j pressed')
            quit_ui()
        case 'm':
            print('m pressed')
            quit_ui()
        case 'h':
            print('h pressed')
            quit_ui()
        case 'c':
            print('c pressed')
            show_options()
        case _:
            print('Other key pressed')
            show_admin_options()


def search():
    '''
    Sends you to a search screen that lets you filter 
    job listings by location.
    '''
    return

def login():
    '''
    Sends you to a login screen that lets you input
    an admin user and password, sending you back to
    client screen if you fail and showing admin options if passed.
    '''
    return

def manage_jobs():
    '''
    Sends you to a manage screen that lets you edit the jobs table.
    '''
    return

def manage_mortgages():
    '''
    Sends you to a manage screen that lets you edit the mortgages table.
    '''
    return

def manage_prices():
    '''
    Sends you to a manage screen that lets you edit the prices in 
    the locations table.
    '''
    return

def quit_ui():
    """
    Quits the program, printing a good bye message to the user.
    """
    print('Good bye!')
    exit()


def main():
    """
    Main function for starting things up.
    """
    show_options()


if __name__ == '__main__':
    # This conn is a global object that other functions can access.
    # You'll need to use cursor = conn.cursor() each time you are
    # about to execute a query with cursor.execute(<sqlquery>)
    conn = get_conn()
    main()
