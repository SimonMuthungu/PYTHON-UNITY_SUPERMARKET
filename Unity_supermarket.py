# A supermarket app backend code... Developed by Simon.

import datetime
import ast
import mysql.connector as con
import secrets


# Checks time to know how to salute the user.
time_of_day = datetime.datetime.now()
am_pm = time_of_day.strftime('%p')
if am_pm == 'AM':
    salutation = "Morning"
else:
    if int(time_of_day.strftime('%I')) < 3:
        salutation = 'Afternoon'
    else:
        salutation = 'Evening'

# Admin user...
def Admin():
    name = input(f'Whats your first name:\n')
    try:
        with open('D:\python general\supermarket_app\Admin_file.txt') as readAdmin:
            for line in readAdmin.readlines():
                 # converting to dictionary
                record = ast.literal_eval(line)
                if record['name'] == name:
                    print(f'Welcome {name.capitalize()}')

                    code = input(f'Enter your admin secret password, {name.capitalize()}:\n')
                    if code == record['secret_pass']:
                        print(f'\nLogging you in as {name.capitalize()}... Welcome\n')
                        # log file recording...
                        return True
                    else:
                        print('Wrong pin... please be careful...')
                        # log file recording of wrong pin
                        return False
                else:
                    print('\nWe have a few admin names but yours seems not to be one of them...Please consult one of the admins to add you\n')
                    # Log of admin name mismatch 
                    return False
    except:
        # if this program is being run for the first time
        print('\nSeems you\'re running this program for the first time; Please enter your name to set you as admin:')
        admin_name = input()
        secret_pass = input('Also enter a secret passkey that you can remember easily:\n')
        admin_details = str({'name':admin_name, 'secret_pass':secret_pass})

        with open('D:\python general\supermarket_app\Admin_file.txt', 'w') as first_admin:
            first_admin.write(admin_details + '\n') 
        print('First admin file created') # can be logged...
    try:
    # creates also the cashier files
        with open('D:\python general\supermarket_app\Cashier_file.txt', 'w') as createCashier:
            cashier_name = input('Enter the name of one cashier to start with...:\n')
            cashier_pass = input(f'\nSetup a password for {cashier_name.capitalize()} to access the system')
            cashier_details = str({'name':cashier_name, 'secret_pass':cashier_pass})
            createCashier.write(cashier_details + '\n')
    except:
        with open('D:\python general\supermarket_app\Cashier_file.txt', 'w') as createCashier:
            cashier_name = input('Enter the name of one cashier to start with...:\n')
            cashier_pass = input(f'\nSetup a password for {cashier_name.capitalize()} to access the system:\n')
            cashier_details = str({'name':cashier_name, 'secret_pass':cashier_pass})
            createCashier.write(cashier_details + '\n') 



# Cashier
def Cashier():
    name = input(f'Whats your first name:\n')
    with open('D:\python general\supermarket_app\Cashier_file.txt') as readCashier:
        for line in readCashier.readlines():
                # converting to dictionary again
            record = ast.literal_eval(line)
            if record['name'] == name:
                print(f'Welcome {name.capitalize()}')

                code = input(f'Enter your cashier secret password, {name.capitalize()}:\n')
                if code == record['secret_pass']:
                    print(f'\nLogged in as {name.capitalize()}... Welcome\n')
                    # log file recording...
                    return True
                else:
                    print('Wrong access passwrod, please be careful...')
                    # log file recording of wrong pin
                    return False
            else:
                print('\nYour name seems not to be in our records...\n') 
                # Log of admin name mismatch 
                return False

