from flask import Blueprint, render_template, request, flash, redirect, url_for
from sql.db import DB
company = Blueprint('company', __name__, url_prefix='/company')

@company.route("/search", methods=["GET"])
def search():
    rows = []
    # DO NOT DELETE PROVIDED COMMENTS
    # TODO search-1 retrieve id, name, address, city, country, state, zip, website, employee count for the company
    # don't do SELECT *
    # retrieved id, name, address, city, country, state, zip, website, employee count for the company - Kshitij Aji, ka598, Dec 03 2022
    query = """
    SELECT id, name, address, city, country, state, zip, website FROM IS601_MP2_Companies WHERE 1=1
    """
    args = [] # <--- append values to replace %s placeholders
    allowed_columns = ["name", "city", "country", "state"]
    print('The query parameters are ',args)
    allowed_list = [(v,v) for v in allowed_columns]
    # TODO search-2 get name, country, state, column, order, limit request args
    # Added request args to get name, country, state, column, order, limit - Kshitij Aji, ka598, Dec 03 2022
    request_args = request.args.to_dict()
    # TODO search-3 append a LIKE filter for name if provided
    # appended a LIKE filter for name if provided - Kshitij Aji, ka598, Dec 03 2022
    if request_args.get('name'):
        query+=" AND name like %s"
        args.append("%"+request_args.get('name')+"%")
    # TODO search-4 append an equality filter for country if provided
    # appended an equality filter for country if provided - Kshitij Aji, ka598, Dec 03 2022
    if request_args.get('country'):
        query+=" AND country=%s"
        args.append(request_args.get('country'))
    # TODO search-5 append an equality filter for state if provided
    # appended an equality filter for state if provided - Kshitij Aji, ka598, Dec 03 2022
    if request_args.get('state'):
        query+=" AND state=%s"
        args.append(request_args.get('state'))
    # TODO search-6 append sorting if column and order are provided and within the allows columsn and allowed order asc,desc
    # appended sorting if column and order are provided and within the allows columsn and allowed order asc,desc - Kshitij Aji, ka598, Dec 03 2022
    if request_args.get('column') and request_args.get('order') and (request_args.get('column') in allowed_columns):
        query+=" ORDER BY "+request_args.get('column') +" "+request_args.get('order')
    # TODO search-7 append limit (default 10) or limit greater than 1 and less than or equal to 100
    # TODO search-8 provide a proper error message if limit isn't a number or if it's out of bounds
    # Added search-7 and search-8 - Kshitij Aji, ka598, Dec 03 2022
    if request_args.get('limit'):
        if int(request_args.get('limit'))>1 and int(request_args.get('limit'))<=100:
            query+=" limit "+request_args.get('limit')
        else:
            flash('Request Limit is invalid','danger')
    else:
        query+=" limit 10"

    print("The query is: ",query)
    print("The args are: ", args)
    try:
        result = DB.selectAll(query, *args)
        if result.status:
            rows = result.rows
            print('The result of Company search is :',rows)
    except Exception as e:
        # TODO search-9 make message user friendly
        # Made the message user friendly - Kshitij Aji, ka598, Dec 03 2022
        print('There was an error fetching the data',e)
        flash('There was an error fetching the required data', "danger")
    # hint: use allowed_columns in template to generate sort dropdown
    return render_template("list_companies.html", rows=rows, allowed_list=allowed_list)

    
@company.route("/add", methods=["GET","POST"])
def add():
    if request.method == "POST":
        has_error = False # use this to control whether or not an insert occurs
         # TODO add-1 retrieve form data for name, address, city, state, country, zip, website
         # retrieved form data for name, address, city, state, country, zip, website - Kshitij Aji, ka598, Dec 03 2022
        request_args = request.form.to_dict()
        print('The request agrs for Add company:',request_args)
        # TODO add-2 name is required (flash proper error message)
        # Added the flash message - Kshitij Aji, ka598, Dec 03 2022
        if(not request_args.get('name')):
            flash('Name is required, Please enter the name!','danger')
            has_error=True
        # TODO add-3 address is required (flash proper error message)
        # Added the flash message - Kshitij Aji, ka598, Dec 03 2022
        if(not request_args.get('address')):
            flash('Address is required, Please enter the Address!','danger')
            has_error=True
        # TODO add-4 city is required (flash proper error message)
        # Added the flash message - Kshitij Aji, ka598, Dec 03 2022
        if(not request_args.get('city')):
            flash('City is required, Please enter the city! ','danger')
            has_error=True
        # TODO add-5 state is required (flash proper error message)
        # Added the flash message - Kshitij Aji, ka598, Dec 03 2022
        if(not request_args.get('state')):
            flash('State is required, Please enter the state!','danger')
            has_error=True
        # TODO add-6 country is required (flash proper error message)
        # Added the flash message - Kshitij Aji, ka598, Dec 03 2022
        if(not request_args.get('country')):
            flash('Country is required! Please enter the country ','danger')
            has_error=True
        # TODO add-7 website is not required
        if not has_error:
            try:
                result = DB.insertOne("""
                INSERT INTO IS601_MP2_Companies (name, address, city, zip, country, state, website)
                        VALUES (%(name)s, %(address)s, %(city)s, %(zip)s ,%(country)s, %(state)s, %(website)s)
                """, request_args) # <-- TODO add-8 add query and add arguments
                # Added query - Kshitij Aji, ka598, Dec 03 2022
                if result.status:
                    flash("Company was successfully added. ", "success")
            except Exception as e:
                # TODO add-9 make message user friendly
                # Added the flash message - Kshitij Aji, ka598, Dec 03 2022
                print('There was an error while adding the company',e)
                flash('There was an error while adding the company', "danger")
    return render_template("add_company.html")


