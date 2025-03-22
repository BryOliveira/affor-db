import sys 
import mysql.connector 
import mysql.connector.errorcode as errorcode
import app
from validation import *

class Admin:
    VALID_JOB_FIELDS = [
        'job_title',
        'job_description',
        'loc_city',
        'loc_state',
        'min_salary',
        'max_salary',
        'avg_salary',
        'is_hourly'
    ]

    def __init__(self, client, connection):
        self.connection = connection
        self.cursor = connection.cursor()
        self.client = client

    def create_admin_account(self):
        """
        Create a new admin account 
        """
        print("\n=== Create New Admin Account ===")
        
        try:
            new_username: str = get_str("Enter new admin username")
            new_password: str = get_str("Enter new admin password")
            
            confirm = get_yes_no(f"Confirm creating new admin user '{new_username}'? (y/n)")
            if not confirm:
                print("Cancelled creating new admin.")
                return
            
            self.cursor.callproc('sp_add_user', (new_username, new_password))
            self.connection.commit()

            print(f"Admin account '{new_username}' created successfully.")
        
        except ValueError:
            print("Failed to create new admin account"
                  +"\nAre you sure you entered")

    def login(self):
        """
        Prompts the user for a username and password, and attempts to authenticate
        them against the database.
        """
        print("\n=== Admin Login ===")
        username = input("Enter Username: ").strip()
        password = input("Enter Password: ").strip()

        if not username or not password:
            print("Username and password cannot be empty")
            return

        try:
            self.cursor.execute("SELECT authenticate(%s, %s)",
                                (username, password))
            result = self.cursor.fetchone()

            if result and result[0]:
                print(f"Login successful as {username}.")
                self.show_admin_menu()
            else:
                print("Invalid username or password.")
        except mysql.connector.Error as err:
            print(f"Database error: {err}")

    def show_admin_menu(self):
        """
        Displays the admin menu and handles user input for various admin tasks.
        """
        while True:
            print("\n=== Admin Menu ===")
            print("  (j) Manage Job Listings")
            print("  (m) Update Mortgage Rates")
            print("  (h) Update Housing Prices")
            print("  (c) Create New Admin Account")
            print("  (t) Test Client Mode")
            print("  (q) Quit Admin Menu")

            choice = input("Choose an option: ").lower()

            if choice == 'j':
                self.manage_job_listings()
            elif choice == 'm':
                self.update_mortgage_rates()
            elif choice == 'h':
                self.update_housing_prices()
            elif choice == 'c':
                self.create_admin_account()
            elif choice == 't':
                self.test_client_mode()
            elif choice == 'q':
                print("Leaving Admin Menu.")
                break
            else:
                print("Invalid selection. Try again.")


    def manage_job_listings(self):
        """
        Displays the job listings management menu and handles user input for
        adding, editing, or deleting job listings.
        """
        while True:
            print("\n--- Manage Job Listings ---")
            print("  (a) Add Job")
            print("  (e) Edit Job")
            print("  (d) Delete Job")
            print("  (b) Back to Admin Menu")

            choice = input("Choose an option: ").lower()

            if choice == 'a':
                self.add_job()
            elif choice == 'e':
                self.edit_job()
            elif choice == 'd':
                self.delete_job()
            elif choice == 'b':
                break
            else:
                print("Invalid selection. Try again.")

    def add_job(self):
        print("\n=== Add New Job ===")
        try:
            company_id = get_int("Company ID")

            job_title = get_str("Job Title")
            job_description = get_str("Job Description", nullable=True)

            loc_city = get_str("City", nullable=True)
            loc_state = get_state("State (2-letter abbreviation)")

            print("\nEnter salary in thousands for annual or dollars for hourly (e.g. 50 for 50k or 25 for $25/hour)\n")

            min_salary = get_positive_float("Minimum Salary")
            max_salary = get_positive_float("Maximum Salary")

            if min_salary > max_salary:
                print("Minimum salary cannot be greater than maximum salary.")
                return

            avg_salary_input = input("Average Salary (or leave blank): ").strip()

            if avg_salary_input == "":
                avg_salary = None
            else:
                avg_salary = validate_positive_float(avg_salary_input)
                if not min_salary <= avg_salary <= max_salary:
                    print("Average salary must be between minimum and maximum salary.")
                    return

            is_hourly = get_yes_no("Is the job hourly? (y/n)")

            self.cursor.callproc('add_job_listing', [
                company_id, job_title, job_description, loc_city, loc_state,
                min_salary, max_salary, avg_salary, is_hourly
            ])
            self.connection.commit()

            print(f"Job added successfully under company ID: {company_id}")

        except Exception as err:
            print(f"Error: {err}")


    def edit_job(self):
        print("\n=== Edit Job ===")
        try:
            job_id = get_int("Enter Job ID to edit")

            self.cursor.execute("SELECT * FROM jobs WHERE job_id = %s", (job_id,))
            job = self.cursor.fetchone()

            if not job:
                print("Job not found.")
                return

            print(f"\nEditable fields: {', '.join([field for field in self.VALID_JOB_FIELDS if field != 'avg_salary'])}")
            column = input("Field to edit: ").strip()

            if column == 'avg_salary':
                print("You cannot manually edit avg_salary.")
                return

            if column not in self.VALID_JOB_FIELDS:
                print("Invalid field name.")
                return

            new_value_input = input(f"Enter new value for {column}: ").strip()

            if column in ['min_salary', 'max_salary']:
                new_value = validate_positive_float(new_value_input)
            elif column == 'is_hourly':
                if new_value_input.lower() not in ['y', 'n']:
                    print("Invalid input. Enter 'y' or 'n'.")
                    return
                new_value = 1 if new_value_input.lower() == 'y' else 0
            else:
                new_value = new_value_input or None  # Allow nullable for text fields

            if column == 'min_salary':
                existing_max = job[self.VALID_JOB_FIELDS.index('max_salary') + 2]  # offset +2 for correct tuple index
                if new_value > existing_max:
                    print(f"min_salary cannot be greater than existing max_salary ({existing_max}).")
                    return
            if column == 'max_salary':
                existing_min = job[self.VALID_JOB_FIELDS.index('min_salary') + 2]
                if new_value < existing_min:
                    print(f"max_salary cannot be less than existing min_salary ({existing_min}).")
                    return

            confirm = get_yes_no(f"\nConfirm update of {column} to '{new_value}'? (y/n)")
            if not confirm:
                print("Update cancelled.")
                return

            sql = f"UPDATE jobs SET {column} = %s WHERE job_id = %s"
            self.cursor.execute(sql, (new_value, job_id))
            self.connection.commit()

            if self.cursor.rowcount > 0:
                print(f"Job ID {job_id} updated: {column} set to '{new_value}'")
            else:
                print("No changes made.")

        except Exception as err:
            print(f"Error: {err}")


    def delete_job(self):
        """
        Prompts the user for a job ID and deletes the corresponding job listing
        from the database.
        """
        print("\n=== Delete Job ===")
        try:
            job_id = get_int("Enter Job ID to delete")

            qry = "SELECT * FROM jobs WHERE job_id = %s"
            self.cursor.execute(qry, (job_id,))
            job = self.cursor.fetchone()
            if not job:
                print("Job not found.")
                return
            print("Job Details:")
            print(f"  Job ID: {job[0]}")
            print(f"  Job Title: {job[2]}")
            print(f"  Company ID: {job[1]}")
            print(f"  Description: {job[3]}")
            
            confirm = get_yes_no(f"Confirm deletion of job {job_id}? (y/n)")

            sql = "DELETE FROM jobs WHERE job_id = %s"
            self.cursor.execute(sql, (job_id,))
            self.connection.commit()

            print("Job deleted successfully.")
        except Exception as err:
            print(f"Error: {err}")

    def update_mortgage_rates(self):
        print("\n=== Update Mortgage Rates ===")
        try:
            loc_state = get_state("Enter state abbreviation (2-letter)")
            loan_term_years = get_choice("Enter loan term (10, 15, 30)", [10, 15, 30])
            date_recorded = get_str("Enter date recorded (YYYY-MM-DD)")
            annual_interest_rate = get_float_in_range("Annual interest rate %", 0, 100)

            sql = """
                INSERT INTO mortgage_rates (loc_state, loan_term_years, date_recorded, annual_interest_rate)
                VALUES (%s, %s, %s, %s)
            """
            self.cursor.execute(sql, (loc_state, loan_term_years, date_recorded, annual_interest_rate))
            self.connection.commit()
            print("Mortgage rate updated successfully.")
        except Exception as err:
            print(f"Error: {err}")

    def update_housing_prices(self):
        print("\n=== Update Housing Prices ===")
        try:
            loc_state = get_state("Enter state abbreviation (2-letter)")
            median_house_price = get_positive_float("Enter new median house price")

            sql = """
                UPDATE home_prices
                SET median_house_price = %s
                WHERE loc_state = %s
            """
            self.cursor.execute(sql, (median_house_price, loc_state))
            self.connection.commit()
            print("Housing price updated successfully.")
        except Exception as err:
            print(f"Error: {err}")

    def test_client_mode(self):
        print("\n=== Test Client Mode ===")
        self.client.search_jobs(True)
