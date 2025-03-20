import sys 
import mysql.connector 
import mysql.connector.errorcode as errorcode
import app

class Client:

    def __init__(self, conn):
        self.conn = conn

    def search_query(self, loc):
        split = loc.split(', ')
        if len(split) != 2:
            print('ERROR: Make sure to have the format city, st\n')
            return False
        
        city, state = split
        cursor = self.conn.cursor()

        sql = 'SELECT * FROM jobs WHERE loc_city = %s AND loc_state = %s ;'

        try:
            cursor.execute(sql, (city, state))
            rows = ' '.join(map(str, cursor.fetchall()))
            rows = rows.split('\\r\\n')
            for row in rows:
                print(str(row))
            return True
        except mysql.connector.Error as err:
            sys.stderr.write('Database error occurred: ' + str(err) + '\n')
            return False
    
    def search(self, conn):
        '''
        Sends you to a search screen that lets you filter 
        job listings by location.
        '''
        while True:
            ans = input('Enter any City, ST: ')
            if self.search_query(ans):
                print('Search Finished.')
                break
        app.show_options(self, conn)