@company.route("/edit", methods=["GET", "POST"])
def edit():
 # TODO edit-1 request args id is required (flash proper error message)
 # Added flash message -  - Kshitij Aji, ka598, Dec 03 2022
    has_error = False
    row=[]
    company_id = request.args.get('id')
    if company_id: # TODO update this for TODO edit-1
        if request.method == "POST":
            # TODO edit-2 retrieve form data for name, address, city, state, country, zip, website
            # retrieved form data for name, address, city, state, country, zip, website - Kshitij Aji, ka598, Dec 03 2022
            formData = request.form.to_dict()
            # TODO edit-3 name is required (flash proper error message)
            # Added flash message -  - Kshitij Aji, ka598, Dec 03 2022
            if not formData.get('name'):
                flash('Name is required, Please enter the name!','danger')
                has_error=True
            # TODO edit-4 address is required (flash proper error message)
            # Added flash message -  - Kshitij Aji, ka598, Dec 03 2022
            if not formData.get('address'):
                flash('Address is required, Please enter the address!','danger')
                has_error=True
            # TODO edit-5 city is required (flash proper error message)
            # Added flash message -  - Kshitij Aji, ka598, Dec 03 2022
            if not formData.get('city'):
                flash('City is required, Please enter the city!','danger')
                has_error=True
            # TODO edit-6 state is required (flash proper error message)
            # Added flash message -  - Kshitij Aji, ka598, Dec 03 2022
            if not formData.get('state'):
                flash('State is required, Please enter the state!','danger')
                has_error=True
            # TODO edit-7 country is required (flash proper error message)
            # Added flash message -  - Kshitij Aji, ka598, Dec 03 2022
            if not formData.get('country'):
                flash('Country is required, Please enter the country !','danger')
                has_error=True
            # TODO edit-8 website is not required
            # note: call zip variable zipcode as zip is a built in function it could lead to issues
            data = [formData.get('name',''), formData.get('address',''), formData.get('city',''),\
                 formData.get('state',''), formData.get('country',''), formData.get('zip',''), formData.get('website','')]
            data.append(company_id)
            try:
                # TODO edit-9 fill in proper update query
                result = DB.update("""
                UPDATE IS601_MP2_Companies SET name=%s, address=%s, city=%s, state=%s,
                country=%s, zip=%s, website=%s WHERE id=%s
                """, *data)
                if result.status:
                    flash("The record has been updated. ", "success")
            except Exception as e:
                # TODO edit-10 make this user-friendly
                # Added flash message to make it user firendly  - Kshitij Aji, ka598, Dec 03 2022
                print('An error occurred during updation of company',e)
                flash('An error occurred during updation of company', "danger")
        try:
            # TODO edit-11 fetch the updated data
            result = DB.selectOne("SELECT name, address, city, state, country, zip, website FROM IS601_MP2_Companies WHERE id=%s", company_id)
            if result.status:
                row = result.row
                print('The company data is: ',row)
        except Exception as e:
            # TODO edit-12 make this user-friendly
            print('There was an error while fetching the company data',e)
            flash('There was an error while fetching the company data', "danger")
    # TODO edit-13 pass the company data to the render template
    return render_template("edit_company.html", row=row)


@company.route("/delete", methods=["GET"])
def delete():
    # TODO delete-1 delete company by id (unallocate any employees)
    # deleted company by id (unallocate any employees) - Kshitij Aji, ka598, Dec 03 2022
    company_id = request.args.get('id')
    has_error = False
    if company_id:
        try:
            result = DB.selectAll('SELECT id FROM IS601_MP2_Companies WHERE name=%s','N/A')
            if not result.rows:
                result = DB.insertOne("""INSERT INTO IS601_MP2_Companies (name, address, city, country, state, website)
                        VALUES ('N/A','N/A','N/A','N/A','N/A','N/A')""")
            result = DB.selectAll('SELECT id FROM IS601_MP2_Companies WHERE name=%s','N/A')
            DB.update("""UPDATE IS601_MP2_Employees SET company_id=%s WHERE company_id=%s""",*[result.rows[0]['id'],company_id])
            delete_ = DB.delete("DELETE FROM IS601_MP2_Companies where id=%s", company_id)
        except Exception as e:
            print('There was an error while deleting the company',e)
            flash('There was an error while deleting the company','danger')
            has_error=True
    # TODO delete-2 redirect to company search
    # TODO delete-3 pass all argument except id to this route
    # TODO delete-4 ensure a flash message shows for successful delete
    # Added delete-2, delete-3, delete-4 - Kshitij Aji, ka598, Dec 03 2022
    if not has_error:
        flash('The company was successfully deleted','success')
    return redirect('/company/search')
   