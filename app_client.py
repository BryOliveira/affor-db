import sys
import mysql.connector
import mysql.connector.errorcode as errorcode
import app
from validation import *


class Client:
    def __init__(self, conn):
        self.conn = conn

    def search_jobs(self, admin=False):
        """
        Prompts the user to search for jobs based on job title, city, state,
        minimum salary, and maximum salary. Displays the results.
        """
        cursor = self.conn.cursor()

        while True:
            job_title = get_str('Enter a job title (or leave blank)', nullable=True) 
            state_input = get_state('Enter a state (or leave blank)', nullable=True) 
            city_input = get_str('Enter a city (or leave blank)', nullable=True)

            min_salary_input = get_positive_float('Enter a minimum salary (or leave blank)', nullable=True)
            max_salary_input = get_positive_float('Enter a maximum salary (or leave blank)', nullable=True)
            
            n_res = get_int("Enter the number of results to display (default 10)", default=10)

            if min_salary_input is not None and max_salary_input is not None:
                if min_salary_input > max_salary_input:
                    print(" Minimum salary cannot be greater than maximum salary.")
                    continue
                
            conditions = []
            parameters = []

            if job_title and job_title.strip():
                conditions.append("job_title LIKE %s")
                parameters.append(f"%{job_title}%")
            if city_input and city_input.strip():
                conditions.append("LOWER(loc_city) LIKE %s")
                parameters.append(f"%{city_input.lower()}%")
            if state_input and state_input.strip():
                conditions.append("loc_state = %s")
                parameters.append(state_input.upper()) 
            if min_salary_input is not None:
                conditions.append("min_salary >= %s")
                parameters.append(min_salary_input)
            if max_salary_input is not None:
                conditions.append("max_salary <= %s")
                parameters.append(max_salary_input)

            if not conditions:
                print("\nNo search criteria provided.")
                if admin:
                    print("Returning to Admin options.")
                return
           
            where_clause = " WHERE " + " AND ".join(conditions)
 
            # would you like to sort by salary?
            sortsalary = get_yes_no("Would you like to sort by max salary? (y/n)")
            sort_order = " ORDER BY avg_salary DESC" if sortsalary else ""

            sql = (
                "SELECT job_id, job_title, company_name, loc_city, loc_state, "
                "min_salary, max_salary, avg_salary "
                "FROM v_jobs_with_annual_salary"
                + where_clause
                + sort_order
                + " LIMIT " + str(n_res) + ";"
            )

            try:
                cursor.execute(sql, tuple(parameters))
                rows = cursor.fetchall()
                if rows:
                    print(f"\nFound {len(rows)} job(s) matching your criteria\n")
                    
                    for row in rows:
                        job_id, title, company_name, city, state, min_sal, max_sal, ann_sal = row
                        print("=" * 80)
                        print(f"Job ID           : {job_id}")
                        print(f"Title            : {title}")
                        print(f"Company          : {company_name}")
                        print(f"Location         : {city}, {state}")
                        print(f"Min Salary       : {int(min_sal)}K")
                        print(f"Max Salary       : {int(max_sal)}K")
                        print(f"Avg Salary       : {int(ann_sal)}K")
                        print("=" * 80)

                    while True:
                        prmp = "\nOptions: [S]earch again, [L]ook up Job ID, [Q]uit"
                        if admin:
                            prmp += ", return to [A]dmin"
                        action = get_str(prmp).lower()

                        if action == 's':
                            break  
                        elif action == 'l':
                            job_id_selected = get_int("Enter the Job ID to view full description")
                            job_ids = [row[0] for row in rows]
                            if job_id_selected in job_ids:
                                self.show_job_description(cursor, job_id_selected)
                            else:
                                print("Invalid Job ID.")
                        elif action == 'q' or action == 'a':
                            if admin:
                                print("Returning to Admin options.")
                            return
                        else:
                            print("Invalid option. Please choose [S], [L], or [Q].")
                else:
                    print("No matching jobs found.")

            except mysql.connector.Error as err:
                sys.stderr.write('Database error occurred: ' + str(err) + '\n')
                break

    def show_job_description(self, cursor, job_id):
        """
        Given a job ID, displays the full job description and
        calculates home affordability.
        """
        try:
            sql = """
            SELECT j.job_id, j.job_title, c.company_name, j.loc_city, j.loc_state, 
                   j.min_salary, j.max_salary, j.avg_salary, j.is_hourly, j.job_description
            FROM jobs j
            JOIN companies c ON j.company_id = c.company_id
            WHERE j.job_id = %s
            """
            cursor.execute(sql, (job_id,))
            job = cursor.fetchone()

            if job:
                job_id, job_title, company_name, city, state, min_salary, max_salary, avg_salary, is_hourly, description = job
                pay_type = "Hourly" if is_hourly else "Annual"

                print("\n" + "=" * 80)
                print(f"Job ID      : {job_id}")
                print(f"Title       : {job_title}")
                print(f"Company     : {company_name}")
                print(f"Location    : {city}, {state}")
                print(f"Pay Type    : {pay_type}")
                
                if is_hourly:
                    print(f"Pay Range   : {min_salary} to {max_salary} /hr")
                else:
                    print(f"Pay Range   : {int(min_salary)}K to {int(max_salary)}K /year")
                
                print("=" * 80)
                print("Job Description:\n")
                print(description)
                print("=" * 80)

                calculate_affordability = get_yes_no(
                    "Would you like to check home affordability based on this job's average salary? (y/n)")
                    
                if calculate_affordability:
                    loc_state = state
                    if loc_state:
                        loc_state = loc_state.strip()
                    else:
                        print("No state information available.")
                        return
                    if avg_salary is not None:
                        avg_salary = float(avg_salary)
                    if avg_salary is not None and loc_state:
                        self.check_home_affordability(cursor, avg_salary, loc_state)
                        
                        
                    
            else:
                print("Job not found.")
        except mysql.connector.Error as err:
            sys.stderr.write('Database error occurred: ' + str(err) + '\n')

    def check_home_affordability(self, cursor, avg_salary, loc_state):
        """
        Checks home affordability based on user input.
        """
        try:
            cursor.execute("SELECT median_house_price FROM home_prices WHERE loc_state = %s", (loc_state,))
            house_price_result = cursor.fetchone()
            if not house_price_result:
                print(f"No house price data found for {loc_state}.")
                return
            house_price = house_price_result[0]

            print(f"\nMedian House Price in {loc_state}: ${house_price:,.2f}")

            down_payment_percent = get_float_in_range("Enter down payment percent (default 20)", 0, 100, default=20)

            down_payment = float(house_price) * (down_payment_percent / 100)
            print(f"\n-->Down Payment: ${down_payment:,.2f}\n")

            loan_term_years = get_choice("Enter loan term in years [10, 15, 30] (default 30): ", [10, 15, 30], default=30)
            loan_term_years = int(loan_term_years)

            cursor.execute("""
                SELECT calc_monthly_mortgage_payment(%s, %s, %s, %s)
            """, (
                house_price,
                down_payment_percent,
                loc_state,
                loan_term_years
            ))

            monthly_payment_result = cursor.fetchone()
            if not monthly_payment_result:
                print("Unable to calculate monthly mortgage payment.")
                return
            monthly_payment = monthly_payment_result[0]
            
            if monthly_payment is None:
                print("We do not have mortgage data for this state.")
                return

            print(f"\nCalculated Monthly Mortgage Payment: ${monthly_payment:,.2f}")

            cursor.execute("""
                SELECT calc_affordability_ratio(%s, %s)
            """, (
                avg_salary * 1000,
                monthly_payment
            ))

            ratio_result = cursor.fetchone()
            if not ratio_result:
                print("Unable to calculate affordability ratio.")
                return

            affordability_ratio = ratio_result[0]

            print(f"Affordability ratio: {affordability_ratio:.2f}")
            print("Note: A ratio of 30 or less is considered affordable.")

            if affordability_ratio <= 30:
                print(f"A home in {loc_state} is considered affordable. Monthly payment is ${monthly_payment:,.2f}.")
            else:
                print(f"A home in {loc_state} is not affordable with the given job salary and mortgage terms.")

        except mysql.connector.Error as err:
            sys.stderr.write('Database error occurred: ' + str(err) + '\n')

    def view_top_annual_salary_per_state(self):
        """
        Displays the top annual salaries by state.
        """
        cursor = self.conn.cursor()
        try:
            cursor.execute("SELECT loc_state, max_annual_salary FROM top_annual_salary_per_state ORDER BY loc_state;")
            rows = cursor.fetchall()

            print("\nTop Annual Salaries by State:")
            print("=" * 50)
            for row in rows:
                loc_state, max_salary = row
                print(f"State: {loc_state} | Max Annual Salary: ${int(max_salary):,}")
            print("=" * 50)

        except mysql.connector.Error as err:
            sys.stderr.write('Database error occurred: ' + str(err) + '\n')
        finally:
            cursor.close()
        
    def view_top_annual_salary_per_sector(self):
        """
        Displays the top annual salaries by sector.
        """
        cursor = self.conn.cursor()
        try:
            cursor.execute("SELECT sector, max_annual_salary FROM top_annual_salary_per_sector ORDER BY max_annual_salary DESC;")
            rows = cursor.fetchall()

            print("\nTop Annual Salaries by Sector:")
            print("=" * 50)
            for row in rows:
                sector, max_salary = row
                print(f"Sector: {sector:<35} | Max Annual Salary: ${int(max_salary):,}")
                
            print("=" * 50)

        except mysql.connector.Error as err:
            sys.stderr.write('Database error occurred: ' + str(err) + '\n')
        finally:
            cursor.close()

    def search(self, conn):
        """
        Prompts the user to perform a job search with optional 
        job title, city, or state. Then goes back to main options.
        """
        self.search_jobs()
        app.show_options(self, conn)