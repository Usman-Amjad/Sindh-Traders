# -------Importing Modules
import sqlite3
from tkinter import *
from tkinter import ttk, messagebox
import customtkinter as ctk


class returnedItems:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x600+250+190")
        self.root.title("UA")
        # self.root.config(bg="#333333")
        self.root.focus_force()

        # ===== Style =====
        style = ttk.Style(self.root)

        ctk.set_appearance_mode("light")  # Modes: system (default), light, dark
        ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

        # ====== Icon Image ======
        icon = PhotoImage(file='images/logo.png')
        self.root.iconphoto(False, icon)

        # ================== Variables ======================
        self.var_searchby = StringVar(value="Select")
        self.var_searchtxt = StringVar()

        self.var_pid = StringVar()
        self.var_cat = StringVar()
        self.var_loc = StringVar()

        self.orderId = StringVar()
        self.var_name = StringVar()
        self.payType = StringVar()
        self.customerName = StringVar()
        self.customerPhone = StringVar()
        self.returnDate = StringVar()
        self.returnTime = StringVar()

        self.var_price = IntVar()
        self.var_qty = IntVar()
        self.totalPrice = IntVar()
        self.Discount = IntVar()
        self.NetPrice = IntVar()

        # ====== Title =======
        self.title = ctk.CTkLabel(self.root, text="Return Products", font=("Brush Script MT", 50, "bold"))
        self.title.pack(side=TOP, fill=X)

        # ===== Logo Image =====
        # self.logo = ctk.CTkImage(Image.open("images/logo.png"), size=(120, 120))
        # self.logoImage = ctk.CTkLabel(self.root, image=self.logo)
        # self.logoImage.configure(text="")
        # self.logoImage.place(x=5, y=10, width=120, height=95)

        # ==============================================================
        self.product_Frame = ctk.CTkFrame(self.root)
        self.product_Frame.place(x=10, y=100, width=450, height=482)

        fontStyle = ('Bell Gothic Std Black', 20)

        # ====== Column 1 ======
        self.lblOrderID = ctk.CTkLabel(self.product_Frame, text="Order Id", font=(fontStyle))
        self.lblOrderID.place(x=30, y=20)

        self.lblProductName = ctk.CTkLabel(self.product_Frame, text="Name", font=(fontStyle))
        self.lblProductName.place(x=30, y=70)

        self.lblPrice = ctk.CTkLabel(self.product_Frame, text="Price", font=(fontStyle))
        self.lblPrice.place(x=30, y=120)

        self.lblQty = ctk.CTkLabel(self.product_Frame, text="Quantity", font=(fontStyle))
        self.lblQty.place(x=30, y=170)

        self.lblTotalPrice = ctk.CTkLabel(self.product_Frame, text="Total Price", font=(fontStyle))
        self.lblTotalPrice.place(x=30, y=220)

        self.lblNetPrice = ctk.CTkLabel(self.product_Frame, text="Net Price", font=(fontStyle))
        self.lblNetPrice.place(x=30, y=270)
        # lblPayType = Label(product_Frame, text="Pay Type", font=(fs, 18), bg="#333333", fg='white') \
        #     .place(x=30, y=410)
        # lblCustomerName = Label(product_Frame, text="Customer Name", font=(fs, 18), bg="#333333", fg='white') \
        #     .place(x=30, y=460)
        # lblCustomerPhone = Label(product_Frame, text="Customer Phone", font=(fs, 18), bg="#333333", fg='white') \
        #     .place(x=30, y=510)
        # lblReturnDate = Label(product_Frame, text="Return Date", font=(fs, 18), bg="#333333", fg='white') \
        #     .place(x=30, y=560)
        # lblReturnTime = Label(product_Frame, text="Return Time", font=(fs, 18), bg="#333333", fg='white') \
        #     .place(x=30, y=610)

        # ====== Column 2 ======
        txtOrderID = ctk.CTkEntry(self.product_Frame, textvariable=self.orderId, font=(fontStyle))
        txtOrderID.place(x=190, y=25, width=200)

        txtName = ctk.CTkEntry(self.product_Frame, textvariable=self.var_name, font=(fontStyle))
        txtName.place(x=190, y=75, width=200)

        txtPrice = ctk.CTkEntry(self.product_Frame, textvariable=self.var_price, font=(fontStyle))
        txtPrice.place(x=190, y=125, width=200)

        txtQty = ctk.CTkEntry(self.product_Frame, textvariable=self.var_qty, font=(fontStyle))
        txtQty.place(x=190, y=175, width=200)

        txtTotalPrice = ctk.CTkEntry(self.product_Frame, textvariable=self.totalPrice, font=(fontStyle))
        txtTotalPrice.place(x=190, y=225, width=200)
        txtTotalPrice.selection_clear()

        txtNetPrice = ctk.CTkEntry(self.product_Frame, textvariable=self.NetPrice, font=(fontStyle))
        txtNetPrice.place(x=190, y=275, width=200)
        # txtPayType = Entry(product_Frame, textvariable=self.payType,
        #                    font=("goudy old style", 15), bg="light yellow").place(x=200, y=415, width=200)
        # txtCustomerName = Entry(product_Frame, textvariable=self.customerName,
        #                         font=("goudy old style", 15), bg="light yellow").place(x=200, y=465, width=200)
        # txtCustomerPhone = Entry(product_Frame, textvariable=self.customerPhone,
        #                          font=("goudy old style", 15), bg="light yellow").place(x=200, y=515, width=200)
        # txtReturnDate = Entry(product_Frame, textvariable=self.returnDate,
        #                       font=("goudy old style", 15), bg="light yellow").place(x=200, y=565, width=200)
        # txtReturnTime = Entry(product_Frame, textvariable=self.returnTime,
        #                       font=("goudy old style", 15), bg="light yellow").place(x=200, y=615, width=200)

        # ====== Buttons ======
        bs = ('Bell Gothic Std Black', 16)

        btn_return = ctk.CTkButton(self.product_Frame, text="Return", font=(bs), cursor="hand2")
        btn_return.place(x=180, y=330, width=100, height=40)
        btn_return.bind("<Return>", self.update)
        btn_return.bind("<ButtonRelease-1>", self.update)

        btn_clear = ctk.CTkButton(self.product_Frame, text="Clear", font=(bs), cursor="hand2")
        btn_clear.place(x=270, y=330, width=100, height=40)
        btn_clear.bind("<Return>", self.clear)
        btn_clear.bind("<ButtonRelease-1>", self.clear)

        # ====== Search Frame ======
        self.SearchFrame = ctk.CTkFrame(self.root)
        self.SearchFrame.place(x=480, y=90, width=600, height=80)

        cmb_search = ctk.CTkOptionMenu(self.SearchFrame, variable=self.var_searchby,
                                       values=("Select", "Bill No", "Item Name"),
                                       font=("Bell Gothic Std Black", 17), dropdown_fg_color="#fff",
                                       dropdown_hover_color="light blue",
                                       dropdown_text_color="#000", state="readonly", text_color="#fff")
        cmb_search.place(x=10, y=15, width=180)

        txt_search = ctk.CTkEntry(self.SearchFrame, textvariable=self.var_searchtxt, font=("Bell Gothic Std Black", 17))
        txt_search.place(x=180, y=15, width=200, height=35)
        txt_search.focus()

        btn_search = ctk.CTkButton(self.SearchFrame, text="Search", command=self.search,
                                   font=("Bell Gothic Std Black", 17), cursor="hand2").place(x=350, y=15, width=150,
                                                                                             height=35)

        # ====== Product Details ======
        p_Frame = ctk.CTkFrame(self.root)
        p_Frame.place(x=480, y=170, width=600, height=400)

        style.configure("Treeview", background="#ebebeb", foreground="black", fieldbackground="#ebebeb", rowheight=30,
                        font=("Bell Gothic Std Black", 18))
        style.map("Treeview", background=[("selected", "#333333")])
        style.configure("Treeview.Heading", font=('Bell Gothic Std Black', 18))
        style.layout("Treeview",
                     [('Treeview.treearea', {'sticky': 'nswe'})])  # Remove the borders

        self.product_table = ttk.Treeview(p_Frame, style="Treeview", columns=(
            "orderId", "orderItemName", "perItemPrice", "orderQty", "orderTotalPrice", "orderDiscount", "orderNetPrice",
            "orderPayType", "orderCustomerName", "orderCustomerPhone", "orderDate", "orderTime"))
        for column in self.product_table["columns"]:
            self.product_table.column(column, anchor=CENTER)

        scrolly = ctk.CTkScrollbar(p_Frame, orientation=VERTICAL, command=self.product_table.yview)
        scrolly.pack(side=RIGHT, fill=Y)
        self.product_table.configure(yscrollcommand=scrolly.set)

        scrollx = ctk.CTkScrollbar(p_Frame, orientation=HORIZONTAL, command=self.product_table.xview)
        scrollx.pack(side=BOTTOM, fill=X)
        self.product_table.configure(xscrollcommand=scrollx.set)

        self.product_table.heading("orderId", text="Id")
        self.product_table.heading("orderItemName", text="Name")
        self.product_table.heading("perItemPrice", text="Price")
        self.product_table.heading("orderQty", text="Qty")
        self.product_table.heading("orderTotalPrice", text="Total price")
        self.product_table.heading("orderDiscount", text="Discount")
        self.product_table.heading("orderNetPrice", text="Net Price")
        self.product_table.heading("orderPayType", text="Pay type")
        self.product_table.heading("orderCustomerName", text="Customer Name")
        self.product_table.heading("orderCustomerPhone", text="Customer Phone")
        self.product_table.heading("orderDate", text="Order Date")
        self.product_table.heading("orderTime", text="Order Time")

        self.product_table["show"] = "headings"

        self.product_table.column("orderId", width=150, minwidth=150)
        self.product_table.column("orderItemName", width=150, minwidth=150)
        self.product_table.column("perItemPrice", width=150, minwidth=150)
        self.product_table.column("orderQty", width=100, minwidth=100)
        self.product_table.column("orderTotalPrice", width=150, minwidth=150)
        self.product_table.column("orderDiscount", width=150, minwidth=150)
        self.product_table.column("orderNetPrice", width=150, minwidth=150)
        self.product_table.column("orderPayType", width=100, minwidth=100)
        self.product_table.column("orderCustomerName", width=200, minwidth=200)
        self.product_table.column("orderCustomerPhone", width=200, minwidth=200)
        self.product_table.column("orderDate", width=150, minwidth=150)
        self.product_table.column("orderTime", width=150, minwidth=150)

        self.product_table.pack(fill=BOTH, expand=1)
        self.product_table.bind("<ButtonRelease-1>", self.get_data)

        self.show()

        # ========================================================================================

    def get_data(self, ev):
        try:
            f = self.product_table.focus()
            content = (self.product_table.item(f))
            row = content['values']
            self.orderId.set(row[0])
            self.var_name.set(row[1])
            self.var_price.set(row[2])
            self.var_qty.set(row[3])
            self.totalPrice.set(row[4])
            self.Discount.set(row[5])
            self.NetPrice.set(row[6])
            self.payType.set(row[7])
            self.customerName.set(row[8])
            if row[9] == "":
                self.customerPhone.set("None")
            else:
                self.customerPhone.set(row[9])
            self.returnDate.set(row[10])
            self.returnTime.set(row[11])
        except (Exception,):
            pass

    def update(self, e):
        try:
            con = sqlite3.connect(database=r'std.db')
            cur = con.cursor()

            cur.execute("SELECT cid FROM orders WHERE orderId=?", (self.orderId.get(),))
            catID = cur.fetchone()
            catID = catID[0]

            cur.execute("SELECT price FROM product WHERE cid=? AND name=?", (catID, self.var_name.get()))
            buyingPrice = cur.fetchone()
            buyingPrice = buyingPrice[0]

            orderStatus = 'returned'

            total = float(buyingPrice) * float(self.var_qty.get())

            netPrice = float(total) - float(self.Discount.get())

            cur.execute("SELECT * FROM orders WHERE orderId=?", (self.orderId.get(),))
            row = cur.fetchone()
            op = messagebox.askyesno("Confirm", "Do you want to return this product?", parent=self.root)
            if self.orderId.get() == "" or row is None:
                messagebox.showerror("Error", "Invalid or Empty Order ID", parent=self.root)
            elif op is True:
                cur.execute(
                    "UPDATE product SET qty = qty + ?, totalPrice = totalPrice + ? WHERE name = ? AND cid = ?",
                    (
                        self.var_qty.get(),
                        total,
                        self.var_name.get(),
                        catID,
                    ))
                con.commit()
                cur.execute(
                    "INSERT INTO returnedOrders(orderId, orderItemName, perItemPrice, orderQty, orderTotalPrice, orderStatus, orderDiscount, orderNetPrice, orderPayType, orderCustomerName, orderCustomerPhone, orderDate, orderTime) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)",
                    (
                        self.orderId.get(),
                        self.var_name.get(),
                        self.var_price.get(),
                        self.var_qty.get(),
                        total,
                        orderStatus,
                        self.Discount.get(),
                        self.NetPrice.get(),
                        self.payType.get(),
                        self.customerName.get(),
                        self.customerPhone.get(),
                        self.returnDate.get(),
                        self.returnTime.get(),
                    ))
                con.commit()
                messagebox.showinfo("Success", "Product Updated Successfully", parent=self.root)

                cur.execute(
                    "DELETE FROM orders WHERE orderId=? AND cid=? AND orderItemName=?",
                    (self.orderId.get(), catID, self.var_name.get()))
                con.commit()

                cur.execute(
                    "UPDATE customersDetails SET custBalance = custBalance - ? WHERE custName=? ",
                    (netPrice, self.customerName.get()))
                con.commit()
                con.close()
                self.show()
                self.clear(e)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def clear(self, e):
        self.orderId.set("")
        self.var_name.set("")
        self.var_price.set("")
        self.var_qty.set("")
        self.totalPrice.set("")
        self.NetPrice.set("")
        self.var_searchtxt.set("")
        self.var_searchby.set("Select")

        self.show()

    def show(self):
        con = sqlite3.connect(database=r'std.db')
        cur = con.cursor()
        try:
            cur.execute(
                "SELECT orderId, orderItemName, perItemPrice, orderQty, orderTotalPrice, orderDiscount, orderNetPrice, orderPayType, orderCustomerName, orderCustomerPhone, orderDate, orderTime FROM orders ORDER BY orderTime DESC")
            rows = cur.fetchall()
            self.product_table.delete(*self.product_table.get_children())
            for row in rows:
                self.product_table.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def search(self):
        try:
            con = sqlite3.connect(database=r'std.db')
            cur = con.cursor()
            if self.var_searchby.get() == "Select":
                messagebox.showerror("Error", "Select Search By Option", parent=self.root)
            elif self.var_searchby.get() == "Bill No":
                cur.execute(
                    "SELECT orderId, orderItemName, perItemPrice, orderQty, orderTotalPrice, orderDiscount, orderNetPrice, orderPayType, orderCustomerName, orderCustomerPhone, orderDate, orderTime FROM orders WHERE orderId LIKE '%" + self.var_searchtxt.get() + "%'")
                rows = cur.fetchall()
                if len(rows) != 0:
                    self.product_table.delete(*self.product_table.get_children())
                    for row in rows:
                        self.product_table.insert('', END, values=row)
                else:
                    messagebox.showerror("Error", "No record found!!!", parent=self.root)
            elif self.var_searchby.get() == "Item Name":
                cur.execute(
                    "SELECT orderId, orderItemName, perItemPrice, orderQty, orderTotalPrice, orderDiscount, orderNetPrice, orderPayType, orderCustomerName, orderCustomerPhone, orderDate, orderTime FROM orders WHERE orderItemName LIKE '%" + self.var_searchtxt.get() + "%'")
                rows = cur.fetchall()
                if len(rows) != 0:
                    self.product_table.delete(*self.product_table.get_children())
                    for row in rows:
                        self.product_table.insert('', END, values=row)
                else:
                    messagebox.showerror("Error", "No record found!!!", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)


if __name__ == "__main__":
    root = ctk.CTk()
    obj = returnedItems(root)
    root.mainloop()
