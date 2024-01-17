from flask import Blueprint, render_template, request, flash, redirect
from sql.db import DB
employee = Blueprint('employee', __name__, url_prefix='/employee')


@employee.route("/search", methods=["GET"])
def search():
    rows = []
    # DO NOT DELETE PROVIDED COMMENTS
    # TODO search-1 retrieve employee id as id, first_name, last_name, email, company_id, company_name using a LEFT JOIN
    # Added select query to retreive data using Left join on the comapanies and employees relation - Kshitij Aji, ka598, Dec 03, 2022
    query = """SELECT E.id, E.first_name, E.last_name, E.email, E.company_id, C.name as company_name from IS601_MP2_Employees E
     LEFT JOIN IS601_MP2_Companies C ON E.company_id=C.id WHERE 1=1"""
    args = [] # <--- append values to replace %s placeholders
    allowed_columns = ["first_name", "last_name", "email", "company_name"]
    allowed_list = [(v,v) for v in allowed_columns]
    # TODO search-2 get fn, ln, email, company, column, order, limit from request args
    # Added code to get fn, ln, email, company, column, order, limit from request args - Kshitij Aji, ka598, Dec 03 2022
    request_args = request.args.to_dict()
    print('Request Args from Employees:',request_args)
    # TODO search-3 append like filter for first_name if provided
    # Appended like filter for first_name if provided - Kshitij Aji, ka598, Dec 03 2022
    if request_args.get('first_name'):
        query+=" AND first_name like %s"
        args.append("%"+request_args.get('first_name')+"%")

    # TODO search-4 append like filter for last_name if provided
    # Appended like filter for last_name if provided - Kshitij Aji, ka598, Dec 03 2022
    if request_args.get('last_name'):
        query+=" AND last_name like %s"
        args.append("%"+request_args.get('last_name')+"%")

    # TODO search-5 append like filter for email if provided
    # Appended like filter for email if provided - Kshitij Aji, ka598, Dec 03 2022 
    if request_args.get('email'):
        query+=" AND email like %s"
        args.append("%"+request_args.get('email')+"%")

    # TODO search-6 append equality filter for company_id if provided
    # Appended equality filter for company_id if provided - Kshitij Aji, ka598, Dec 03 2022 
    if request_args.get('company'): # check if this should be company_id 
        query+=" AND company_id=%s"
        args.append(request_args.get('company'))

    # TODO search-7 append sorting if column and order are provided and within the allowed columns and order options (asc, desc)
    # Appended sorting if column and order are provided and within the allowed columns and order options (asc, desc) - Kshitij Aji, ka598, Dec 03 2022 
    if request_args.get('column') and request_args.get('order') and (request_args.get('column') in allowed_columns):
        query+=" ORDER BY "+request_args.get('column') +" "+request_args.get('order')

    # TODO search-8 append limit (default 10) or limit greater than 1 and less than or equal to 100
    # TODO search-9 provide a proper error message if limit isn't a number or if it's out of bounds
    # Added todo items search-8 and search-9 - Kshitij Aji, ka598, Dec 03 2022 
    if request_args.get('limit'):
        if int(request_args.get('limit'))>1 and int(request_args.get('limit'))<=100:
            query+=" limit "+request_args.get('limit')
        else:
            flash('The limit is out of bounds','danger')
    else:
        query+=" limit 10"

    print("query",query)
    print("args", args)
    try:
        result = DB.selectAll(query, *args)
        if result.status:
            rows = result.rows
            print(f'The result of the employee search is {rows}')
    except Exception as e:
        # TODO search-10 make message user friendly
        #  made the message user friendly - Kshitij Aji, ka598, Dec 03 2022 
        print('There was an error in fetching the data:',e)
        flash('There was an error in fetching the data', "danger")
    # hint: use allowed_columns in template to generate sort dropdown
    # Changed to allowed_list instead of allowed_columns - Kshitij Aji, ka598, Nov 30, 2022
    return render_template("list_employees.html", rows=rows, allowed_list = allowed_list)

@employee.route("/add", methods=["GET","POST"])
def add():
    if request.method == "POST":
        # TODO add-1 retrieve form data for first_name, last_name, company, email
        # retrieved form data for first_name, last_name, company, email - Kshitij Aji, ka598, Dec 03 2022 
        is_error = False
        request_args = request.form.to_dict()
        # TODO add-2 first_name is required (flash proper error message)
        # Added flash message - Kshitij Aji, ka598, Dec 03 2022 
        if(not request_args.get('first_name')):
            flash('First Name is required!','danger')
            is_error=True
        # TODO add-3 last_name is required (flash proper error message)
        # Added flash message - Kshitij Aji, ka598, Dec 03 2022 
        if(not request_args.get('last_name')):
            flash('Last name is required!','danger')
            is_error=True
        # TODO add-4 company (may be None)
        # Added request args for company - Kshitij Aji, ka598, Dec 03 2022 
        if(not request_args.get('company')):
            request_args['company']=None
        # TODO add-5 email is required (flash proper error message)
        # Added flash message - Kshitij Aji, ka598, Dec 03 2022 
        if(not request_args.get('email')):
            flash('Email is Required!','danger')
            is_error=True
        if not is_error:
            try:
                result = DB.insertOne("""
                INSERT INTO IS601_MP2_Employees (first_name, last_name, email, company_id)
                        VALUES (%(first_name)s, %(last_name)s, %(email)s, %(company)s)
                """,
                request_args) # <-- TODO add-6 add query and add arguments
                # Added query -  Kshitij Aji, ka598, Dec 03 2022 
                if result.status:
                    flash("Created Employee Record", "success")
            except Exception as e:
                # TODO add-7 make message user friendly
                # Added flash messages to make them user friendly -  Kshitij Aji, ka598, Dec 03 2022 
                print('There was an error while attempting to add a new employee',e)
                flash('There was an error while attempting to add a new employee', "danger")
    return render_template("add_employee.html")