def Customer():
    print('Welcome to Unity Supermarket... We\'ll be happy to know your name...:')
    customer_name = input()
    mydb = con.connect(host='localhost', user='root', password='***** #for security', database='Unity_supermarket')
    cursor = mydb.cursor()

    # makes a log of this customers events
    print(f'Please tell us how we can help you, {customer_name.capitalize()}...\n')
    customer_event = int(input('1-I want to shop\n2-I want to report misconduct\n3-I want to return a good\nSelect the option number:\n'))
    if customer_event == 1:
        # making db connection with db as products
        mydb = con.connect(host='localhost', user='root', password='***** #for security', database='Products')
        cursor = mydb.cursor()

        print('Here are the product categories you can shop from...')
        # categories of products from the db
        cursor.execute('SHOW TABLES')
        prod_categories = cursor.fetchall()

        for x in prod_categories:
            print(x)

        category = input('please enter the category of products you want to shop... ')
        #display all products with given category
        try:
            cursor.execute(f'SELECT * FROM {category}')
            products = cursor.fetchall()
            for x in products:
                print(x)

        except:
            print('Seems the product category you choose isnt existent...')
            print('The problem could also be an issue on our side with the database, do bear with us.')

    elif customer_event == 2:
        print('First, we are very sorry for any misconduct you may have encountered. We promise to work our best to resolve any misconduct fairly...')
        misc_type = input('Please enter the misconduct that occured to you:\n1-Abuse\n2-Violence\n3-Theft\n4-Describe it yourself...\n')
        if misc_type != 4:
            misc_employee = input('Please enter the employee name that mishandled you...')
            misc_description = input('Enter a brief description of what happened...')
            print('This will be looked at by our manager and we promise to get back to you.')
            customer_no = input('Please enter your number incase we have to call you')

            # Update and db with issue
            mydb = con.connect(host='localhost', user='root', password='***** #for security', database='Unity_supermarket')
            cursor = mydb.cursor()

            issue = f'Customer {customer_name} allegedly mishandled by {misc_employee} with the following description: {misc_description}. Customer contact: {customer_no}'

            cursor.execute(f'INSERT INTO customer_issues (issue_description) VALUES({issue})')

        else:
            misc_description = input('Please enter a brief description of what happened...')
            misc_employee = input('Please enter the employee name that mishandled you...')
            print('Our QA managers have been given a report of this issue. We will get back to you soonest. Thanks')
            customer_no = input('Please enter your number incase we have to call you')

            # update db with issue
            mydb = con.connect(host='localhost', user='root', password='***** #for security', database='Unity_supermarket')
            cursor = mydb.cursor()

            issue = f'Customer {customer_name} allegedly mishandled by {misc_employee} with the following description: {misc_description}. Customer contact: {customer_no}'

            try:
                cursor.execute(f'INSERT INTO customer_issues (issue_description) VALUES({issue})')
            except:
                pass
            # does nothing but should create a file and save the issue in the meantime

    elif customer_event == 3:
        # checks sales files to ascertain whether there was this purchase
        receipt_no = input('Please enter the receipt number:\n')

        # checks transaction details from the table sales in the db
        mydb = con.connect(host='localhost', user='root', password='***** #for security', database='Unity_supermarket')
        cursor = mydb.cursor() 

        sql = f"SELECT receipt_id FROM sales WHERE receipt_id = '{receipt_no}'"
        cursor.execute(sql)
        valid_purchase = cursor.fetchall()

        # checks if theres a value in the variable meaning there was such a sale...
        # updates necessary files and db for the return
        if valid_purchase:
                return_reason = input('Please enter the reason for your return in brief:\n') 
                cursor.execute(f'INSERT INTO customer_queries(issue_description) VALUES("{customer_name}{return_reason}")')
        
    else: 
        print('Invalid selection, was nice having you...')
    return 

    

#checks to know who the user is, logs them in and records in the log files!
who_r_you = int(input(f'\nGood {salutation}, Who are you?:\n1-Admin\n2-Cashier\n3-Customer\n\nSelect number: '))

