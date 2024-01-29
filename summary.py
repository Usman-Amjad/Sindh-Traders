# -------Importing Modules
from tkinter import *
import customtkinter as ctk
import sqlite3
from tkinter import ttk
import win32print
import win32api
from fpdf import FPDF
from tkinter import messagebox
from PIL import Image
from tkcalendar import DateEntry
import datetime


class allSummary:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1520x770+0+0")
        self.root.title("Summary")
        # self.root.resizable(False, False)
        self.root.focus_force()

        ctk.set_appearance_mode("light")  # Modes: system (default), light, dark
        ctk.set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green

        # ==Declaring Variables==
        self.invoice_no = StringVar()
        self.item_name = StringVar()  # For Row 2
        self.searchOption = StringVar(value="Select")  # For search
        self.search_txt = StringVar()  # For search
        self.search_cmb = StringVar()  # For search

        self.var_loc = StringVar()
        self.loc_list = []
        self.fetch_cat_loc()

        self.chk_print = 0

        # ====== Title ======
        self.title = ctk.CTkLabel(self.root, text="Summary", font=("Brush Script MT", 50))
        self.title.pack(side=TOP, fill=X)

        # ===== Style =====
        style = ttk.Style(self.root)

        fontStyle = ('Bell Gothic Std Black', 19)

        # Frame for border
        self.net_border = ctk.CTkFrame(self.root, border_width=2, border_color="#009688")
        self.lblPriceByLoc = ctk.CTkLabel(self.net_border, text="Inventory Cost\n 0 ",
                                          font=(fontStyle))
        self.lblPriceByLoc.place(x=3, y=3, height=100, width=220)
        self.net_border.place(x=10, y=90, height=106, width=226)

        self.sales_border = ctk.CTkFrame(self.root, border_width=2, border_color="#009688")
        self.totalSales = ctk.CTkLabel(self.sales_border, text="Total Sales\n 0 ", font=(fontStyle))
        self.totalSales.place(x=3, y=3, height=100, width=220)
        self.sales_border.place(x=250, y=90, height=106, width=226)

        self.totalCostPriceBorder = ctk.CTkFrame(self.root, border_width=2, border_color="#009688")
        self.lblTotalCostPrice = ctk.CTkLabel(self.totalCostPriceBorder, text="Total Cost Price\n 0 ",
                                              font=(fontStyle))
        self.lblTotalCostPrice.place(x=3, y=3, height=100, width=220)
        self.totalCostPriceBorder.place(x=490, y=90, height=106, width=226)

        self.lblMinus = ctk.CTkLabel(self.root, text="-", anchor='center',
                                     font=(fontStyle))
        self.lblMinus.place(x=700, y=120, height=40, width=70)

        self.totalSalesPriceBorder = ctk.CTkFrame(self.root, border_width=2, border_color="#009688")
        self.lblTotalSalesPrice = ctk.CTkLabel(self.totalSalesPriceBorder, text="Total Sales Price\n 0 ",
                                               font=(fontStyle))
        self.lblTotalSalesPrice.place(x=3, y=3, height=100, width=220)
        self.totalSalesPriceBorder.place(x=800, y=90, height=106, width=226)

        self.lblEquals = ctk.CTkLabel(self.root, text="=", anchor='center',
                                      font=(fontStyle))
        self.lblEquals.place(x=1010, y=120, height=40, width=70)

        self.profit_border = ctk.CTkFrame(self.root, border_width=2, border_color="#009688")
        self.lblProfit = ctk.CTkLabel(self.profit_border, text="Profit\n 0 ",
                                      font=(fontStyle))
        self.lblProfit.place(x=3, y=3, height=100, width=220)
        self.profit_border.place(x=1100, y=90, height=106, width=226)

        # ===== Product Search Frame =====
        ProductFrame2 = ctk.CTkFrame(self.root, border_color="#979da2", border_width=2)
        ProductFrame2.place(x=10, y=210, width=380, height=500)

        lbl_search = ctk.CTkLabel(ProductFrame2, text="Search By Name And Date",
                                  font=("Bell Gothic Std Black", 18, "bold")).place(x=40, y=5)

        divider = ctk.CTkLabel(ProductFrame2, bg_color="#000")
        divider.place(x=0, y=35, relwidth=1, height=1)

        self.lbl_status = ctk.CTkLabel(ProductFrame2, text="Select Category",
                                       font=("Bell Gothic Std Black", 17, "bold"))
        self.lbl_status.place(x=20, y=40)

        cmbStatus = ctk.CTkOptionMenu(ProductFrame2, variable=self.searchOption, font=("Bell Gothic Std Black", 17),
                                      dynamic_resizing=True,
                                      values=(
                                          "Select", "Sales", "Credit Customers Details", "Returned Orders",
                                          "Cust Payment Details",
                                          "Shop Expenses")
                                      , dropdown_fg_color="#fff", dropdown_hover_color="light blue",
                                      dropdown_text_color="#000", state="readonly", text_color="#fff")
        cmbStatus.place(x=20, y=75, width=300, height=38)

        lbl_search_name = ctk.CTkLabel(ProductFrame2, text="Name", font=("Bell Gothic Std Black", 17, "bold")).place(
            x=20, y=120)
        txt_search_name = ctk.CTkEntry(ProductFrame2, textvariable=self.search_txt, font=("Bell Gothic Std Black", 17))
        txt_search_name.place(x=20, y=155, width=300, height=38)
        txt_search_name.focus()

        lbl_search_date = ctk.CTkLabel(ProductFrame2, text="From", font=("Bell Gothic Std Black", 17))
        lbl_search_date.place(x=20, y=195)
        self.cal = DateEntry(ProductFrame2, selectmode='day', background="#242424", disabledbackground="#242424",
                             bordercolor="#242424", font=("Bell Gothic Std Black", 15),
                             headersbackground="#242424", normalbackground="#242424", foreground='white',
                             normalforeground='white', headersforeground='white', state='readonly')
        self.cal.place(x=25, y=285, width=200, height=30)

        lbl_search_date1 = ctk.CTkLabel(ProductFrame2, text="To", font=("Bell Gothic Std Black", 17))
        lbl_search_date1.place(x=20, y=260)
        self.cal1 = DateEntry(ProductFrame2, selectmode='day', background="#242424", disabledbackground="#242424",
                              bordercolor="#242424", font=("Bell Gothic Std Black", 15),
                              headersbackground="#242424", normalbackground="#242424", foreground='white',
                              normalforeground='white', headersforeground='white', state='readonly')
        self.cal1.place(x=25, y=365, width=200, height=30)

        # ====== Buttons ======

        self.printIcon = ctk.CTkImage(Image.open("images/print.png"), size=(25, 25))
        self.btnPrint = ctk.CTkButton(ProductFrame2, text="Print", image=self.printIcon, compound=RIGHT,
                                      font=("Bell Gothic Std Black", 17), command=self.print_bill,
                                      cursor="hand2", corner_radius=5)
        self.btnPrint.place(relx=0.085, rely=0.87, width=100, height=40)

        self.searchIcon = ctk.CTkImage(Image.open("images/search.png"), size=(25, 25))
        btn_search = ctk.CTkButton(ProductFrame2, text="Search", image=self.searchIcon, compound=RIGHT,
                                   font=("Bell Gothic Std Black", 17), corner_radius=5,
                                   command=lambda: [self.searchData(), self.update_content()], cursor="hand2")
        btn_search.place(relx=0.36, rely=0.87, width=120, height=40)

        self.clearIcon = ctk.CTkImage(Image.open("images/clear.png"), size=(25, 25))
        btn_clear = ctk.CTkButton(ProductFrame2, text="Clear", image=self.clearIcon, compound=RIGHT,
                                  font=("Bell Gothic Std Black", 17), cursor="hand2", corner_radius=5)
        btn_clear.place(relx=0.69, rely=0.87, width=100, height=40)
        btn_clear.bind("<Return>", self.clearData)
        btn_clear.bind("<ButtonRelease-1>", self.clearData)

        # ====== Sales Frame ======
        self.salesFrame = ctk.CTkFrame(self.root)

        style.configure("Treeview", background="#ebebeb", foreground="black", fieldbackground="#ebebeb", rowheight=30,
                        font=("Bell Gothic Std Black", 18))
        style.map("Treeview", background=[("selected", "#333333")])
        style.configure("Treeview.Heading", font=('Bell Gothic Std Black', 18))
        style.layout("Treeview",
                     [('Treeview.treearea', {'sticky': 'nswe'})])  # Remove the borders

        self.salesTable = ttk.Treeview(self.salesFrame, style="Treeview", columns=(
            "orderId", "orderItemName", "perItemPrice", "orderQty", "orderTotalPrice", "orderDiscount",
            "orderNetPrice", "orderPayType", "orderCustomerName", "orderCustomerPhone", "orderDate", "orderTime"))
        for column in self.salesTable["columns"]:
            self.salesTable.column(column, anchor=CENTER)

        scrolly = ctk.CTkScrollbar(self.salesFrame, orientation=VERTICAL, command=self.salesTable.yview)
        scrolly.pack(side=RIGHT, fill=Y)
        self.salesTable.configure(yscrollcommand=scrolly.set)

        scrollx = ctk.CTkScrollbar(self.salesFrame, orientation=HORIZONTAL, command=self.salesTable.xview)
        scrollx.pack(side=BOTTOM, fill=X)
        self.salesTable.configure(xscrollcommand=scrollx.set)

        self.salesTable.heading("orderId", text="Order ID")
        self.salesTable.heading("orderItemName", text="Name")
        self.salesTable.heading("perItemPrice", text="Item Price")
        self.salesTable.heading("orderQty", text="Quantity")
        self.salesTable.heading("orderTotalPrice", text="Total Price")
        self.salesTable.heading("orderDiscount", text="Discount")
        self.salesTable.heading("orderNetPrice", text="Net Pay")
        self.salesTable.heading("orderPayType", text="Pay Type")
        self.salesTable.heading("orderCustomerName", text="Customer Name")
        self.salesTable.heading("orderCustomerPhone", text="Phone No.")
        self.salesTable.heading("orderDate", text="Order Date")
        self.salesTable.heading("orderTime", text="Order Time")

        self.salesTable["show"] = "headings"

        self.salesTable.column("orderId", width=150, minwidth=150)
        self.salesTable.column("orderItemName", width=250, minwidth=250)
        self.salesTable.column("perItemPrice", width=250, minwidth=250)
        self.salesTable.column("orderQty", width=200, minwidth=200)
        self.salesTable.column("orderTotalPrice", width=250, minwidth=250)
        self.salesTable.column("orderDiscount", width=150, minwidth=150)
        self.salesTable.column("orderNetPrice", width=250, minwidth=250)
        self.salesTable.column("orderPayType", width=250, minwidth=250)
        self.salesTable.column("orderCustomerName", width=250, minwidth=250)
        self.salesTable.column("orderCustomerPhone", width=220, minwidth=220)
        self.salesTable.column("orderDate", width=170, minwidth=170)
        self.salesTable.column("orderTime", width=170, minwidth=170)

        # ====== Customers Details Frame ======
        self.custDetailsFrame = ctk.CTkFrame(self.root)

        style.configure("Treeview", background="#ebebeb", foreground="black", fieldbackground="#ebebeb", rowheight=30,
                        font=("Bell Gothic Std Black", 18))
        style.map("Treeview", background=[("selected", "#333333")])
        style.configure("Treeview.Heading", font=('Bell Gothic Std Black', 18))
        style.layout("Treeview",
                     [('Treeview.treearea', {'sticky': 'nswe'})])  # Remove the borders

        self.custDetailsTable = ttk.Treeview(self.custDetailsFrame, style="Treeview", columns=(
            "custId", "custName", "custBalance", "custStatus"))
        for column in self.custDetailsTable["columns"]:
            self.custDetailsTable.column(column, anchor=CENTER)

        scrolly = ctk.CTkScrollbar(self.custDetailsFrame, orientation=VERTICAL, command=self.custDetailsTable.yview)
        scrolly.pack(side=RIGHT, fill=Y)
        self.custDetailsTable.configure(yscrollcommand=scrolly.set)

        scrollx = ctk.CTkScrollbar(self.custDetailsFrame, orientation=HORIZONTAL, command=self.custDetailsTable.xview)
        scrollx.pack(side=BOTTOM, fill=X)
        self.custDetailsTable.configure(xscrollcommand=scrollx.set)

        self.custDetailsTable.heading("custId", text="Order ID")
        self.custDetailsTable.heading("custName", text="Product Name")
        self.custDetailsTable.heading("custBalance", text="Item Price")
        self.custDetailsTable.heading("custStatus", text="Quantity")

        self.custDetailsTable["show"] = "headings"

        self.custDetailsTable.column("custId", width=100, minwidth=100)
        self.custDetailsTable.column("custName", width=200, minwidth=200)
        self.custDetailsTable.column("custBalance", width=200, minwidth=200)
        self.custDetailsTable.column("custStatus", width=130, minwidth=130)

        # ====== Sales Frame ======
        self.returnedOrdersFrame = ctk.CTkFrame(self.root)

        style.configure("Treeview", background="#ebebeb", foreground="black", fieldbackground="#ebebeb", rowheight=30,
                        font=("Bell Gothic Std Black", 18))
        style.map("Treeview", background=[("selected", "#333333")])
        style.configure("Treeview.Heading", font=('Bell Gothic Std Black', 18))
        style.layout("Treeview",
                     [('Treeview.treearea', {'sticky': 'nswe'})])  # Remove the borders

        self.returnedOrdersTable = ttk.Treeview(self.returnedOrdersFrame, style="Treeview", columns=(
            "orderId", "orderItemName", "perItemPrice", "orderQty", "orderTotalPrice", "orderStatus", "orderDiscount",
            "orderNetPrice", "orderPayType", "orderCustomerName", "orderCustomerPhone", "orderDate"))
        for column in self.returnedOrdersTable["columns"]:
            self.returnedOrdersTable.column(column, anchor=CENTER)

        scrolly = ctk.CTkScrollbar(self.returnedOrdersFrame, orientation=VERTICAL,
                                   command=self.returnedOrdersTable.yview)
        scrolly.pack(side=RIGHT, fill=Y)
        self.returnedOrdersTable.configure(yscrollcommand=scrolly.set)

        scrollx = ctk.CTkScrollbar(self.returnedOrdersFrame, orientation=HORIZONTAL,
                                   command=self.returnedOrdersTable.xview)
        scrollx.pack(side=BOTTOM, fill=X)
        self.returnedOrdersTable.configure(xscrollcommand=scrollx.set)

        self.returnedOrdersTable.heading("orderId", text="Order ID")
        self.returnedOrdersTable.heading("orderItemName", text="Name")
        self.returnedOrdersTable.heading("perItemPrice", text="Item Price")
        self.returnedOrdersTable.heading("orderQty", text="Quantity")
        self.returnedOrdersTable.heading("orderTotalPrice", text="Total Price")
        self.returnedOrdersTable.heading("orderStatus", text="Order Status")
        self.returnedOrdersTable.heading("orderDiscount", text="Discount")
        self.returnedOrdersTable.heading("orderNetPrice", text="Net Payment")
        self.returnedOrdersTable.heading("orderPayType", text="Payment Type")
        self.returnedOrdersTable.heading("orderCustomerName", text="Customer Name")
        self.returnedOrdersTable.heading("orderCustomerPhone", text="Phone No.")
        self.returnedOrdersTable.heading("orderDate", text="Order Date")

        self.returnedOrdersTable["show"] = "headings"

        self.returnedOrdersTable.column("orderId", width=100, minwidth=100)
        self.returnedOrdersTable.column("orderItemName", width=200, minwidth=200)
        self.returnedOrdersTable.column("perItemPrice", width=200, minwidth=200)
        self.returnedOrdersTable.column("orderQty", width=130, minwidth=130)
        self.returnedOrdersTable.column("orderTotalPrice", width=200, minwidth=200)
        self.returnedOrdersTable.column("orderStatus", width=170, minwidth=170)
        self.returnedOrdersTable.column("orderDiscount", width=130, minwidth=130)
        self.returnedOrdersTable.column("orderNetPrice", width=200, minwidth=200)
        self.returnedOrdersTable.column("orderPayType", width=150, minwidth=150)
        self.returnedOrdersTable.column("orderCustomerName", width=200, minwidth=200)
        self.returnedOrdersTable.column("orderCustomerPhone", width=160, minwidth=160)
        self.returnedOrdersTable.column("orderDate", width=170, minwidth=170)

        if self.searchOption.get() != "Select":
            self.update_content()

        self.showAll()

    def fetch_cat_loc(self):
        try:
            self.loc_list.append("Empty")

            con = sqlite3.connect(database=r'std.db')
            cur = con.cursor()

            cur.execute("SELECT name FROM locations")
            loc = cur.fetchall()
            if len(loc) > 0:
                del self.loc_list[:]
                self.loc_list.append("Select")
                for i in loc:
                    self.loc_list.append(i[0])

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def searchData(self):
        try:
            con = sqlite3.connect(database=r'std.db')
            cur = con.cursor()

            dt = self.cal.get_date()
            date1 = str(dt.strftime("%d/%m/%Y"))

            dt1 = self.cal1.get_date()
            date2 = str(dt1.strftime("%d/%m/%Y"))

            self.chk_print = 1

            # When search by sales is selected It will search through orderItemName by orderDate
            if self.searchOption.get() == "Sales":
                self.custDetailsFrame.place_forget()
                self.custDetailsTable.pack_forget()
                self.returnedOrdersFrame.place_forget()
                self.returnedOrdersTable.pack_forget()
                self.salesFrame.place(x=320, y=212, width=1500, height=500)
                self.salesTable.pack(fill=BOTH, expand=1)
                cur.execute(
                    "SELECT orderId, orderItemName, perItemPrice, orderQty, orderTotalPrice, orderDiscount, "
                    "orderNetPrice, orderPayType, orderCustomerName, orderCustomerPhone, orderDate, orderTime "
                    "FROM orders WHERE orderItemName LIKE '%" + self.search_txt.get() + "%' AND orderDate BETWEEN ? AND ?",
                    (date1, date2))
                fetch = cur.fetchall()
                if len(fetch) != 0:
                    self.update1(fetch)
                    con.close()
                else:
                    messagebox.showerror("Error", "No record found!!!", parent=self.root)

            # When search by customer name is selected It will search through orderCustomerName by orderDate
            elif self.searchOption.get() == "Credit Customers Details":
                self.salesFrame.place_forget()
                self.salesTable.pack_forget()
                self.returnedOrdersFrame.place_forget()
                self.returnedOrdersTable.pack_forget()
                self.custDetailsFrame.place(x=320, y=212, width=1500, height=700)
                self.custDetailsTable.pack(fill=BOTH, expand=1)
                cur.execute("SELECT * FROM customersDetails WHERE (? = '' OR custName LIKE ?)",
                            (self.search_txt.get(), '%' + self.search_txt.get() + '%'))
                fetch = cur.fetchall()
                if len(fetch) != 0:
                    self.update1(fetch)
                    con.close()
                else:
                    messagebox.showerror("Error", "No record found!!!", parent=self.root)

            # When search by Credited Info is selected. It will search through orderCustomerName and orderPayType by orderDate to show user the credit info
            elif self.searchOption.get() == "Returned Orders":
                self.custDetailsFrame.place_forget()
                self.custDetailsTable.pack_forget()
                self.salesFrame.place_forget()
                self.salesTable.pack_forget()
                self.returnedOrdersFrame.place(x=320, y=212, width=1500, height=700)
                self.returnedOrdersTable.pack(fill=BOTH, expand=1)
                cur.execute(
                    "SELECT * FROM returnedOrders WHERE (? = '' OR orderItemName LIKE ? AND orderDate BETWEEN ? AND ?)",
                    (self.search_txt.get(), '%' + self.search_txt.get() + '%', date1, date2))
                fetch = cur.fetchall()
                if len(fetch) != 0:
                    self.update1(fetch)
                    con.close()
                else:
                    messagebox.showerror("Error", "No record found!!!", parent=self.root)

            elif self.searchOption.get() == "Cust Payment Details":
                cur.execute(
                    "SELECT * FROM custPaymentDetails WHERE custPayDate BETWEEN ? AND ?", (date1, date2))
                fetch = cur.fetchall()
                if len(fetch) != 0:
                    self.update1(fetch)
                    con.close()
                else:
                    messagebox.showerror("Error", "No record found!!!", parent=self.root)

            elif self.searchOption.get() == "Shop Expenses":
                cur.execute(
                    "SELECT * FROM shopExpenses WHERE expId LIKE '%" + self.search_txt.get() + "%' OR expDate BETWEEN ? AND ?",
                    (date1, date2))
                fetch = cur.fetchall()
                if len(fetch) != 0:
                    self.update1(fetch)
                    con.close()
                else:
                    messagebox.showerror("Error", "No record found!!!", parent=self.root)

            else:
                messagebox.showerror("Error", "Please select category", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def clearData(self, e):
        try:
            self.search_txt.set("")
            self.searchOption.set("Select")
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def showAll(self):
        try:
            con = sqlite3.connect(database=r'std.db')
            cur = con.cursor()

            cur.execute(
                "SELECT orderId, orderItemName, perItemPrice, orderQty, orderTotalPrice, orderDiscount, orderNetPrice, orderPayType, orderCustomerName, orderCustomerPhone, orderDate, orderTime FROM orders ORDER BY orderId DESC")
            fetch = cur.fetchall()
            self.update1(fetch)

            current_month = datetime.datetime.now().strftime('%m')
            current_year = datetime.datetime.now().strftime('%Y')

            cur.execute("SELECT orderID FROM orders WHERE orderDate LIKE ?",
                        (f"%{current_month}/{current_year}%",))
            sales = cur.fetchall()
            number_of_orders = len(sales)

            cur.execute("SELECT SUM(orderTotalPrice) FROM orders WHERE orderDate LIKE ?",
                        (f"%{current_month}/{current_year}%",))
            totalSalesPrice = cur.fetchone()
            totalSalesPrice = float(totalSalesPrice[0]) if totalSalesPrice[0] is not None else 0.0

            cur.execute("SELECT SUM(totalPrice) FROM product")
            totalCostPrice = cur.fetchone()
            totalCostPrice = float(totalCostPrice[0]) if totalCostPrice[0] is not None else 0.0

            cur.execute("SELECT SUM(orderNetPrice) FROM orders WHERE orderDate LIKE ?",
                        (f"%{current_month}/{current_year}%",))
            orderNetPrice = cur.fetchone()
            orderNetPrice = float(orderNetPrice[0]) if orderNetPrice[0] is not None else 0.0

            profit = totalSalesPrice - totalCostPrice

            self.lblPriceByLoc.configure(text=f"Inventory Cost\n Rs.{totalCostPrice}")

            if number_of_orders < int(50):
                self.sales_border.configure(border_color='red')
                self.totalSales.configure(text=f"Total Sales\n {number_of_orders}\n {totalSalesPrice} ")
            else:
                self.totalSales.configure(text=f"Total Sales\n {number_of_orders}\n {totalSalesPrice}")

            self.lblTotalCostPrice.configure(text=f"Total Cost Price\n Rs. {totalCostPrice}")

            self.lblTotalSalesPrice.configure(text=f"Total Sales Price\n Rs. {totalSalesPrice}")

            if profit < float(0.0):
                self.profit_border.configure(border_color='red')
                self.lblProfit.configure(text=f"Loss\n Rs. {str(profit)}")
            else:
                self.lblProfit.configure(text=f"Profit\n Rs. {str(profit)}")

            con.close()

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def update1(self, fetch):
        if self.searchOption.get() == "Sales":
            self.salesTable.delete(*self.salesTable.get_children())
            for data in fetch:
                self.salesTable.insert('', 'end', values=(data))
        elif self.searchOption.get() == "Credit Customers Details":
            self.custDetailsTable.delete(*self.custDetailsTable.get_children())
            for data in fetch:
                self.custDetailsTable.insert('', 'end', values=(data))
        elif self.searchOption.get() == "Returned Orders":
            self.returnedOrdersTable.delete(*self.returnedOrdersTable.get_children())
            for data in fetch:
                self.returnedOrdersTable.insert('', 'end', values=(data))

    def update_content(self):
        try:
            conn = sqlite3.connect(database=r'std.db')
            cursor = conn.cursor()

            dt = self.cal.get_date()
            date1 = str(dt.strftime("%d/%m/%Y"))

            dt1 = self.cal1.get_date()
            date2 = str(dt1.strftime("%d/%m/%Y"))

            cursor.execute("SELECT SUM(orderTotalPrice) FROM orders WHERE orderDate BETWEEN ? AND ?", (date1, date2))
            totalSalesPrice = cursor.fetchone()
            totalSalesPrice = float(totalSalesPrice[0]) if totalSalesPrice[0] is not None else 0.0
            self.lblTotalSalesPrice.configure(text=f"Total Sales Price\n Rs. {totalSalesPrice}")

            cursor.execute("SELECT * FROM orders WHERE orderDate BETWEEN ? AND ?", (date1, date2))
            sales = cursor.fetchall()
            numberOfOrders = len(sales)
            if numberOfOrders < 50:
                self.sales_border.configure(border_color='red')
                self.totalSales.configure(text=f"Total Sales\n {numberOfOrders}\n {totalSalesPrice} ")
            else:
                self.totalSales.configure(text=f"Total Sales\n {numberOfOrders}\n {totalSalesPrice}")

            cursor.execute("SELECT SUM(totalPrice) FROM product")
            totalProductPrice = cursor.fetchone()
            totalProductPrice = float(totalProductPrice[0]) if totalProductPrice[0] is not None else 0.0
            self.lblPriceByLoc.configure(text=f"Inventory Cost\n Rs.{totalProductPrice}")

            cursor.execute("SELECT SUM(totalPrice) FROM product")
            totalCostPrice = cursor.fetchone()
            totalCostPrice = float(totalCostPrice[0]) if totalCostPrice[0] is not None else 0.0

            # cursor.execute(
            #     "SELECT orders.orderQty, product.price FROM orders JOIN product ON orders.pid = product.pid WHERE orderDate BETWEEN ? AND ?",
            #     (date1, date2))
            # rows = cursor.fetchall()
            # self.totalCostPrice = 0
            # for row in rows:
            #     self.totalCostPrice += row[0] * row[1]
            # self.lblTotalCostPrice.configure(text=f"Total Cost Price\n Rs. {self.totalCostPrice}")

            cursor.execute(
                "SELECT SUM(expPrice) FROM shopExpenses WHERE expDate BETWEEN ? AND ?", (date1, date2))
            expenses = cursor.fetchone()
            expenses = float(expenses[0]) if expenses[0] is not None else 0.0

            profit = totalSalesPrice - totalCostPrice
            netProfit = profit - expenses

            if netProfit < 0:
                self.profit_border.configure(border_color='red')
                self.lblProfit.configure(text=f"Loss\n Rs. {netProfit}")
            else:
                self.lblProfit.configure(text=f"Profit\n Rs. {netProfit}")

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    # def print_bill(self):
    #     try:
    #         if self.chk_print == 1 and self.searchOption.get() == "Sales":
    #             messagebox.showinfo('Print', "Please wait while printing", parent=self.root)
    #             new_file = tempfile.mktemp('.txt')
    #             open(new_file, 'w').write(self.salesTable.get_children())
    #             os.startfile(new_file, 'print')
    #         elif self.chk_print == 1 and self.searchOption.get() == "Credit Customers Details":
    #             messagebox.showinfo('Print', "Please wait while printing", parent=self.root)
    #             new_file = tempfile.mktemp('.txt')
    #             open(new_file, 'w').write(self.custDetailsTable.get_children())
    #             os.startfile(new_file, 'print')
    #         elif self.chk_print == 1 and self.searchOption.get() == "Credit Customers Details":
    #             messagebox.showinfo('Print', "Please wait while printing", parent=self.root)
    #             new_file = tempfile.mktemp('.txt')
    #             open(new_file, 'w').write(self.returnedOrdersTable.get_children())
    #             os.startfile(new_file, 'print')
    #         else:
    #             messagebox.showinfo('Print', "Please generate bill, to print the receipt", parent=self.root)
    #
    #     except (Exception,):
    #         pass

    # def print_bill(self):
    #     try:
    #         if self.chk_print == 1:
    #             messagebox.showinfo('Print', 'Please wait while printing', parent=self.root)
    #
    #             # Choose the appropriate table based on self.searchOption.get()
    #             if self.searchOption.get() == 'Sales':
    #                 table = self.salesTable
    #             elif self.searchOption.get() == 'Credit Customers Details':
    #                 table = self.custDetailsTable
    #             elif self.searchOption.get() == 'Returned Orders':
    #                 table = self.returnedOrdersTable
    #             else:
    #                 messagebox.showinfo('Print', 'Please generate bill to print the receipt', parent=self.root)
    #                 return
    #
    #             # Get the content of the selected table
    #             table_content = []
    #             for item_id in table.get_children():
    #                 values = table.item(item_id, 'values')
    #                 table_content.append(values)
    #
    #             # Create a temporary text file and write the content including the header
    #             new_file = tempfile.mktemp('.txt')
    #             with open(new_file, 'w') as f:
    #                 # Write the header
    #                 header = [column for column in table["columns"]]
    #                 f.write(tabulate([header] + table_content, headers="firstrow", tablefmt="plain",
    #                                  colalign=("left",) * len(header)))
    #
    #             # Open the temporary text file for printing
    #             os.startfile(new_file, 'print')
    #
    #     except Exception as e:
    #         print(e)

    # def print_bill(self):
    #     try:
    #         # Create a new PDF document
    #         pdf = canvas.Canvas("invoice.pdf")
    #
    #         # Set the font and font size
    #         pdf.setFont("Helvetica", 12)
    #
    #         # Draw the invoice header
    #         pdf.drawString(50, 750, "Invoice")
    #         pdf.drawString(50, 735, "123 Main Street")
    #         pdf.drawString(50, 720, "Anytown, USA 12345")
    #         pdf.drawString(50, 705, "Phone: (555) 555-5555")
    #
    #         # Draw the invoice body
    #         pdf.drawString(250, 750, "Date: 01/01/2022")
    #         pdf.drawString(250, 735, "Invoice #: 123456")
    #         pdf.drawString(250, 720, "Customer ID: 0001")
    #
    #         # Get the column names from the Treeview
    #         columns = self.salesTable['columns']
    #
    #         # Calculate the number of columns that can fit on a page
    #         max_columns_on_page = 5
    #         num_columns = min(max_columns_on_page, len(columns))
    #
    #         # Calculate the width available for each column
    #         column_width = 525 / num_columns
    #
    #         # Draw the table headers dynamically
    #         x_position = 50
    #         for col in columns[:num_columns]:
    #             pdf.drawString(x_position, 650, col)
    #             x_position += column_width
    #
    #         # Draw the table rows from the Treeview
    #         y_position = 625
    #         for item_id in self.salesTable.get_children():
    #             values = self.salesTable.item(item_id, 'values')
    #             x_position = 50
    #             for val in values[:num_columns]:
    #                 pdf.drawString(x_position, y_position, str(val))
    #                 x_position += column_width
    #             y_position -= 25
    #
    #         # Draw the invoice footer
    #         pdf.drawString(50, 500, "Thank you for your business!")
    #
    #         # Save the PDF document
    #         pdf.save()
    #
    #         # Print the PDF document
    #         subprocess.Popen(["start", "", "invoice.pdf"], shell=True)
    #
    #     except Exception as e:
    #         print(e)

    def print_bill(self):
        try:
            pdf_filename = "invoice.pdf"
            pdf = FPDF()

            # Choose the appropriate table based on self.searchOption.get()
            if self.searchOption.get() == 'Sales':
                table = self.salesTable
            elif self.searchOption.get() == 'Credit Customers Details':
                table = self.custDetailsTable
            elif self.searchOption.get() == 'Returned Orders':
                table = self.returnedOrdersTable
            else:
                messagebox.showinfo('Print', 'Please generate a bill to print the receipt', parent=self.root)
                return

            # Get the heading names from the chosen table
            columns = [table.heading(col)['text'] for col in table['columns']]

            # Set page orientation to landscape if there are many columns
            max_columns_on_page = 5
            if len(columns) > max_columns_on_page:
                pdf.add_page(orientation='L')  # Landscape mode
            else:
                pdf.add_page(orientation='P')  # Portrait mode

            # Set font
            pdf.set_font("Arial", size=12)

            # Calculate cell width based on the number of columns
            cell_width = 280 / len(columns)  # Adjust the total width (280) based on your preference

            # Draw the invoice header
            pdf.cell(0, 10, txt="Invoice", ln=True, align='C')

            # Draw the table headings
            for col in columns:
                pdf.cell(cell_width, 10, txt=col, border=1)

            pdf.ln()  # Move to the next line

            # Get the data from the chosen table
            for item_id in table.get_children():
                values = table.item(item_id, 'values')
                for value in values:
                    pdf.cell(cell_width, 10, txt=str(value), border=1)

                pdf.ln()  # Move to the next line

            pdf.output(pdf_filename)

            # Automatically print the PDF using win32print
            printer_name = win32print.GetDefaultPrinter()
            win32api.ShellExecute(0, "print", pdf_filename, f'"{printer_name}"', ".", 0)

        except Exception as e:
            print(e)


if __name__ == "__main__":
    root = ctk.CTk()
    obj = allSummary(root)
    root.mainloop()
