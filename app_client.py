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
        city = split[0]
        state = split[1]
        cursor = self.conn.cursor()
        sql = 'SELECT * FROM jobs WHERE loc_city = \'%s\' AND loc_state = \'%s\' ;' % (city, state)
        try:
            cursor.execute(sql)
            rows = ' '.join(map(str, cursor.fetchall()))
            rows = rows.split('\\r\\n')
            for row in rows:
                print(str(row))
            return True
        except mysql.connector.Error as err:
            sys.stderr('frick')
    
    def search(self):
        '''
        Sends you to a search screen that lets you filter 
        job listings by location.
        '''
        print('Where are you searching?:')
        ans = input('Enter any City, ST: ')
        if not self.search_query(ans):
            ans = input('Enter any City, ST: ')
            self.search_query(ans)
        else:
            print('Search Finished.')
            app.show_options(self)