if who_r_you == 1:
    # Admin()
    if Admin():
        admin_event = int(input('What would you like to do?:\n1-add products\n2-update cashier list\n3-check sales\n4-check products in store\n5-Check customer records:\n'))

        if admin_event == 1:
            prod_cat = input('Enter the category of the product (sports, electronic, beauty?):\n')
            prod_name = input('Enter the product name:\n')
            prod_price = int(input('Set price:\n'))

            #making product id and date in
            prod_id = secrets.token_hex(2)
            date_in = datetime.datetime.now().strftime('%c')

            # for connection to the database
            mydb = con.connect(host='localhost', user='root', password='***** #for security', database='Products')
            cursor = mydb.cursor()

            #adding products to db
            query = f'INSERT INTO {prod_cat} (prod_id, name, price, date_in, date_out) VALUES (%s, %s, %s, %s, %s)'
            val = (prod_id, prod_name, prod_price, date_in, '-')

            try:
                cursor.execute(query, val)
                mydb.commit()
            except:
                print("\n!!!\nfor some reason, we cannot connect to the database, check the connection or contact simon for help.")

        elif admin_event == 2:
            #update cashier files and db
            new_cashier = input('Enter the name of the cashier you  want to add:\n')
            new_cashier_pass = int(input(f'Give {new_cashier} a secret passcode:\n'))
            # writing cashier details to file
            with open('D:\python general\supermarket_app\Cashier_file.txt', 'a') as addCashier:
                time = datetime.datetime.now()
                details = str({'name': new_cashier, 'secret_pass': new_cashier_pass, 'added':time.strftime('%x')})
                addCashier.write(details)
                # Then write to db
                # for connection to the database
            mydb = con.connect(host='localhost', user='root', password='***** #for security', database='Unity_supermarket')
            cursor = mydb.cursor()

            #adding products to db
            query = f'INSERT INTO employees (name, level, date_started) VALUES (%s, %s, %s)'
            val = (new_cashier, 'cashier', datetime.datetime.now().strftime('%c'))

            try:
                cursor.execute(query, val)
                mydb.commit()
            except:
                print("\n!!!\nfor some reason, we cannot connect to the database, check the connection or contact simon for help.")

        elif admin_event == 3:
            #check sales summary from db or sales files
            mydb = con.connect(host='localhost', user='root', password='***** #for security', database='Unity_supermarket')
            cursor = mydb.cursor()

            #adding products to db
            cursor.execute('SELECT * FROM sales')
            sales = cursor.fetchall()
            for sale in sales:
                print(sale)

        elif admin_event == 4:
            # enter category to check from db
            category = input('Enter category to check:\n')
            #checks the products database and table for entered category
            mydb = con.connect(host='localhost', user='root', password='***** #for security', database='Products')
            cursor = mydb.cursor()

            #adding products to db
            cursor.execute(f'SELECT * FROM {category}')
            prods = cursor.fetchall()
            if not prods:
                print('There are no products here. Thank you!')
            else:
                print(f'These are the products in the {category} section:\n')
            for prod in prods:
                print(prod) 

        else:
            print('Here are the customers records at unity supermarket:')
            # prints customers details from files and possibly db
            mydb = con.connect(host='localhost', user='root', password='***** #for security', database='Unity_supermarket')
            cursor = mydb.cursor()

            #adding products to db
            cursor.execute(f'SELECT * FROM Customers')
            custs = cursor.fetchall()
            for cust in custs:
                print(cust) 


elif who_r_you == 2:
    # Cashier()

    if Cashier():
        cashier_event = int(input('what do u want to do?\n1-receive returned product\n2-make transaction:\n'))
        
        if cashier_event == 1:
            receipt_no = input('Enter the returned good\'s receipt number')
            # checks whether sale had been done and does what happens in customer return goods menu
        
        elif cashier_event == 2:
            print('Enter q to quit making transactions\n')
            # Keep making transactions iteratively until the cashier breaks out
            while True: 
                # Enter the good code_id
                product_id = input('Enter 4-digit product id:\n')

                # if q is entered insted of code_id, exits transaction mode.
                if product_id == 'q':
                    break

                else:
                    name = input('Enter name of product:\n')
                    time_of_sale = datetime.datetime.now().strftime('%p')
                    receipt_no = secrets.token_hex(2)

                    # removes product from the products list and updates the sales table
                    mydb = con.connect(host='localhost', user='root', password='***** #for security', database='Unity_supermarket')
                    cursor = mydb.cursor()

                    #adding products to db
                    query = f'INSERT INTO sales (receipt_id, cashier, customer, time) VALUES (%s, %s, %s, %s)'
                    val = (receipt_no, '','', datetime.datetime.now().strftime('%c'))

                    try:
                        cursor.execute(query, val)
                        mydb.commit()
                    except:
                        print("\n!!!\nfor some reason, we cannot connect to the database, check the connection or contact simon for help.") 
                
elif who_r_you == 3:
    Customer()
