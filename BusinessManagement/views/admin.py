import io
from flask import Blueprint, render_template, request, redirect, flash
from werkzeug.utils import secure_filename
from sql.db import DB
import traceback
import re
import csv
admin = Blueprint('admin', __name__, url_prefix='/admin')

@admin.route("/import", methods=["GET","POST"])
def importCSV():
    if request.method == "POST":
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file', "warning")
            return redirect(request.url)
        # TODO importcsv-1 check that it's a .csv file, return a proper flash message if it's not
        # Added code to check that file is in .csv format - Kshitij Aji (UCID: ka598), Nov 21, 2022
        if not re.search(r'.\.csv',file.filename):
            flash("The file selected is not in CSV format, please select a file that is in csv format.","warning")
            return redirect(request.url)
            
        '''
        allowed_extension = {"csv"}
        if file.filename.rsplit(".")[1].lower() in allowed_extension:
            print(f"{file.filename} is in the correct format.")
            pass
        else: 
            flash("Selected file is not in .csv format", "warning")
            return redirect(request.url)
        '''
        
        if file and secure_filename(file.filename):
            companies = []
            employees = []
            company_query = """
            INSERT INTO IS601_MP2_Companies (name, address, city, country, state, zip, website)
                        VALUES (%(name)s, %(address)s, %(city)s, %(country)s, %(state)s, %(zip)s, %(website)s)
                        ON DUPLICATE KEY UPDATE address = %(address)s, city = %(city)s, country=%(country)s, state=%(state)s, zip=%(zip)s, website=%(website)s 
            """
            employee_query = """
             INSERT INTO IS601_MP2_Employees (first_name, last_name, email, company_id)
                        VALUES (%(first_name)s, %(last_name)s, %(email)s, 
                        (SELECT id FROM IS601_MP2_Companies WHERE name = %(company_name)s LIMIT 1))
                        ON DUPLICATE KEY UPDATE first_name=%(first_name)s, last_name = %(last_name)s, email = %(email)s, company_id = (SELECT id FROM IS601_MP2_Companies WHERE name = %(company_name)s LIMIT 1)
            """
            # Note: this reads the file as a stream instead of requiring us to save it
            stream = io.TextIOWrapper(file.stream._file, "UTF8", newline=None)
            # TODO importcsv-2 read the csv file stream as a dict
            # Reading the csv file stream as a dict - Kshitij Aji, ka598, Nov 21, 2022
            for row in csv.DictReader(stream, delimiter=','):
                # print(row) #example
                # TODO importcsv-3 extract company data and append to company list as a dict only with company data
                # Added company data to the company list - Kshitij Aji, ka598, Nov 21, 2022
                if row["company_name"] and row["address"] and row["city"] and row["state"] and row["zip"] and row["web"]:
                    companies.append({'name': row['company_name'],'address':row['address'],'city':row['city'],\
                        'country':row['country'],'state':row['state'],'zip': row['zip'],'website': row['web']})
                # TODO importcsv-4 extract employee data and append to employee list as a dict only with employee data
                # Added employee data to the employee list - Kshitij Aji, ka598, Nov 21, 2022
                if row["first_name"] and row["last_name"] and row["email"] and row["company_name"]:
                    employees.append({'first_name': row['first_name'],'last_name': row['last_name'],\
                        'email': row['email'],'company_name':row['company_name']})

            if len(companies) > 0:
                print(f"Inserting or updating {len(companies)} companies")
                try:
                    result = DB.insertMany(company_query, companies)
                    # TODO importcsv-5 display flash message about number of companies inserted
                    # Added flash message to display number of companies inserted - Kshitij Aji, ka598, Nov 21, 2022
                    flash(f"The number of companies inserted in the database is {len(companies)}.","info")
                except Exception as e:
                    traceback.print_exc()
                    flash("There was an error loading in the csv data", "danger")
            else:
                # TODO importcsv-6 display flash message (info) that no companies were loaded
                # Added flash message to display that no companies were loaded to the database. - Kshitij Aji, ka598, Nov 21, 2022
                flash("No companies were loaded to the database.", "info")
            if len(employees) > 0:
                print(f"Inserting or updating {len(employees)} employees")
                try:
                    result = DB.insertMany(employee_query, employees)
                    # TODO importcsv-7 display flash message about number of employees loaded
                    # Added flash message to display number of employees inserted - Kshitij Aji, ka598, Nov 21, 2022
                    flash(f"The number of employees inserted in the database is {len(employees)}.", "info")
                except Exception as e:
                    traceback.print_exc()
                    flash("There was an error loading in the csv data", "danger")
            else:
                 # TODO importcsv-8 display flash message (info) that no employees were loaded
                #pass
                # Added flash message to display that no employees were loaded to the database. - Kshitij Aji, ka598, Nov 21, 2022
                flash("No employees were inserted into the database.", "info")
    return render_template("upload.html")
