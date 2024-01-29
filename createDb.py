import sqlite3


def stDatabase():
    con = sqlite3.connect(database=r'std.db')
    cur = con.cursor()

    cur.execute(
        "CREATE TABLE IF NOT EXISTS employee(eid INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT,email TEXT,gender TEXT,"
        "contact TEXT,dob TEXT,doj TEXT,pass TEXT,utype TEXT,address TEXT,salary TEXT)")
    con.commit()

    cur.execute(
        "CREATE TABLE IF NOT EXISTS category(cid INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT)")
    con.commit()

    cur.execute(
        "CREATE TABLE IF NOT EXISTS locations(lid INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT, address TEXT)")
    con.commit()

    cur.execute(
        "CREATE TABLE IF NOT EXISTS product(pid INTEGER PRIMARY KEY AUTOINCREMENT, cid INTEGER, category TEXT,"
        "name TEXT, scheme TEXT, price INTEGER, sellingPrice INTEGER, qty INTEGER, totalPrice INTEGER, status TEXT, location TEXT"
        ", FOREIGN KEY (cid) REFERENCES category(cid))")
    con.commit()

    cur.execute(
        "CREATE TABLE IF NOT EXISTS productDetails(pid INTEGER PRIMARY KEY AUTOINCREMENT, category TEXT,"
        "name TEXT, scheme TEXT, price INTEGER, sellingPrice INTEGER, qty INTEGER, totalPrice INTEGER, status TEXT, location TEXT, Date TEXT, Time, TEXT)")
    con.commit()

    cur.execute(
        '''CREATE TABLE IF NOT EXISTS returnedItems(item_id INTEGER, category TEXT, item_name TEXT, item_price INTEGER
                                                , item_qty INTEGER, item_totalPrice INTEGER, item_returnDate TEXT);''')
    con.commit()

    cur.execute('''CREATE TABLE IF NOT EXISTS orders(orderId INTEGER, pid INTEGER, cid INTEGER, orderItemName TEXT, perItemPrice FLOAT
                                                    , orderQty INTEGER, orderTotalPrice FLOAT, orderStatus TEXT
                                                    , orderDiscount FLOAT, orderNetPrice FLOAT, orderPayType TEXT
                                                    , orderCustomerName TEXT, orderCustomerPhone TEXT, orderDate TEXT
                                                    , orderTime TEXT, FOREIGN KEY (pid) REFERENCES product(pid)
                                                    , FOREIGN KEY (cid) REFERENCES product(cid))''')
    con.commit()

    cur.execute(
        '''CREATE TABLE IF NOT EXISTS returnedOrders(orderId INTEGER, orderItemName TEXT, perItemPrice FLOAT, orderQty INTEGER
                                                    , orderTotalPrice FLOAT, orderStatus TEXT, orderDiscount FLOAT
                                                    , orderNetPrice FLOAT, orderPayType TEXT, orderCustomerName TEXT
                                                    , orderCustomerPhone TEXT, orderDate TEXT, orderTime TEXT);''')
    con.commit()

    cur.execute(
        '''CREATE TABLE IF NOT EXISTS customersDetails(custId INTEGER PRIMARY KEY, custName TEXT, custBalance INTEGER, custStatus TEXT);''')
    con.commit()

    cur.execute(
        '''CREATE TABLE IF NOT EXISTS custPaymentDetails(custId INTEGER, custName TEXT, custBalance INTEGER, custPaid INTEGER
                                                        , custTotalBalance INTEGER, custPayType TEXT, custPayDate TEXT, custStatus TEXT);''')
    con.commit()

    cur.execute(
        '''CREATE TABLE IF NOT EXISTS shopExpensesNames(expID INTEGER PRIMARY KEY AUTOINCREMENT, expName TEXT);''')
    con.commit()

    cur.execute(
        '''CREATE TABLE IF NOT EXISTS shopExpenses(expID INTEGER PRIMARY KEY AUTOINCREMENT, expName TEXT, expDesc TEXT, expPrice INTEGER, expDate TEXT);''')
    con.commit()


stDatabase()