@employee.route("/edit", methods=["GET", "POST"])
def edit():
    row = []
    e_id = request.args.get('id')
    # TODO edit-1 request args id is required (flash proper error message)
    # Added flash messages to make them user friendly -  Kshitij Aji, ka598, Dec 03 2022 
    form_data = {}
    if e_id: # TODO update this for TODO edit-1
        is_error = False
        if request.method == "POST":
            # TODO edit-1 retrieve form data for first_name, last_name, company, email
            # Retrieved form data for first_name, last_name, company, email - Kshitij Aji, ka598, Dec 03 2022 
            form_data= request.form.to_dict()
            # TODO edit-2 first_name is required (flash proper error message)
            # Added flash messages to make them user friendly -  Kshitij Aji, ka598, Dec 03 2022 
            if not form_data.get('first_name'):
                flash('Please enter the First Name, it is required !','danger')
                is_error=True
            # TODO edit-3 last_name is required (flash proper error message)
            # Added flash messages to make them user friendly -  Kshitij Aji, ka598, Dec 03 2022 
            if not form_data.get('last_name'):
                flash('Please enter the Last Name, it is required !','danger')
                is_error=True
            # TODO edit-4 company may be None
            # Added condition so that company may be None -  Kshitij Aji, ka598, Dec 03 2022 
            if (not form_data.get('company')):
                form_data['company']= None
            # TODO edit-5 email is required (flash proper error message)
            # Added flash messages to make them user friendly -  Kshitij Aji, ka598, Dec 03 2022
            if not form_data.get('email'):
                flash('Please enter the email, it is required !','danger')
                is_error=True
            if(is_error):
                return render_template("edit_employee.html",row={},value=None)
            data = [form_data.get('first_name'), form_data.get('last_name'), form_data.get('company',None),\
                form_data.get('email',None),e_id]
            print('The arguments for emplyee edit:',data)
            try:
                # TODO edit-6 fill in proper update query
                # Update query is added - Kshitij Aji, ka598, Dec 03 2022
                result = DB.update("""
                UPDATE IS601_MP2_Employees SET first_name=%s, last_name=%s, 
                company_id=%s, email=%s WHERE id=%s
                """, *data)
                if result.status:
                    print('The Record has been Updated.',result)
                    flash("The Record has been Updated.", "success")
            except Exception as e:
                # TODO edit-7 make this user-friendly
                # Added flash messages to make them user friendly -  Kshitij Aji, ka598, Dec 03 2022
                print('There was an error updating the employee record.',e)
                flash('There was an error updating the employee record. Try again later!', "danger")
        try:
            # TODO edit-8 fetch the updated data (including company_name)
            # company_name should be 'N/A' if the employee isn't assigned to a copany
            # Fetched the updated data (including company_name)  -  Kshitij Aji, ka598, Dec 03 2022
            result = DB.selectOne("""SELECT e.id, e.first_name, e.last_name, e.email, e.company_id, c.name as company_name from IS601_MP2_Employees e
     LEFT JOIN IS601_MP2_Companies c ON e.company_id=c.id WHERE e.id=%s""", e_id)
            if result.status:
                row = result.row
                print('Employee Data is fetched',row)
        except Exception as e:
            # TODO edit-9 make this user-friendly
            # Added user friendly messages -  Kshitij Aji, ka598, Dec 03 2022
            print('There was an error in fetching the employee data',e)
            flash('There was an error in fetching the employee data', "danger")
    # TODO edit-10 pass the employee data to the render template
    # Passed the employee data to the render template - Kshitij Aji, ka598, Dec 03 2022
    return render_template("edit_employee.html", row=row, val=row.get('company_id',None))


@employee.route("/delete", methods=["GET"])
def delete():
    # TODO delete-1 delete employee by id
    #  Deleted employee by id - Kshitij Aji, ka598, Dec 03 2022
    employee_id = request.args.get('id')
    is_error = False
    if employee_id:
        try:
            result = DB.delete("DELETE FROM IS601_MP2_Employees where id=%s", employee_id)
        except Exception as e:
            flash('There was an error in deleting the employee from the database','danger')
            is_error=True
    # TODO delete-2 redirect to employee search
    # TODO delete-3 pass all argument except id to this route
    # TODO delete-4 ensure a flash message shows for successful delete
    # Added todo items delete-2, delete-3, delete-4 - Kshitij Aji, ka598, Dec 03 2022
    if not is_error:
        flash('The employee was deleted successfully','success')
        return redirect('/employee/search')
    
