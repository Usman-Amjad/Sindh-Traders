# -------Importing Modules
from tkinter import *
import customtkinter as ctk
from tkinter import ttk, messagebox
import sqlite3
import os
import tempfile
import time
from datetime import datetime
from PIL import Image


class BillClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1290x600+140+120")
        self.root.title("Sindh Traders")
        self.root.resizable(False, False)

        ctk.set_appearance_mode("light")  # Modes: system (default), light, dark
        ctk.set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green

        # ===== Style =====
        self.style = ttk.Style(self.root)

        icon = PhotoImage(file='images/logo.png')
        self.root.iconphoto(False, icon)

        # ===== Variables =====
        self.cat_list = []  # List Variable
        self.custNameList = []
        self.catIdList = []
        self.fetch_cat_loc()  # Calling Function
        self.scheme = StringVar()
        self.catId = StringVar()

        self.cart_list = []
        self.chk_print = 0

        # ====== Title =======
        self.title = ctk.CTkLabel(self.root, text="Billing Menu", font=("Brush Script MT", 50, "bold"), anchor="n")
        self.title.pack(side=TOP, fill=X)

        # ===== Logo Image =====
        # self.logo = ImageTk.PhotoImage(file="images/logoB.png")
        # self.logoImage = Label(self.root, image=self.logo).place(x=5, y=5, width=120, height=80)

        # ====== Clock ======
        self.clockFrame = ctk.CTkFrame(self.root, bg_color="#eeba2b", corner_radius=5)
        self.clockFrame.place(x=0, y=62, relwidth=1, height=30)
        self.lbl_clock = ctk.CTkLabel(self.clockFrame,
                                      text="Welcome To Stock Management System\t\t Date:DD-MM-YYYY\t\t Time: ""HH:MM:SS",
                                      font=("Bell Gothic Std Black", 15))
        self.lbl_clock.place(x=0, y=0, relwidth=1, height=30)

        # ====== Product Frame ======
        # ===== Search Variables =====
        self.var_searchby = StringVar(value="Select")
        self.var_searchtxt = StringVar()
        # # ===== Variable =====
        self.var_search = StringVar()
        self.search_cat = StringVar()

        self.ProductFrame1 = ctk.CTkFrame(self.root, border_width=2, border_color="#e6b42b")
        self.ProductFrame1.place(relx=0.001, rely=0.147, width=500, height=580)

        self.pTitle = ctk.CTkLabel(self.ProductFrame1, text="All Products", font=("Brush Script MT", 30, "bold"))
        self.pTitle.pack(side=TOP, fill=X)

        # ====== Search Frame ======
        self.ProductFrame2 = ctk.CTkFrame(self.ProductFrame1)
        self.ProductFrame2.place(relx=0.01, rely=0.08, width=490, height=100)
        self.lbl_search = ctk.CTkLabel(self.ProductFrame2, text="Search Product | By Category",
                                       font=("Bell Gothic Std Black", 15, "bold"))
        self.lbl_search.place(x=5, y=5)

        cmb_search = ctk.CTkOptionMenu(self.ProductFrame2, variable=self.var_searchby, dropdown_fg_color="#fff",
                                       dropdown_hover_color="light blue", dropdown_text_color="#000",
                                       values=("Select", "Category", "Location", "Name"), state='readonly',
                                       text_color="#fff",
                                       font=("Bell Gothic Std Black", 18))
        cmb_search.place(relx=0.01, rely=0.55, width=160, height=35)

        txt_search = ctk.CTkEntry(self.ProductFrame2, textvariable=self.var_searchtxt,
                                  font=("Bell Gothic Std Black", 20)).place(
            relx=0.365, rely=0.55, width=160, height=35)

        self.searchIcon = ctk.CTkImage(Image.open("images/search.png"), size=(25, 25))
        self.btn_search = ctk.CTkButton(self.ProductFrame2, text="Search", image=self.searchIcon, command=self.search,
                                        font=("Bell Gothic Std Black", 15), border_width=0,
                                        corner_radius=5, cursor="hand2")
        self.btn_search.place(x=280, y=44, width=130, height=35)

        # ===== Product Detail Frame =====
        self.ProductFrame3 = ctk.CTkFrame(self.ProductFrame1)
        self.ProductFrame3.place(x=2, y=120, width=495, height=390)

        self.style.configure("Treeview", background="#333333", foreground="white", fieldbackground="#333333",
                             rowheight=30,
                             font=("Arial", 17))
        self.style.map("Treeview", background=[("selected", "#0078D7")])  # added blue color when a row is selected
        self.style.configure("Treeview.Heading", font=('Bell Gothic Std Black', 20))
        self.style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])  # Remove the borders

        self.Product_Table = ttk.Treeview(self.ProductFrame3, style='Treeview', columns=(
            "cid", "pid", "category", "name", "scheme", "sellingPrice", "qty"))
        for column in self.Product_Table["columns"]:
            self.Product_Table.column(column, anchor=CENTER)

        scrolly = ctk.CTkScrollbar(self.ProductFrame3, orientation=VERTICAL, command=self.Product_Table.yview)
        scrolly.pack(side=RIGHT, fill=Y)
        self.Product_Table.configure(yscrollcommand=scrolly.set)

        scrollx = ctk.CTkScrollbar(self.ProductFrame3, orientation=HORIZONTAL, command=self.Product_Table.xview)
        scrollx.pack(side=BOTTOM, fill=X)
        self.Product_Table.configure(xscrollcommand=scrollx.set)

        self.Product_Table.heading("cid", text="CID")
        self.Product_Table.heading("pid", text="PID")
        self.Product_Table.heading("category", text="Category")
        self.Product_Table.heading("name", text="Name")
        self.Product_Table.heading("scheme", text="Scheme")
        self.Product_Table.heading("sellingPrice", text="Price")
        self.Product_Table.heading("qty", text="Quantity")

        self.Product_Table["show"] = "headings"

        self.Product_Table.column("cid", width=50)
        self.Product_Table.column("pid", width=50)
        self.Product_Table.column("category", width=150)
        self.Product_Table.column("name", width=150)
        self.Product_Table.column("scheme", width=150)
        self.Product_Table.column("sellingPrice", width=100, minwidth=100)
        self.Product_Table.column("qty", width=100)

        self.Product_Table.pack(fill=BOTH, expand=1)
        self.Product_Table.bind("<ButtonRelease-1>", self.getData)

        self.lbl_note = ctk.CTkLabel(self.ProductFrame1, text="Note: Enter 0 Quantity to remove the product from cart",
                                     font=("Bell Gothic Std Black", 14, 'bold'))
        self.lbl_note.pack(side=BOTTOM, fill=X)

        # ===== Customer Details Frame =====
        self.var_cname = StringVar(value="None")
        self.var_contact = StringVar()
        self.paymentType = StringVar(value="Select")

        self.CustomerFrame = ctk.CTkFrame(self.root, border_width=2, border_color="#e6b42b", width=500, height=70)
        self.CustomerFrame.place(relx=0.315, rely=0.147)

        self.lblPaymentType = ctk.CTkLabel(self.CustomerFrame, text="Payment Type", font=("Bell Gothic Std Black", 15))
        self.lblPaymentType.place(relx=0.01, rely=0.07)
        cmbPayType = ctk.CTkOptionMenu(self.CustomerFrame, font=("Bell Gothic Std Black", 18),
                                       variable=self.paymentType,
                                       values=["Select", "Credit", "Debit"], dropdown_fg_color="#fff",
                                       dropdown_hover_color="light blue", dropdown_text_color="#000", state='readonly',
                                       text_color="#fff")
        cmbPayType.place(relx=0.22, rely=0.09)

        self.lbl_name = ctk.CTkLabel(self.CustomerFrame, text="Name", font=("Bell Gothic Std Black", 16))
        self.lbl_name.place(relx=0.01, rely=0.5)
        cmbCustName = ctk.CTkOptionMenu(self.CustomerFrame, font=("Bell Gothic Std Black", 18), variable=self.var_cname,
                                        values=self.custNameList, dynamic_resizing=True, dropdown_fg_color="#fff",
                                        dropdown_hover_color="light blue", dropdown_text_color="#000", state='readonly',
                                        text_color="#fff")
        cmbCustName.place(relx=0.22, rely=0.55)

        self.lbl_contact = ctk.CTkLabel(self.CustomerFrame, text="Contact No.", font=("Bell Gothic Std Black", 15))
        self.lbl_contact.place(relx=0.57, rely=0.55)
        txt_contact = ctk.CTkEntry(self.CustomerFrame, textvariable=self.var_contact, width=130,
                                   font=("times new roman", 18)).place(relx=0.735, rely=0.55)

        # ===== Cal Cart Frame =====
        self.Cal_Cart_Frame = ctk.CTkFrame(self.root, border_width=2, border_color="#e6b42b", width=500, height=285)
        self.Cal_Cart_Frame.place(relx=0.315, rely=0.266)

        # ===== Calculator Frame =====
        self.var_cal_input = StringVar()

        self.Cal_Frame = Frame(self.Cal_Cart_Frame, bg="white", bd=9, relief=RIDGE)
        self.Cal_Frame.place(x=5, y=10, width=268, height=340)

        txt_cal_input = Entry(self.Cal_Frame, textvariable=self.var_cal_input, bg='#333333', fg='#333333',
                              font=("Bell Gothic Std Black", 15, "bold"), width=21, bd=8,
                              relief=GROOVE, state='readonly', justify=RIGHT)
        txt_cal_input.grid(row=0, columnspan=4)
        txt_cal_input.focus()

        btn_7 = Button(self.Cal_Frame, text="7", font=("arial", 15, "bold"), bg='#333333', fg='white',
                       command=lambda: self.get_input(7), bd=5,
                       width=4, pady=10, cursor="hand2")
        btn_7.grid(row=1, column=0)
        txt_cal_input.bind('7', lambda event: self.get_input(7))
        btn_8 = Button(self.Cal_Frame, text="8", font=("arial", 15, "bold"), bg='#333333', fg='white',
                       command=lambda: self.get_input(8), bd=5,
                       width=4, pady=10, cursor="hand2")
        btn_8.grid(row=1, column=1)
        txt_cal_input.bind('8', lambda event: self.get_input(8))
        btn_9 = Button(self.Cal_Frame, text="9", font=("arial", 15, "bold"), bg='#333333', fg='white',
                       command=lambda: self.get_input(9), bd=5,
                       width=4, pady=10, cursor="hand2")
        btn_9.grid(row=1, column=2)
        txt_cal_input.bind('9', lambda event: self.get_input(9))
        btn_sum = Button(self.Cal_Frame, text='+', font=("arial", 15, "bold"), bg='#333333', fg='white',
                         command=lambda: self.get_input('+'), bd=5,
                         width=4, pady=10, cursor="hand2")
        btn_sum.grid(row=1, column=3)
        txt_cal_input.bind('+', lambda event: self.get_input('+'))

        btn_4 = Button(self.Cal_Frame, text="4", font=("arial", 15, "bold"), bg='#333333', fg='white',
                       command=lambda: self.get_input(4), bd=5,
                       width=4, pady=10, cursor="hand2")
        btn_4.grid(row=2, column=0)
        txt_cal_input.bind('4', lambda event: self.get_input(4))
        btn_5 = Button(self.Cal_Frame, text="5", font=("arial", 15, "bold"), bg='#333333', fg='white',
                       command=lambda: self.get_input(5), bd=5,
                       width=4, pady=10, cursor="hand2")
        btn_5.grid(row=2, column=1)
        txt_cal_input.bind('5', lambda event: self.get_input(5))
        btn_6 = Button(self.Cal_Frame, text="6", font=("arial", 15, "bold"), bg='#333333', fg='white',
                       command=lambda: self.get_input(6), bd=5,
                       width=4, pady=10, cursor="hand2")
        btn_6.grid(row=2, column=2)
        txt_cal_input.bind('6', lambda event: self.get_input(6))
        btn_sub = Button(self.Cal_Frame, text='-', font=("arial", 15, "bold"), bg='#333333', fg='white',
                         command=lambda: self.get_input('-'), bd=5,
                         width=4, pady=10, cursor="hand2")
        btn_sub.grid(row=2, column=3)
        txt_cal_input.bind('-', lambda event: self.get_input('-'))

        btn_1 = Button(self.Cal_Frame, text="1", font=("arial", 15, "bold"), bg='#333333', fg='white',
                       command=lambda: self.get_input(1), bd=5,
                       width=4, pady=10, cursor="hand2")
        btn_1.grid(row=3, column=0)
        txt_cal_input.bind('1', lambda event: self.get_input(1))
        btn_2 = Button(self.Cal_Frame, text="2", font=("arial", 15, "bold"), bg='#333333', fg='white',
                       command=lambda: self.get_input(2), bd=5,
                       width=4, pady=10, cursor="hand2")
        btn_2.grid(row=3, column=1)
        txt_cal_input.bind('2', lambda event: self.get_input(2))
        btn_3 = Button(self.Cal_Frame, text="3", font=("arial", 15, "bold"), bg='#333333', fg='white',
                       command=lambda: self.get_input(3), bd=5,
                       width=4, pady=10, cursor="hand2")
        btn_3.grid(row=3, column=2)
        txt_cal_input.bind('3', lambda event: self.get_input(3))
        btn_mul = Button(self.Cal_Frame, text='x', font=("arial", 15, "bold"), bg='#333333', fg='white',
                         command=lambda: self.get_input('*'), bd=5,
                         width=4, pady=10, cursor="hand2")
        btn_mul.grid(row=3, column=3)
        txt_cal_input.bind('*', lambda event: self.get_input('*'))

        btn_0 = Button(self.Cal_Frame, text="0", font=("arial", 15, "bold"), bg='#333333', fg='white',
                       command=lambda: self.get_input(0), bd=5,
                       width=4, pady=15, cursor="hand2")
        btn_0.grid(row=4, column=0)
        txt_cal_input.bind('0', lambda event: self.get_input(0))
        btn_c = Button(self.Cal_Frame, text="c", font=("arial", 15, "bold"), bg='#333333', fg='white',
                       command=self.clear_cal, bd=5, width=4, pady=15,
                       cursor="hand2")
        btn_c.grid(row=4, column=1)
        txt_cal_input.bind('c', lambda event: self.clear_cal())
        btn_eq = Button(self.Cal_Frame, text="=", font=("arial", 15, "bold"), bg='#333333', fg='white',
                        command=self.perform_cal, bd=5, width=4,
                        pady=15, cursor="hand2")
        btn_eq.grid(row=4, column=2)
        txt_cal_input.bind('<Return>', lambda event: self.perform_cal())
        btn_div = Button(self.Cal_Frame, text='/', font=("arial", 15, "bold"), bg='#333333', fg='white',
                         command=lambda: self.get_input('/'), bd=5,
                         width=4, pady=15, cursor="hand2")
        btn_div.grid(row=4, column=3)
        txt_cal_input.bind('/', lambda event: self.get_input('/'))

        # ===== Cart Frame =====
        self.cart_Frame = ctk.CTkFrame(self.Cal_Cart_Frame)
        self.cart_Frame.place(relx=0.45, rely=0.02, width=340, height=340)

        self.cartTitle = ctk.CTkLabel(self.cart_Frame, text="Cart\t          Total Products: [0]",
                                      font=("Bell Gothic Std Black", 17))
        self.cartTitle.pack(side=TOP, fill=X)

        self.style.configure("Treeview", background="#333333", foreground="white", fieldbackground="#333333",
                             rowheight=30,
                             font=("Arial", 17))
        self.style.map("Treeview", background=[("selected", "#0078D7")])  # added blue color when a row is selected
        self.style.configure("Treeview.Heading", font=('Bell Gothic Std Black', 15))
        self.style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])  # Remove the borders

        self.CartTable = ttk.Treeview(self.cart_Frame, style='Treeview',
                                      columns=("pid", "cid", "name", "scheme", "price", "qty"))
        for column in self.CartTable["columns"]:
            self.CartTable.column(column, anchor=CENTER)

        scrolly = ctk.CTkScrollbar(self.cart_Frame, orientation=VERTICAL, command=self.CartTable.yview)
        scrolly.pack(side=RIGHT, fill=Y)
        self.CartTable.configure(yscrollcommand=scrolly.set)

        scrollx = ctk.CTkScrollbar(self.cart_Frame, orientation=HORIZONTAL, command=self.CartTable.xview)
        scrollx.pack(side=BOTTOM, fill=X)
        self.CartTable.configure(xscrollcommand=scrollx.set)

        self.CartTable.heading("pid", text="PID")
        self.CartTable.heading("cid", text="CID")
        self.CartTable.heading("name", text="Name")
        self.CartTable.heading("scheme", text="Scheme")
        self.CartTable.heading("price", text="Price")
        self.CartTable.heading("qty", text="Qty")

        self.CartTable["show"] = "headings"

        self.CartTable.column("pid", width=60, minwidth=60)
        self.CartTable.column("cid", width=60, minwidth=60)
        self.CartTable.column("name", width=150, minwidth=150)
        self.CartTable.column("scheme", width=100, minwidth=100)
        self.CartTable.column("price", width=100, minwidth=100)
        self.CartTable.column("qty", width=50, minwidth=50)

        self.CartTable.pack(fill=BOTH, expand=1)
        self.CartTable.bind("<ButtonRelease-1>", self.get_data_cart)

        # ===== Add Cart Widgets Frame =====
        self.var_pid = StringVar()
        self.var_pname = StringVar()
        self.var_price = StringVar()
        self.var_qty = StringVar()
        self.var_stock = StringVar()

        self.Add_CartWidgetsFrame = ctk.CTkFrame(self.root, border_width=2, border_color="#e6b42b", width=500,
                                                 height=104)
        self.Add_CartWidgetsFrame.place(relx=0.315, rely=0.745)

        self.lbl_p_name = ctk.CTkLabel(self.Add_CartWidgetsFrame, text="Product Name",
                                       font=("Bell Gothic Std Black", 18))
        self.lbl_p_name.place(relx=0.01, rely=0.05)
        txt_p_name = ctk.CTkEntry(self.Add_CartWidgetsFrame, textvariable=self.var_pname,
                                  font=("Bell Gothic Std Black", 17),
                                  state='readonly', width=190, height=22).place(relx=0.01, rely=0.3)

        self.lbl_p_price = ctk.CTkLabel(self.Add_CartWidgetsFrame, text="Price Per Qty",
                                        font=("Bell Gothic Std Black", 18))
        self.lbl_p_price.place(relx=0.42, rely=0.05)
        txt_p_price = ctk.CTkEntry(self.Add_CartWidgetsFrame, textvariable=self.var_price,
                                   font=("Bell Gothic Std Black", 17), width=150, height=22).place(relx=0.41, rely=0.3)

        self.lbl_p_qty = ctk.CTkLabel(self.Add_CartWidgetsFrame, text="Quantity", font=("Bell Gothic Std Black", 18))
        self.lbl_p_qty.place(relx=0.74, rely=0.05)
        self.txt_p_qty = ctk.CTkEntry(self.Add_CartWidgetsFrame, textvariable=self.var_qty,
                                      font=("Bell Gothic Std Black", 17), width=120, height=22)
        self.txt_p_qty.place(relx=0.74, rely=0.3)

        self.lbl_instock = ctk.CTkLabel(self.Add_CartWidgetsFrame, text="In Stock",
                                        font=("Bell Gothic Std Black", 15, 'bold'))
        self.lbl_instock.place(relx=0.01, rely=0.67)

        btn_clear_cart = ctk.CTkButton(self.Add_CartWidgetsFrame, text="Clear", command=self.clear_cart,
                                       font=("Bell Gothic Std Black", 17), cursor="hand2")
        btn_clear_cart.place(relx=0.45, rely=0.65, width=130, height=35)

        btn_add_cart = ctk.CTkButton(self.Add_CartWidgetsFrame, text="Add | Update Cart",
                                     font=("Bell Gothic Std Black", 17), cursor="hand2")
        btn_add_cart.place(relx=0.685, rely=0.65, width=185, height=35)
        btn_add_cart.bind("<Return>", self.add_update_cart)
        btn_add_cart.bind("<ButtonRelease-1>", self.add_update_cart)

        # ===== Billing Area =====
        self.txt_disc = IntVar()
        self.radio_var = IntVar(value=1)

        self.billFrame = ctk.CTkFrame(self.root, border_width=2, border_color="#e6b42b")
        self.billFrame.place(relx=0.707, rely=0.147, width=470, height=250)

        # self.BTitle = ctk.CTkLabel(self.billFrame, text="Customer Bill Area", font=("Brush Script MT", 30, "bold"))
        # self.BTitle.pack(side=TOP, fill=X)

        self.lbl_amnt = ctk.CTkLabel(self.billFrame, text="Bill Amount:   Rs. 0.0", font=("Bell Gothic Std Black", 20),
                                     anchor="w")
        self.lbl_amnt.place(relx=0.05, rely=0.07, width=350, height=50)

        radiobutton_1 = ctk.CTkRadioButton(self.billFrame, text="Percentage%", border_width_checked=4,
                                           radiobutton_width=15, radiobutton_height=15, variable=self.radio_var,
                                           value=1)
        radiobutton_1.place(relx=0.35, rely=0.35, width=130, height=30)
        radiobutton_2 = ctk.CTkRadioButton(self.billFrame, text="Value", border_width_checked=4,
                                           radiobutton_width=15, radiobutton_height=15, variable=self.radio_var,
                                           value=2)
        radiobutton_2.place(relx=0.35, rely=0.5, width=130, height=30)

        self.lbl_discount = ctk.CTkLabel(self.billFrame, text="Discount:  ", font=("Bell Gothic Std Black", 20))
        self.lbl_discount.place(relx=0.05, rely=0.35, width=120, height=50)
        self.txt_discount = Entry(self.billFrame, textvariable=self.txt_disc, font=("goudy old style", 20, "bold"),
                                  justify='center')
        self.txt_discount.place(relx=0.65, rely=0.4, width=100, height=35)

        self.lbl_net_pay = ctk.CTkLabel(self.billFrame, text="Net Pay:         Rs. 0.0",
                                        font=("Bell Gothic Std Black", 20), anchor="w")
        self.lbl_net_pay.place(relx=0.05, rely=0.68, width=350, height=50)

        # ===== Billing Buttons =====
        self.billMenuFrame = ctk.CTkFrame(self.root, border_width=2, border_color="#e6b42b")
        self.billMenuFrame.place(relx=0.707, rely=0.49, width=470, height=100)

        self.clearIcon = ctk.CTkImage(Image.open("images/clear.png"), size=(25, 25))
        self.btn_clear_all = ctk.CTkButton(self.billMenuFrame, text="Clear All", compound=RIGHT,
                                           font=("Bell Gothic Std Black", 15, 'bold'), image=self.clearIcon,
                                           command=self.clear_all, cursor="hand2")
        self.btn_clear_all.place(relx=0.36, rely=0.5, width=130)

        self.billIcon = ctk.CTkImage(Image.open("images/bill.png"), size=(25, 25))
        self.btn_generate = ctk.CTkButton(self.billMenuFrame, text="Save Bill", compound=RIGHT,
                                          command=self.billPage,
                                          font=("Bell Gothic Std Black", 15, 'bold'), image=self.billIcon,
                                          cursor="hand2")
        self.btn_generate.place(relx=0.68, rely=0.5, width=130)

        # ===== Footer =====
        self.footer = ctk.CTkLabel(self.root,
                                   text="Sindh Distribution - Stock Management System | Developed By UA\nFor any Technical Issue contact: "
                                        "+923412800010",
                                   font=("Bell Gothic Std Black", 18))
        self.footer.pack(side=BOTTOM, fill=X)

        self.show()
        self.update_date_time()

    # ==================== All Functions ==========================================

    def fetch_cat_loc(self):
        try:
            self.catIdList.append("Empty")
            self.cat_list.append("Empty")
            self.custNameList.append("Empty")

            con = sqlite3.connect(database=r'std.db')
            cur = con.cursor()

            cur.execute("SELECT cid FROM category")
            catIdList = cur.fetchall()
            if len(catIdList) > 0:
                del self.catIdList[:]
                self.catIdList.append("Select")
                for i in catIdList:
                    self.catIdList.append(i[0])

            cur.execute("SELECT name FROM category")
            loc = cur.fetchall()
            if len(loc) > 0:
                del self.cat_list[:]
                self.cat_list.append("Select")
                for i in loc:
                    self.cat_list.append(i[0])

            cur.execute("SELECT custName FROM customersDetails WHERE custStatus='Active'")
            name = cur.fetchall()
            if len(name) > 0:
                del self.custNameList[:]
                self.custNameList.append("Select")
                for i in name:
                    self.custNameList.append(i[0])

            conn = sqlite3.connect(database=r'std.db')
            cursor = conn.cursor()

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def get_input(self, num):
        xnum = self.var_cal_input.get() + str(num)
        self.var_cal_input.set(xnum)

    def clear_cal(self):
        self.var_cal_input.set('')

    def perform_cal(self):
        result = self.var_cal_input.get()
        self.var_cal_input.set(eval(result))

    def show(self):
        conn = sqlite3.connect(database=r'std.db')
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT cid, pid, category, name, scheme, sellingPrice, qty FROM product WHERE status='Active'")
            rows = cursor.fetchall()
            self.Product_Table.delete(*self.Product_Table.get_children())
            for row in rows:
                self.Product_Table.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def search(self):
        try:
            con = sqlite3.connect(database=r'std.db')
            cur = con.cursor()
            if self.var_searchby.get() == "Select":
                messagebox.showerror("Error", "Select Search By Option", parent=self.root)
            else:
                cur.execute(
                    "SELECT * FROM product WHERE " + self.var_searchby.get() + " LIKE '%" + self.var_searchtxt.get() + "%'")
                rows = cur.fetchall()
                if len(rows) != 0:
                    self.Product_Table.delete(*self.Product_Table.get_children())
                    for row in rows:
                        self.Product_Table.insert('', END, values=row)
                else:
                    messagebox.showerror("Error", "No record found!!!", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def getData(self, ev):
        try:
            f = self.Product_Table.focus()
            content = (self.Product_Table.item(f))
            row = content['values']
            self.var_pid.set(row[1])
            self.catId.set(row[0])
            self.var_pname.set(row[3])
            self.scheme.set(row[4])
            self.var_price.set(row[5])
            self.lbl_instock.configure(text=f"In Stock [{str(row[6])}]")
            self.var_stock.set(row[6])
            self.var_qty.set('1')
            self.search_cat.set(row[2])
            self.txt_p_qty.focus()
            self.txt_p_qty.select_range(0, END)
        except (Exception,):
            pass

    def get_data_cart(self, ev):
        try:
            f = self.CartTable.focus()
            content = (self.CartTable.item(f))
            row = content['values']
            self.var_pid.set(row[0])
            self.catId.set(row[1])
            self.var_pname.set(row[2])
            self.var_price.set(row[4])
            self.var_qty.set(row[5])
            self.lbl_instock.config(text=f"In Stock [{str(row[7])}]", bg='#333333', fg='white')
            self.var_stock.set(row[7])
        except (Exception,):
            pass

    def add_update_cart(self, e):
        try:
            if self.var_pid.get() == '':
                messagebox.showerror("Error", "Please select product from the list", parent=self.root)
            elif self.var_qty.get() == '':
                messagebox.showerror("Error", "Quantity is Required", parent=self.root)
            elif float(self.var_qty.get()) > float(self.var_stock.get()):
                messagebox.showerror("Error", "Invalid Quantity", parent=self.root)
            else:
                billAmt = float(self.var_price.get()) * float(self.var_qty.get())
                price_cal = self.var_price.get()
                cart_data = [self.var_pid.get(), self.catId.get(), self.var_pname.get(), self.scheme.get(), price_cal,
                             self.var_qty.get(),
                             self.var_stock.get(), billAmt, self.search_cat.get()]

                # ===== Update Cart =====
                present = 'no'
                index_ = 0
                for row in self.cart_list:
                    if self.var_pid.get() == row[0]:
                        present = 'yes'
                        break
                    index_ += 1
                if present == 'yes':
                    op = messagebox.askyesno('Confirm',
                                             "Product already present\nDo you want to Update | Remove from the Cart List",
                                             parent=self.root)
                    if op is True:
                        if self.var_qty.get() == "0":
                            self.cart_list.pop(index_)
                        else:
                            self.cart_list[index_][5] = self.var_qty.get()
                            self.cart_list[index_][-2] = float(self.var_price.get()) * float(self.var_qty.get())
                else:
                    self.cart_list.append(cart_data)
                self.show_cart()
                self.bill_updates()
        except (Exception,):
            pass

    def bill_updates(self):
        try:
            self.bill_amnt = 0
            for row in self.cart_list:
                self.bill_amnt = self.bill_amnt + (float(row[4]) * float(row[5]))

            self.lbl_amnt.configure(text=f'Bill Amount:   Rs. {str(self.bill_amnt)}')

            self.txt_discount.bind("<KeyRelease>", lambda event: self.update_net_pay())

            self.cartTitle.configure(text=f"Cart\t          Total Products: [{str(len(self.cart_list))}]")
        except (Exception,):
            pass

    def update_net_pay(self):
        try:
            if self.radio_var.get() == 1:
                self.discount = float(self.txt_disc.get())
                self.net_pay = self.bill_amnt - (self.bill_amnt * self.discount / 100)
                self.lbl_net_pay.configure(text=f'Net Pay:         Rs. {str(self.net_pay)}')
            elif self.radio_var.get() == 2:
                self.discount = float(self.txt_disc.get())
                self.net_pay = self.bill_amnt - self.discount
                self.lbl_net_pay.configure(text=f'Net Pay:         Rs. {str(self.net_pay)}')
        except ValueError:
            # Handle non-numeric input gracefully
            self.lbl_net_pay.configure(text="Invalid input")

    def show_cart(self):
        try:
            self.CartTable.delete(*self.CartTable.get_children())
            for row in self.cart_list:
                self.CartTable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def generate_bill(self):
        self.addDate = datetime.now().strftime("%d/%m/%Y")
        self.addTime = time.strftime("%I:%M:%S")

        conn = sqlite3.connect(database=r'std.db')
        cursor = conn.cursor()

        if len(self.cart_list) == 0:
            messagebox.showerror("Error", "Please Add Product to the Cart!!!", parent=self.root)
        elif len(self.cart_list) != 0:
            if self.paymentType.get() == 'Select' and self.var_cname.get() == '':
                messagebox.showerror('Error', "Please select Payment Type OR Name", parent=self.root)
            else:
                # ===== Bill Top =====
                self.bill_top()
                # ===== Bill Middle =====
                self.bill_middle()
                # ===== Bill Bottom =====
                self.bill_bottom()

                # ===== Here order will be placed =====
                for row in self.cart_list:
                    pid = row[0]
                    cid = row[1]
                    name = row[2]
                    itemPrice = row[4]
                    itemQty = row[5]
                    totalPrice = row[7]
                    cursor.execute(
                        "INSERT INTO orders(orderId, pid, cid, orderItemName, perItemPrice, orderQty, orderTotalPrice, orderDiscount, orderNetPrice, orderPayType, orderCustomerName, orderCustomerPhone, orderDate, orderTime) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                        (
                            self.invoice,
                            pid,
                            cid,
                            name,
                            itemPrice,
                            itemQty,
                            totalPrice,
                            self.discount,
                            self.net_pay,
                            self.paymentType.get(),
                            self.var_cname.get(),
                            self.var_contact.get(),
                            self.addDate,
                            self.addTime,
                        ))
                    conn.commit()

                # ===== Here if the customer is in Credit then the data will go to customerDetails table and then =====
                # ===== In customer billing page when user pay the amount the data will go to customerPaymentDetails Page =====
                if self.paymentType.get() == 'Credit':
                    for i in self.custNameList:
                        if self.var_cname.get() == i:
                            cursor.execute(
                                "UPDATE customersDetails SET custBalance= custBalance + ? WHERE custName=?",
                                (self.net_pay, self.var_cname.get()))
                            conn.commit()
                elif self.paymentType.get() == 'Debit':  # ===== Here If the customer is in Debit then the data will go to customerPaymentDetails table directly =====
                    for i in self.custNameList:
                        if self.var_cname.get() == i:
                            cursor.execute(
                                "SELECT custId FROM customersDetails WHERE custStatus='Active' AND custName=?",
                                (self.var_cname.get(),))
                            custId = cursor.fetchone()[0]
                            remainingBalance = int(self.net_pay) - int(self.net_pay)
                            cursor.execute(
                                "INSERT INTO custPaymentDetails(custId, custName, custBalance, custPaid, custTotalBalance, custPayType, custPayDate, custStatus) VALUES(?,?,?,?,?,?,?,?)",
                                (
                                    custId,
                                    self.var_cname.get(),
                                    self.net_pay,
                                    self.net_pay,
                                    remainingBalance,
                                    "Debit",
                                    self.addDate,
                                    "Active",

                                ))
                            conn.commit()

                fp = open(f'bill/{str(self.invoice)}.txt', 'w')
                fp.write(self.txt_bill_area.get('1.0', END))
                fp.close()
                messagebox.showinfo('Saved', "Bill has been generated/Save in Backend", parent=self.root)

        self.chk_print = 1

    def bill_top(self):
        self.invoice = int(time.strftime("%H%M%S")) + int(time.strftime("%d%m%Y"))
        bill_top_temp = f'''
ST, Main Bazaar, Sanghar\t\t\t\t    Phone No. +923043786863
{str("=" * 72)}
 Customer Name: {self.var_cname.get()}
 Phone No: {self.var_contact.get()}
 Bill No. {str(self.invoice)}\t\t\tDate: {str(time.strftime("%d/%m/%Y"))}
{str("=" * 72)}
 Product Name\t\t\tScheme\t\tItem Price\t\tQty\tAmount
{str("=" * 72)} 
        '''
        self.txt_bill_area.delete('1.0', END)
        self.txt_bill_area.insert('1.0', bill_top_temp)

    def bill_bottom(self):
        try:
            if self.radio_var.get() == 1:
                self.discount = float(self.txt_disc.get())
                self.net_pay = self.bill_amnt - (self.bill_amnt * self.discount / 100)
            elif self.radio_var.get() == 2:
                self.discount = float(self.txt_disc.get())
                self.net_pay = self.bill_amnt - self.discount
            else:
                self.discount = 0
                self.net_pay = self.bill_amnt
            bill_bottom_temp = f'''
{str("=" * 72)}
 Bill Amount\t\t\t\tRs.{self.bill_amnt}
 Discount\t\t\t\tRs.{self.discount}
 Net Amount\t\t\t\tRs.{self.net_pay}
{str("=" * 72)}
{str("=" * 72)}
        '''
            self.txt_bill_area.insert(END, bill_bottom_temp)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def bill_middle(self):
        try:
            conn = sqlite3.connect(database=r'std.db')
            cursor = conn.cursor()

            self.time_1 = datetime.now().strftime("%d/%m/%Y")
            self.total_price = float(self.var_price.get()) * float(self.var_qty.get())
            if self.search_cat.get() in self.cat_list:
                for row in self.cart_list:
                    self.pid = row[0]
                    self.name = row[2]
                    qty = float(row[6]) - float(row[5])
                    if float(row[5]) == float(row[6]):
                        status = 'Inactive'
                    if float(row[5]) != float(row[6]):
                        status = 'Active'
                    price = float(row[4]) * float(row[5])
                    self.txt_bill_area.insert(END, "\n " + self.name + "\t\t\t" + self.scheme.get() + "  \t\t" + row[
                        4] + "\t\t" + row[5] + "\tRs." + str(price))

                    cursor.execute("SELECT price FROM product WHERE pid=?", (
                        self.pid,
                    ))
                    productPrice = cursor.fetchone()
                    totalPrice = float(qty) * float(productPrice[0])

                    # ===== Update Qty In Product Table =====
                    cursor.execute("UPDATE product SET qty=?, totalPrice=?, status=? WHERE pid=? AND name=?", (
                        qty,
                        totalPrice,
                        status,
                        self.pid,
                        self.name
                    ))
                    conn.commit()
                conn.close()
                self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def clear_cart(self):
        try:
            self.var_pid.set('')
            self.var_pname.set('')
            self.var_price.set('')
            self.var_qty.set('')
            self.lbl_instock.configure(text=f"In Stock")
            self.var_stock.set('')
        except (Exception,):
            pass

    def clear_all(self):
        try:
            del self.cart_list[:]
            self.paymentType.set('Select')
            self.var_searchby.set('Select')
            self.var_cal_input.set('')
            self.clear_cart()
            self.show()
            self.show_cart()
            self.txt_disc.set(0)
            self.var_cname.set('')
            self.var_contact.set('')
            self.cartTitle.configure(text=f"Cart \t Total Product: [0]")
            self.var_search.set('')
            self.chk_print = 0
        except (Exception,):
            pass

    def update_date_time(self):
        try:
            time_ = time.strftime("%I:%M:%S")
            date_ = time.strftime("%d-%m-%Y")
            self.lbl_clock.configure(
                text=f"Welcome to Stock Management System\t\t Date: {str(date_)}\t\t Time: {str(time_)}")
            self.lbl_clock.after(200, self.update_date_time)
        except (Exception,):
            pass

    def billPage(self):
        # Create a new window
        op = messagebox.askyesno("Confirm", "Do you really want to Print Bill?", parent=self.root)
        if op is True:
            self.new_window = ctk.CTkToplevel(self.root)
            self.new_window.title("Bill")
            self.new_window.geometry("1290x600+140+80")

            self.txt_bill_area = ctk.CTkTextbox(self.new_window, font=("goudy old style", 18))
            self.txt_bill_area.pack(fill=X, ipady=150)
            self.txt_bill_area.insert(END, self.txt_bill_area)

            self.printIcon = ctk.CTkImage(Image.open("images/print.png"), size=(30, 30))
            self.btnPrint = ctk.CTkButton(self.new_window, text="Print", image=self.printIcon, compound=RIGHT,
                                          font=("times new roman", 15, 'bold'), cursor="hand2")
            self.btnPrint.place(relx=0.06, rely=0.75, width=100)
            self.btnPrint.bind("<Control-p>", self.print_bill)
            self.btnPrint.bind("<ButtonRelease-1>", self.print_bill)

            self.generate_bill()
            self.new_window.focus_force()
        else:
            messagebox.showinfo('Info', "Please generate bill, to print the receipt", parent=self.root)

    def print_bill(self, e):
        try:
            if self.chk_print == 1:
                messagebox.showinfo('Print', "Please wait while printing", parent=self.root)
                new_file = tempfile.mktemp('.txt')
                open(new_file, 'w').write(self.txt_bill_area.get('1.0', END))
                os.startfile(new_file, 'print')
                self.new_window.destroy()
            else:
                messagebox.showinfo('Print', "Please generate bill, to print the receipt", parent=self.root)
        except (Exception,):
            pass


if __name__ == "__main__":
    root = ctk.CTk()
    obj = BillClass(root)
    root.mainloop()
