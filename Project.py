import mysql.connector as msc

db = msc.connect(user = "root", host="localhost", password = "123")
cursor = db.cursor()

cursor.execute("create database bank;")
db.commit()
cursor.execute("use bank;")

cursor.execute("create table logininfo (username varchar(20) NOT NULL PRIMARY KEY, password varchar(20) NOT NULL);")
cursor.execute("create table accountinfo (accountNumber varchar(20) NOT NULL PRIMARY KEY, name varchar(20) NOT NULL, phoneNumber varchar(15) NOT NULL, address varchar(50) NOT NULL, balance integer NOT NULL);")

# THE FIRST PAGE THAT THE USER WILL SEE. GIVES THE OPTION TO SIGNUP OR SIGN IN.

def page1():

    print("WELCOME !!! \n")
    print("1. SIGNUP")
    print("2. LOGIN \n")

    choice = int(input("Kindly click the number corresponding to the action that you want to perform : "))
    print("\n")

    if choice == 1:
        signup()
    elif choice == 2:
        login()
    else:
        print("Kindly select a valid option !!! \n")


#THIS PAGE ALLOWS THE USER TO PERFORM ACTIONS IN HIS/HER ACCOUNT.

def page2():

    print("1. OPEN AN ACCOUNT")
    print("2. CHECK ACCOUNT BALANCE")
    print("3. DEPOSIT MONEY")
    print("4. WITHDRAW MONEY")
    print("5. SEE ACCOUNT INFORMATION")
    print("6. EXIT")
    print()

    opt = int(input("Kindly click on the number corresponding to the action that you want to perform - "))
    print()


    if opt==1:

        acc = int(input("Enter in your account number of choice –"))
        name = input("Enter in your full name - ")
        ph = int(input("Enter in your phone number - "))
        add = input("Enter in your address - ")
        print()

        # INSERTING DATA INTO DATABASE.

        cursor.execute("insert into accountinfo values(%s,%s,%s,%s,%s);", (acc,name,ph,add,0))
        db.commit()

        print("---------------ACCOUNT SUCCESSFULLY ADDED---------------\n")
        page2()


    elif opt == 2:

        n = input("Kindly enter in your account number : ")
        print()
        cursor.execute("select balance from accountinfo where accountnumber = %s;", (n,))
        ans = cursor.fetchall()

        # WE PRINT ans[0][0] AS JUST PRINTING ANS WILL GIVE YOU [(0,)]

        print("-------- YOUR CURRENT BALANCE IS", ans[0][0], "rs –---------","\n")
        page2()


    elif opt == 3:

        n1 = input("Kindly enter in your account number : ")
        n2 = int(input("Kindly enter in the money that you want to deposit : "))
        print()

        cursor.execute("update accountinfo set balance = balance+%s where accountnumber = %s;", (n2,n1))
        db.commit()

        cursor.execute("select balance from accountinfo where accountnumber = %s;", (n1,))
        ans = cursor.fetchall()
        print("---------YOUR CURRENT BALANCE IS", ans[0][0], "rs –---------","\n")

        page2()


    elif opt == 4:

        n1 = input("Kindly enter in your account number : ")
        n2 = int(input("Kindly enter in the money that you want towithdraw : "))
        print()

        cursor.execute("select balance from accountinfo where accountnumber = %s;", (n1,))
        ans = cursor.fetchall()

        if ans[0][0] < n2:

            print("--------------NOT ENOUGH MONEY IN BANK ACCOUNT---------------")
            print()
            page2()

        else:

            # WE DEDUCT THE AMOUNT AND THEN AGAIN RETRIEVE THE BALANCE.

            cursor.execute("update accountinfo set balance = balance-%s where accountnumber = %s;", (n2,n1))
            db.commit()

            cursor.execute("select balance from accountinfo whereaccountnumber = %s;", (n1,))
            ans = cursor.fetchall()

            print("---------- YOUR CURRENT BALANCE IS", ans[0][0],"rs ----------","\n")
            page2()

    
    elif opt == 5:

        n1 = input("Kindly enter in your account number : ")
        print()

        cursor.execute("select * from accountinfo where accountnumber = %s;", (n1,))
        ans = cursor.fetchall()

        print("ACCOUNT NUMBER -", ans[0][0])
        print("NAME -", ans[0][1])
        print("PHONE NUMBER -", ans[0][2])
        print("ADDRESS -", ans[0][3])
        print("BANK BALANCE -", ans[0][4], "rs")

        page2()

    
    elif opt == 6:

        print("---------------THANK YOU---------------")
        print()

    else:

        print("INVALID OPTION, KINDLY CHOOSE A VALID OPTION.")
        page2()


def signup():

    print("---------------NEW USER--------------- \n")
    un = input("Enter in a username - ")
    pw = input("Enter in a password - ")
    print()

    cursor.execute("select username from logininfo;")

    # FOLLOWING COMMAND CHECKS IF USERNAME ALREADY EXISTS IN DATABASE.

    if (un,) in cursor.fetchall():

        print("----------CREDENTIALS ALREADY EXISTS, KINDLYLOGIN WITH YOUR DETAILS---------- \n")
        page1()

    # IF IT IS A NEW USER, DATA IS ADDED TO DATABASE.

    else:

        cursor.execute("insert into logininfo values(%s,%s);", (un,pw))
        db.commit()

        print("---------------SIGNED UP SUCCESSFULLY---------------")
        page1()


def login():

    print("---------------SIGN IN--------------- \n")
    un = input("Enter in a username - ")
    pw = input("Enter in a password - ")
    print()

    cursor.execute("select username from logininfo;")

    # CHECKS IF THE USERNAME IS EXISTANT IN THE DATABASE.

    if (un,) in cursor.fetchall():

        cursor.execute("select username from logininfo;")
        # GATHERS INDEX OF THE USERNAME.
        ind1 = cursor.fetchall().index((un,))
        cursor.execute("select password from logininfo;")

        if (pw,) in cursor.fetchall():

            cursor.execute("select password from logininfo;")
            # GATHERS INDEX OF THE PASSWORD.
            ind2 = cursor.fetchall().index((pw,))
            # THIS COMMAND MAKES SURE THAT THE PASSWORD BELONGS TO THE PARTICULAR USERNAME ENTERED.

            if ind1==ind2:
                print("---------------LOGGED IN SUCCESSFULLY---------------\n")
                page2()
            
            # IF THE PASSWORD ENTERED BELONGS TO SOME OTHER USERNAME, IT GIVESAN ERROR.
            
            else:
                print("---------------INCORRECT PASSWORD---------------")
                page1()
        else:
            print("---------------INCORRECT PASSWORD---------------")
            page1()
    else:
        print("---------------USERNAME DOES NOT EXIST IN DATABASE---------------")
        page1()

page1()




