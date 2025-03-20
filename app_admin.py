import sys 
import mysql.connector 
import mysql.connector.errorcode as errorcode
import app_client
import app

class Admin:
    def __init__(self, client, conn):
        self.client = client
        self.conn = conn

    def show_admin_options(self):
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
                app.quit_ui()
            case 'j':
                print('j pressed')
                app.quit_ui()
            case 'm':
                print('m pressed')
                app.quit_ui()
            case 'h':
                print('h pressed')
                app.quit_ui()
            case 'c':
                print('c pressed')
                app.show_options()
            case _:
                print('Other key pressed')
                self.show_admin_options(self)


    def login(self):
        """
        Attempts a login by checking the user_info table.
        Sends you to a login screen that lets you input
        an admin user and password, letting you retry password input
        or sending you back to client screen if desired.
        """
        cursor = self.conn.cursor()
        user = input('Username: ')
        pwd = input('Password: ')
        sql = 'CALL authenticate(\'%s\', \'%s\');' % (user, pwd)
        try:
            cursor.execute(sql)
            result = cursor.fetchall()
            if result:
                self.show_admin_options()
            else:
                print('Login failed.')
                while True:
                    quit = input('Quit to client? [Y/N]').lower()
                    if quit == 'y':
                        self.client.show_options()
                        break
                    elif quit == 'n':
                        self.login_attempt()
                        break
        except mysql.connector.Error as err:
            if app.DEBUG:
                sys.stderr(err)
                sys.exit(1)
            else:
                sys.stderr('An error occured, try again later')

    def manage_jobs(self):
        """
        Sends you to a manage screen that lets you edit the jobs table.
        """
        return

    def manage_mortgages(self):
        """
        Sends you to a manage screen that lets you edit the mortgages table.
        """
        return

    def manage_prices(self):
        """
        Sends you to a manage screen that lets you edit the prices in 
        the locations table.
        """
        return

    def add_job(self):
        """
        Adds a new job listing to the database using terminal inputs
        """
        return

    def edit_job(self, job_id):
        """
        Edits an existing job listing by job_id

        Parameters:
        job_id (int): the job_id of the listing
        """
        return

    def delete_job(self, job_id):
        """
        Deletes a job listing by job_id

        Parameters:
        job_id (int): the job_id of the listing
        """
        return