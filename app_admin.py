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
                self.manage_jobs()
            case 'm':
                self.manage_mortgages()
            case 'h':
                self.manage_prices()
            case 'c':
                app.show_options(self.client, self.conn)
            case _:
                print('Other key pressed')
                self.show_admin_options()


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
        sql = 'SELECT authenticate(%s, %s);' 
        try:
            cursor.execute(sql, (user, pwd))
            result = cursor.fetchone()[0]

            if result:
                print('Login successful')
                self.show_admin_options()
            else:
                print('Login failed.')
                while True:
                    quit = input('Quit to client? [Y/N]').lower()
                    if quit == 'y':
                        self.client.show_options()
                        return
                    elif quit == 'n':
                        self.login()
                        return
                    else:
                        print('Invalid input. Please enter Y or N.')
        except mysql.connector.Error as err:
            sys.stderr.write('Login error: ' + str(err) + '\n')

    def manage_jobs(self):
        """
        Sends you to a manage screen that lets you edit the jobs table.
        """
        print('Managing job listings...')
        print('  (a) - (A)dd a job listing')
        print('  (e) - (E)dit a job listing')
        print('  (d) - (D)elete a job listing')
        print('  (b) - (B)ack to Admin Menu')
        print()
        ans = input('Enter an option: ').lower()

        match ans:
            case 'a':
                self.add_job()
            case 'e':
                job_id = input("Enter Job ID to edit: ")
                self.edit_job(job_id)
            case 'd':
                job_id = input("Enter Job ID to delete: ")
                self.delete_job(job_id)
            case 'b':
                self.show_admin_options()
            case _:
                print('Invalid option. Try again.')
                self.manage_jobs()

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
        cursor = self.conn.cursor()
        company_id = input('Enter company ID: ')
        job_title = input('Enter job title: ')
        job_description = input('Enter job description: (can be NULL)')
        loc_city = input('Enter job location (city): ')
        loc_state = input('Enter job location (state): ')
        min_salary = input('Enter minimum salary: ')
        max_salary = input('Enter maximum salary: ')
        avg_salary = input('Enter average salary: ')
        is_hourly = input('Is this an hourly paid job? (1 for Yes, 0 for No): ')

        sql = '''
        INSERT INTO jobs (company_id, job_title, job_description, loc_city, 
                    loc_state, min_salary, max_salary, avg_salary, is_hourly)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
        '''

        try:
            cursor.execute(sql, (company_id, job_title, job_description, loc_city, 
                                 loc_state, min_salary, max_salary, avg_salary, is_hourly))
            self.conn.commit()
            print('Job added successfully.')
        except mysql.connector.Error as err:
            sys.stderr.write('Error adding job: ' + str(err) + '\n')
        

    def edit_job(self, job_id):
        """
        Edits an existing job listing by job_id
        """
        cursor = self.conn.cursor()
        print("\nLeave fields blank to keep them unchanged.")

        job_title = input("Enter new Job Title: ")
        job_desc = input("Enter new Job Description: ")
        min_salary = input("Enter new Minimum Salary: ")
        max_salary = input("Enter new Maximum Salary: ")
        avg_salary = input("Enter new Average Salary: ")
        is_hourly = input("Is this an hourly job? (1 for Yes, 0 for No): ")
        
        update_attributes = []
        values = []

        if job_title:
            update_attributes.append("job_title = %s")
            values.append(job_title)
        if job_desc:
            update_attributes.append("job_description = %s")
            values.append(job_desc)
        if min_salary:
            update_attributes.append("min_salary = %s")
            values.append(min_salary)
        if max_salary:
            update_attributes.append("max_salary = %s")
            values.append(max_salary)
        if avg_salary:
            update_attributes.append("avg_salary = %s")
            values.append(avg_salary)
        if is_hourly:
            update_attributes.append("is_hourly = %s")
            values.append(is_hourly)

        if not update_attributes:
            print('No changes made')
            return

        to_update = ', '.join(update_attributes)
        sql = f'UPDATE jobs SET {to_update} WHERE job_id = %s'
        values.append(job_id)

        try:
            cursor.execute(sql, tuple(values))
            self.conn.commit()
            print('Job updated successfully!')
        except mysql.connector.Error as err:
            sys.stderr.write('Error updating job: ' + str(err) + '\n')


    def delete_job(self, job_id):
        """
        Deletes a job listing by job_id
        """
        cursor = self.conn.cursor()
        sql = "DELETE FROM jobs WHERE job_id = %s"

        try:
            cursor.execute(sql, (job_id,))
            self.conn.commit()
            print("Job deleted successfully!")
        except mysql.connector.Error as err:
            sys.stderr.write("Error deleting job: " + str(err) + '\n')