# -------Importing Modules
from tkinter import *
import customtkinter as ctk
import sqlite3
from tkinter import messagebox
from tkinter import ttk
import os
import tempfile
from PIL import Image
from tkcalendar import DateEntry


# import win32print


class allSummary:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1520x770+0+0")
        self.root.title("Summary")
        self.root.config(bg="#333333")
        # self.root.resizable(False, False)
        self.root.focus_force()

        ctk.set_appearance_mode("System")  # Modes: system (default), light, dark
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

        titleBg = '#333333'
        titleFg = 'white'
        titleFont = ('Agency FB', 18)

        # Frame for border
        self.net_border = ctk.CTkFrame(self.root, border_width=2, border_color="#009688")
        self.lblPriceByLoc = ctk.CTkLabel(self.net_border, text="Inventory Cost\n 0 ",
                                          font=("times new roman", 20, "bold"))
        self.lblPriceByLoc.place(x=3, y=3, height=100, width=220)
        self.net_border.place(x=10, y=90, height=106, width=226)

        self.sales_border = ctk.CTkFrame(self.root, border_width=2, border_color="#009688")
        self.totalSales = ctk.CTkLabel(self.sales_border, text="Total Sales\n 0 ", font=("times new roman", 20, "bold"))
        self.totalSales.place(x=3, y=3, height=100, width=220)
        self.sales_border.place(x=250, y=90, height=106, width=226)

        self.totalCostPriceBorder = ctk.CTkFrame(self.root, border_width=2, border_color="#009688")
        self.lblTotalCostPrice = ctk.CTkLabel(self.totalCostPriceBorder, text="Total Cost Price\n 0 ",
                                              font=("times new roman", 20, "bold"))
        self.lblTotalCostPrice.place(x=3, y=3, height=100, width=220)
        self.totalCostPriceBorder.place(x=490, y=90, height=106, width=226)

        self.lblMinus = ctk.CTkLabel(self.root, text="-", anchor='center',
                                     font=("times new roman", 20, "bold"))
        self.lblMinus.place(x=700, y=120, height=40, width=70)

        self.totalSalesPriceBorder = ctk.CTkFrame(self.root, border_width=2, border_color="#009688")
        self.lblTotalSalesPrice = ctk.CTkLabel(self.totalSalesPriceBorder, text="Total Sales Price\n 0 ",
                                               font=("times new roman", 20, "bold"))
        self.lblTotalSalesPrice.place(x=3, y=3, height=100, width=220)
        self.totalSalesPriceBorder.place(x=800, y=90, height=106, width=226)

        self.lblEquals = ctk.CTkLabel(self.root, text="=", anchor='center',
                                      font=("times new roman", 20, "bold"))
        self.lblEquals.place(x=1010, y=120, height=40, width=70)

        self.profit_border = ctk.CTkFrame(self.root, border_width=2, border_color="#009688")
        self.lblProfit = ctk.CTkLabel(self.profit_border, text="Profit\n 0 ",
                                      font=("times new roman", 20, "bold"))
        self.lblProfit.place(x=3, y=3, height=100, width=220)
        self.profit_border.place(x=1100, y=90, height=106, width=226)

        # ===== Product Search Frame =====
        ProductFrame2 = ctk.CTkFrame(self.root)
        ProductFrame2.place(x=10, y=210, width=350, height=330)

        lbl_search = ctk.CTkLabel(ProductFrame2, text="Search By Name And Date",
                                  font=("Agency FB", 20, "bold")).place(x=40, y=5)

        self.lbl_status = ctk.CTkLabel(ProductFrame2, text="Select Category", font=("Agency FB", 20, "bold"))
        self.lbl_status.place(x=20, y=40)
        cmbStatus = ctk.CTkComboBox(ProductFrame2, variable=self.searchOption,
                                    values=("Select", "Sales", "Sales by Cust.Name", "Credited Info", "Cust Payment Details", "Shop Expenses"),
                                    state='readonly',
                                    justify=CENTER, fg_color=("#333333"), text_color=("#3c3c3c"),
                                    font=("Agency FB", 17))
        cmbStatus.place(x=140, y=45, width=150)

        lbl_search_name = ctk.CTkLabel(ProductFrame2, text="Name", font=("Agency FB", 20, "bold")).place(x=20, y=85)
        txt_search_name = ctk.CTkEntry(ProductFrame2, textvariable=self.search_txt, font=("times new roman", 18))
        txt_search_name.place(x=140, y=90, width=150, height=35)
        txt_search_name.focus()

        lbl_search_date = ctk.CTkLabel(ProductFrame2, text="From", font=("Agency FB", 20, "bold"))
        lbl_search_date.place(x=20, y=130)
        self.cal = DateEntry(ProductFrame2, selectmode='day', background="#242424", disabledbackground="#242424",
                             bordercolor="#242424", font=("Agency FB", 15, "bold"),
                             headersbackground="#242424", normalbackground="#242424", foreground='white',
                             normalforeground='white', headersforeground='white', state='readonly')
        self.cal.place(x=175, y=170, width=150, height=30)

        lbl_search_date1 = ctk.CTkLabel(ProductFrame2, text="To", font=("Agency FB", 20, "bold"))
        lbl_search_date1.place(x=20, y=170)
        self.cal1 = DateEntry(ProductFrame2, selectmode='day', background="#242424", disabledbackground="#242424",
                              bordercolor="#242424", font=("Agency FB", 15, "bold"),
                              headersbackground="#242424", normalbackground="#242424", foreground='white',
                              normalforeground='white', headersforeground='white', state='readonly')
        self.cal1.place(x=175, y=220, width=150, height=25)

        # cmb_loc = ctk.CTkComboBox(ProductFrame2, variable=self.var_loc, font=("goudy old style", 15),
        #                           values=self.loc_list, state='readonly', justify=CENTER, fg_color=("#333333"),
        #                           text_color=("#3c3c3c"))
        # cmb_loc.place(x=120, y=195, width=150)

        self.printIcon = ctk.CTkImage(Image.open("images/print.png"), size=(30, 30))
        self.btnPrint = ctk.CTkButton(ProductFrame2, text="Print", image=self.printIcon, compound=RIGHT,
                                      font=("times new roman", 15, 'bold'), command=self.print_bill, cursor="hand2")
        self.btnPrint.place(relx=0.04, rely=0.81, width=100)

        btn_search = ctk.CTkButton(ProductFrame2, text="Search", font=("goudy old style", 20),
                                   command=lambda: [self.search(), self.update_content()], cursor="hand2")
        btn_search.place(x=100, y=220, width=100, height=40)

        btn_clear = ctk.CTkButton(ProductFrame2, text="Clear", font=("goudy old style", 20), cursor="hand2")
        btn_clear.place(x=190, y=220, width=100, height=40)
        btn_clear.bind("<Return>", self.clear)
        btn_clear.bind("<ButtonRelease-1>", self.clear)

        # ====== Summary Details ======
        summaryFrame = ctk.CTkFrame(self.root)
        summaryFrame.place(x=300, y=212, width=1500, height=700)

        style.configure("Treeview", background="#3c3c3c", foreground="white", fieldbackground="#333333", rowheight=30,
                        font=("Arial", 15))
        style.map("Treeview", background=[("selected", "#0078D7")])
        style.configure("Treeview.Heading", font=('Constantia', 15))
        style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])  # Remove the borders

        scrolly = Scrollbar(summaryFrame, orient=VERTICAL)
        scrollx = Scrollbar(summaryFrame, orient=HORIZONTAL)

        self.summaryTable = ttk.Treeview(summaryFrame, style="Treeview", columns=(
            "orderId", "orderItemName", "perItemPrice", "orderQty", "orderTotalPrice", "orderDiscount",
            "orderNetPrice", "orderPayType", "orderCustomerName", "orderCustomerPhone", "orderDate", "orderTime"),
                                         yscrollcommand=scrolly.set,
                                         xscrollcommand=scrollx.set)
        for column in self.summaryTable["columns"]:
            self.summaryTable.column(column, anchor=CENTER)

        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.summaryTable.xview)
        scrolly.config(command=self.summaryTable.yview)

        self.summaryTable.heading("orderId", text="Order ID")
        self.summaryTable.heading("orderItemName", text="Product Name")
        self.summaryTable.heading("perItemPrice", text="Item Price")
        self.summaryTable.heading("orderQty", text="Quantity")
        self.summaryTable.heading("orderTotalPrice", text="Total Price")
        self.summaryTable.heading("orderDiscount", text="Discount")
        self.summaryTable.heading("orderNetPrice", text="Net Payment")
        self.summaryTable.heading("orderPayType", text="Payment Type")
        self.summaryTable.heading("orderCustomerName", text="Customer Name")
        self.summaryTable.heading("orderCustomerPhone", text="Customer Phone")
        self.summaryTable.heading("orderDate", text="Order Date")
        self.summaryTable.heading("orderTime", text="Order Time")

        self.summaryTable["show"] = "headings"

        self.summaryTable.column("orderId", width=100, minwidth=100)
        self.summaryTable.column("orderItemName", width=140, minwidth=140)
        self.summaryTable.column("perItemPrice", width=130, minwidth=130)
        self.summaryTable.column("orderQty", width=130, minwidth=130)
        self.summaryTable.column("orderTotalPrice", width=130, minwidth=130)
        self.summaryTable.column("orderDiscount", width=130, minwidth=130)
        self.summaryTable.column("orderNetPrice", width=130, minwidth=130)
        self.summaryTable.column("orderPayType", width=150, minwidth=150)
        self.summaryTable.column("orderCustomerName", width=150, minwidth=150)
        self.summaryTable.column("orderCustomerPhone", width=160, minwidth=160)
        self.summaryTable.column("orderDate", width=130, minwidth=130)
        self.summaryTable.column("orderTime", width=130, minwidth=130)

        self.summaryTable.pack(fill=BOTH, expand=1)

        self.summaryTable.bind("<ButtonRelease-1>", self.get_data)

        if self.searchOption.get() != "Select":
            self.update_content()

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

    def get_data(self, ev):
        try:
            f = self.summaryTable.focus()
            content = (self.summaryTable.item(f))
            row = content['values']

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def clear(self, e):
        try:
            self.search_txt.set("")
            self.searchOption.set("Sales")
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def search(self):
        try:
            con = sqlite3.connect(database=r'std.db')
            cur = con.cursor()

            dt = self.cal.get_date()
            date1 = str(dt.strftime("%m/%d/%Y"))

            dt1 = self.cal1.get_date()
            date2 = str(dt1.strftime("%m/%d/%Y"))

            self.chk_print = 1

            # When search by sales is selected It will search through orderItemName by orderDate
            if self.searchOption.get() == "Sales":
                cur.execute(
                    "SELECT orderId, orderItemName, perItemPrice, orderQty, orderTotalPrice, orderDiscount, "
                    "orderNetPrice, orderPayType, orderCustomerName, orderCustomerPhone, orderDate, orderTime "
                    "FROM orders WHERE orderItemName LIKE '%" + self.search_txt.get() + "%' AND orderDate BETWEEN ? AND ?",
                    (date1, date2))
                fetch = cur.fetchall()
                if len(fetch) != 0:
                    self.update1(fetch)
                else:
                    messagebox.showerror("Error", "No record found!!!", parent=self.root)
            # When search by customer name is selected It will search through orderCustomerName by orderDate
            elif self.searchOption.get() == "Sales by Customer Name":
                cur.execute(
                    "SELECT * FROM orders WHERE orderCustomerName LIKE '%" + self.search_txt.get() + "%' AND orderDate BETWEEN ? AND ?",
                    (date1, date2))
                fetch = cur.fetchall()
                if len(fetch) != 0:
                    self.update1(fetch)
                else:
                    messagebox.showerror("Error", "No record found!!!", parent=self.root)
            # When search by Credited Info is selected. It will search through orderCustomerName and orderPayType by orderDate to show user the credit info
            elif self.searchOption.get() == "Credited Info":
                cur.execute(
                    "SELECT * FROM orders WHERE orderCustomerName LIKE '%" + self.search_txt.get() + "%' AND orderPayType='Credit' AND orderDate BETWEEN ? AND ?",
                    (date1, date2))
                fetch = cur.fetchall()
                if len(fetch) != 0:
                    self.update1(fetch)
                else:
                    messagebox.showerror("Error", "No record found!!!", parent=self.root)
            elif self.searchOption.get() == "Cust Payment Details":
                cur.execute(
                    "SELECT * FROM custPaymentDetails WHERE custPayDate BETWEEN ? AND ?", (date1, date2))
                fetch = cur.fetchall()
                if len(fetch) != 0:
                    self.update1(fetch)
                else:
                    messagebox.showerror("Error", "No record found!!!", parent=self.root)
            elif self.searchOption.get() == "Shop Expenses":
                cur.execute(
                    "SELECT * FROM shopExpenses WHERE expId LIKE '%" + self.search_txt.get() + "%' OR expDate BETWEEN ? AND ?",
                    (date1, date2))
                fetch = cur.fetchall()
                if len(fetch) != 0:
                    self.update1(fetch)
                else:
                    messagebox.showerror("Error", "No record found!!!", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def update1(self, fetch):
        self.summaryTable.delete(*self.summaryTable.get_children())
        for data in fetch:
            self.summaryTable.insert('', 'end', values=(data))

    def update_content(self):
        try:
            conn = sqlite3.connect(database=r'std.db')
            cursor = conn.cursor()

            dt = self.cal.get_date()
            date1 = str(dt.strftime("%m/%d/%Y"))

            dt1 = self.cal1.get_date()
            date2 = str(dt1.strftime("%m/%d/%Y"))

            cursor.execute("SELECT SUM(orderTotalPrice) FROM orders WHERE orderDate BETWEEN ? AND ?", (date1, date2))
            self.totalSalesPrice = cursor.fetchone()
            saarr = [str(a) for a in self.totalSalesPrice]
            self.totalSalesPrice = (", ".join(saarr))
            self.lblTotalSalesPrice.configure(text=f"Total Sales Price\n Rs. {self.totalSalesPrice}")

            cursor.execute("SELECT * FROM orders WHERE orderDate BETWEEN ? AND ?", (date1, date2))
            self.sales = cursor.fetchall()
            if len(self.sales) < int(50):
                self.sales_border.configure(border_color='red')
                self.totalSales.configure(text=f"Total Sales\n {len(self.sales)}\n {self.totalSalesPrice} ")
            else:
                self.totalSales.configure(text=f"Total Sales\n {len(self.sales)}\n {self.totalSalesPrice}")

            cursor.execute("SELECT SUM(totalPrice) FROM product")
            self.tPrice = cursor.fetchone()
            saar = [str(b) for b in self.tPrice]
            self.tPrice = (", ".join(saar))
            self.lblPriceByLoc.configure(text=f"Inventory Cost\n Rs.{self.tPrice}")

            cursor.execute("SELECT orders.orderQty, product.price FROM orders JOIN product ON orders.pid = product.pid WHERE orderDate BETWEEN ? AND ?", (date1, date2))
            rows = cursor.fetchall()
            self.totalCostPrice = 0
            for row in rows:
                self.totalCostPrice += row[0] * row[1]
            self.lblTotalCostPrice.configure(text=f"Total Cost Price\n Rs. {self.totalCostPrice}")

            # dt2 = self.cal.get_date()
            # date = str(dt2.strftime("%m%"))
            cursor.execute(
                "SELECT SUM(expPrice) FROM shopExpenses WHERE expDate BETWEEN ? AND ?", (date1, date2))
            self.expenses = cursor.fetchone()
            saaar = [str(b) for b in self.expenses]
            self.expenses = (", ".join(saaar))

            profit = float(self.totalSalesPrice) - int(self.totalCostPrice)
            netProfit = float(profit) - int(self.expenses)

            if netProfit < int(0):
                self.profit_border.configure(border_color='red')
                self.lblProfit.configure(text=f"Loss\n Rs. {netProfit}")
            else:
                self.lblProfit.configure(text=f"Profit\n Rs. {netProfit}")

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def print_bill(self):
        try:
            if self.chk_print == 1:
                messagebox.showinfo('Print', "Please wait while printing", parent=self.root)
                new_file = tempfile.mktemp('.txt')
                open(new_file, 'w').write(self.summaryTable.get_children())
                os.startfile(new_file, 'print')
            else:
                messagebox.showinfo('Print', "Please generate bill, to print the receipt", parent=self.root)
        except (Exception,):
            pass

    # def print_bill(self):
    #     if self.chk_print == 1:
    #         hPrinter = win32print.OpenPrinter("Printer_name")
    #         try:
    #             hJob = win32print.StartDocPrinter(hPrinter, 1, ("test of raw data", None, "RAW"))
    #             win32print.WritePrinter(hPrinter, self.summaryTable.get_children())
    #             win32print.EndDocPrinter(hPrinter)
    #         finally:
    #             win32print.ClosePrinter(hPrinter)


if __name__ == "__main__":
    root = ctk.CTk()
    obj = allSummary(root)
    root.mainloop()
