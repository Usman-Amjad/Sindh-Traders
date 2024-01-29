# -------Importing Modules
import sqlite3
from tkinter import *
import customtkinter as ctk
from tkinter import ttk, messagebox
import time
from datetime import datetime


class productClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1300x700+150+80")
        self.root.title("UA")
        self.root.focus_force()

        ctk.set_appearance_mode("light")  # Modes: system (default), light, dark
        ctk.set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green

        # ===== Style =====
        style = ttk.Style(self.root)

        icon = PhotoImage(file='images/logo.png')
        self.root.iconphoto(False, icon)

        # ================== Variables ======================
        self.var_searchby = StringVar(value="Select")
        self.var_searchtxt = StringVar()

        self.var_pid = StringVar()
        self.var_cat = StringVar(value="Select")
        self.var_loc = StringVar(value="Select")

        self.cat_list = []  # List Variable
        self.loc_list = []  # List Variable
        self.fetch_cat_loc()  # Calling Function

        self.var_name = StringVar()
        self.var_scheme = StringVar()
        self.var_price = StringVar()
        self.var_selling_price = StringVar()
        self.var_qty = StringVar()
        self.var_status = StringVar(value="Active")

        # ====== Title =======
        self.title = ctk.CTkLabel(self.root, text="Manage Product Details", font=("Brush Script MT", 50, "bold"),
                                  anchor="n")
        self.title.pack(side=TOP, fill=X, pady=10)

        # ============== PRODUCT FRAME =================
        self.product_Frame = ctk.CTkFrame(self.root)
        self.product_Frame.place(x=0, y=80, relwidth=1, height=325)

        fontStyle = ('Bell Gothic Std Black')

        # ====== Column 1 ======
        self.lbl_category = ctk.CTkLabel(self.product_Frame, text="Category", font=(fontStyle, 20))
        self.lbl_category.place(x=50, y=20)

        self.lbl_location = ctk.CTkLabel(self.product_Frame, text="Location", font=(fontStyle, 20))
        self.lbl_location.place(x=250, y=20)

        self.lbl_product_name = ctk.CTkLabel(self.product_Frame, text="Name", font=(fontStyle, 20))
        self.lbl_product_name.place(x=450, y=20)

        self.lbl_scheme = ctk.CTkLabel(self.product_Frame, text="Scheme", font=(fontStyle, 20))
        self.lbl_scheme.place(x=650, y=20)

        self.lbl_price = ctk.CTkLabel(self.product_Frame, text="Price", font=(fontStyle, 20))
        self.lbl_price.place(x=50, y=110)

        self.lbl_selling_price = ctk.CTkLabel(self.product_Frame, text="Selling Price", font=(fontStyle, 20))
        self.lbl_selling_price.place(x=250, y=110)

        self.lbl_qty = ctk.CTkLabel(self.product_Frame, text="Quantity", font=(fontStyle, 20))
        self.lbl_qty.place(x=450, y=110)

        self.lbl_status = ctk.CTkLabel(self.product_Frame, text="Status", font=(fontStyle, 20))
        self.lbl_status.place(x=650, y=110)

        # ====== Column 2 ======
        xAxis = 180
        cmb_cat = ctk.CTkOptionMenu(self.product_Frame, variable=self.var_cat, values=self.cat_list,
                                    dropdown_fg_color="#fff", dropdown_hover_color="light blue",
                                    dropdown_text_color="#000",
                                    font=(fontStyle, 17), text_color="#fff")
        cmb_cat.place(x=50, y=60, width=200)

        cmb_loc = ctk.CTkOptionMenu(self.product_Frame, variable=self.var_loc, values=self.loc_list,
                                    dropdown_fg_color="#fff", dropdown_hover_color="light blue",
                                    dropdown_text_color="#000",
                                    font=(fontStyle, 17), text_color="#fff")
        cmb_loc.place(x=250, y=60, width=200)

        txt_name = ctk.CTkEntry(self.product_Frame, textvariable=self.var_name,
                                font=(fontStyle, 20)).place(x=450, y=60, width=200)

        txt_scheme = ctk.CTkEntry(self.product_Frame, textvariable=self.var_scheme,
                                  font=(fontStyle, 20)).place(x=650, y=60, width=200)

        txt_price = ctk.CTkEntry(self.product_Frame, textvariable=self.var_price,
                                 font=(fontStyle, 20)).place(x=50, y=150, width=200)

        txt_selling_price = ctk.CTkEntry(self.product_Frame, textvariable=self.var_selling_price,
                                         font=(fontStyle, 20)).place(x=250, y=150, width=200)

        txt_qty = ctk.CTkEntry(self.product_Frame, textvariable=self.var_qty,
                               font=(fontStyle, 20)).place(x=450, y=150, width=200)

        cmb_status = ctk.CTkOptionMenu(self.product_Frame, variable=self.var_status, dropdown_fg_color="#fff",
                                       dropdown_hover_color="light blue", dropdown_text_color="#000",
                                       values=("Active", "Inactive"), font=(fontStyle, 20), text_color="#fff")
        cmb_status.place(x=650, y=150, width=200)

        # ====== Buttons ======
        self.btn_add = ctk.CTkButton(self.product_Frame, text="Add",
                                     font=("Bell Gothic Std Black", 18),
                                     cursor="hand2", border_width=0,
                                     corner_radius=5, text_color="#fff", anchor="center")
        self.btn_add.place(x=370, y=210, width=110, height=40)
        self.btn_add.bind("<Return>", self.add)
        self.btn_add.bind("<ButtonRelease-1>", self.add)

        self.btn_update = ctk.CTkButton(self.product_Frame, text="Update",
                                        font=("Bell Gothic Std Black", 18),
                                        cursor="hand2", border_width=0, corner_radius=5, text_color="#fff", anchor="center")
        self.btn_update.place(x=470, y=210, width=135, height=40)
        self.btn_update.bind("<Return>", self.updateData)
        self.btn_update.bind("<ButtonRelease-1>", self.updateData)

        self.btn_delete = ctk.CTkButton(self.product_Frame, text="Delete",
                                        font=("Bell Gothic Std Black", 18),
                                        cursor="hand2", border_width=0, corner_radius=5, text_color="#fff", anchor="center")
        self.btn_delete.place(x=590, y=210, width=125, height=40)
        self.btn_delete.bind("<Return>", lambda event: self.delete_selected_rows(None))
        self.btn_delete.bind("<ButtonRelease-1>", self.delete_selected_rows)

        self.btn_clear = ctk.CTkButton(self.product_Frame, text="Clear All",
                                       font=("Bell Gothic Std Black", 18),
                                       cursor="hand2", border_width=0, corner_radius=5, text_color="#fff", anchor="center")
        self.btn_clear.place(x=700, y=210, width=145, height=40)
        self.btn_clear.bind("<Return>", self.clearWidgets)
        self.btn_clear.bind("<ButtonRelease-1>", self.clearWidgets)

        # ====== Search Frame ======
        self.SearchFrame = ctk.CTkFrame(self.root)
        self.SearchFrame.place(x=0, y=340, relwidth=1, height=90)

        self.lbl_searchby = ctk.CTkLabel(self.SearchFrame, text="Search By Option", font=('Bell Gothic Std Black', 20))
        self.lbl_searchby.place(x=10, y=0)

        self.cmb_search = ctk.CTkOptionMenu(self.SearchFrame, variable=self.var_searchby, dropdown_fg_color="#fff",
                                            dropdown_hover_color="light blue", dropdown_text_color="#000",
                                            values=("Select", "Category", "Name"), font=("Bell Gothic Std Black", 20),
                                            text_color="#fff")
        self.cmb_search.place(x=10, y=35, width=180, height=35)

        self.txt_search = ctk.CTkEntry(self.SearchFrame, textvariable=self.var_searchtxt,
                                       font=("Bell Gothic Std Black", 17))
        self.txt_search.place(x=170, y=35, width=200, height=37)

        self.btn_search = ctk.CTkButton(self.SearchFrame, text='Search',
                                        font=("Bell Gothic Std Black", 20), cursor="hand2",
                                        border_width=0, text_color="#fff",
                                        corner_radius=5)
        self.btn_search.place(x=350, y=35, width=140, height=37)
        self.btn_search.bind("<Return>", self.search)
        self.btn_search.bind("<ButtonRelease-1>", self.search)

        # ====== Product Details ======
        self.p_Frame = ctk.CTkFrame(self.root, fg_color="#333333")
        self.p_Frame.pack(side=BOTTOM, fill=X, ipady=5)

        style.configure("Treeview", background="#ebebeb", foreground="black", fieldbackground="#ebebeb", rowheight=30,
                        font=("Bell Gothic Std Black", 18))
        style.map("Treeview", background=[("selected", "#333333")])
        style.configure("Treeview.Heading", font=('Bell Gothic Std Black', 18))
        style.layout("Treeview",
                     [('Treeview.treearea', {'sticky': 'nswe'})])  # Remove the borders

        self.product_table = ttk.Treeview(self.p_Frame, style="Treeview", columns=(
            "cid", "pid", "category", "name", "scheme", "price", "sellingPrice", "qty", "totalPrice", "status",
            "location"))
        for column in self.product_table["columns"]:
            self.product_table.column(column, anchor=CENTER)

        scrolly = ctk.CTkScrollbar(self.p_Frame, orientation=VERTICAL, command=self.product_table.yview)
        scrolly.pack(side=RIGHT, fill=Y)
        self.product_table.configure(yscrollcommand=scrolly.set)

        scrollx = ctk.CTkScrollbar(self.p_Frame, orientation=HORIZONTAL, command=self.product_table.xview)
        scrollx.pack(side=BOTTOM, fill=X)
        self.product_table.configure(xscrollcommand=scrollx.set)

        self.product_table.heading("cid", text="Category Id")
        self.product_table.heading("pid", text="Product Id")
        self.product_table.heading("category", text="Category")
        self.product_table.heading("name", text="Name")
        self.product_table.heading("scheme", text="Scheme")
        self.product_table.heading("price", text="Price")
        self.product_table.heading("sellingPrice", text="Selling Price")
        self.product_table.heading("qty", text="Qty")
        self.product_table.heading("totalPrice", text="Total Price")
        self.product_table.heading("status", text="Status")
        self.product_table.heading("location", text="Location")

        self.product_table["show"] = "headings"

        self.product_table.column("cid", width=140, minwidth=140)
        self.product_table.column("pid", width=140, minwidth=140)
        self.product_table.column("category", width=200, minwidth=200)
        self.product_table.column("name", width=140, minwidth=140)
        self.product_table.column("scheme", width=100, minwidth=100)
        self.product_table.column("price", width=100, minwidth=100)
        self.product_table.column("sellingPrice", width=150, minwidth=150)
        self.product_table.column("qty", width=100, minwidth=100)
        self.product_table.column("totalPrice", width=200, minwidth=200)
        self.product_table.column("status", width=100, minwidth=100)
        self.product_table.column("location", width=120, minwidth=120)

        self.product_table.pack(fill=BOTH, expand=1)
        self.product_table.bind("<ButtonRelease-1>", self.get_rows_data)

        self.showAll()

    # ========================= Functions ==============================

    def fetch_cat_loc(self):
        self.cat_list.append("Empty")
        self.loc_list.append("Empty")

        con = sqlite3.connect(database=r'std.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT name FROM category")
            cat = cur.fetchall()
            if len(cat) > 0:
                del self.cat_list[:]
                self.cat_list.append("Select")
                for i in cat:
                    self.cat_list.append(i[0])

            cur.execute("SELECT name FROM locations")
            loc = cur.fetchall()
            if len(loc) > 0:
                del self.loc_list[:]
                self.loc_list.append("Select")
                for i in loc:
                    self.loc_list.append(i[0])

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def add(self, e):
        try:
            con = sqlite3.connect(database=r'std.db')
            cur = con.cursor()

            self.addDate = datetime.now().strftime("%d/%m/%Y")
            self.addTime = time.strftime("%I:%M:%S")

            total = int(self.var_price.get()) * int(self.var_qty.get())  # Calculating Total Price

            # Get category ID from the category table based on the selected category name
            cur.execute("SELECT cid FROM category WHERE name = ?", (self.var_cat.get(),))
            catID = cur.fetchone()
            catID = int(catID[0])

            if self.var_cat.get() == "Select" or self.var_cat.get() == "Empty" or self.var_name.get() == "":
                messagebox.showerror("Error", "Category and name are required", parent=self.root)
            else:
                cur.execute("SELECT * FROM product WHERE name=? AND price=?",
                            (self.var_name.get(), self.var_price.get()))
                row = cur.fetchone()
                if row is not None:
                    op = messagebox.askyesno("Warning", "Product already present, do you really want to add more",
                                             parent=self.root)
                    if op is True:
                        # ----- Updating product if already exist
                        cur.execute(
                            "UPDATE product set qty = qty+?, totalPrice = totalPrice+? WHERE pid=? AND name=?",
                            (
                                self.var_qty.get(),
                                total,
                                self.var_pid.get(),
                                self.var_name.get(),
                            ))
                        con.commit()
                        messagebox.showinfo("Success", "More items added successfully", parent=self.root)
                        self.showAll()
                        # ---- Adding all details in productDetails Table to see the summary
                        cur.execute(
                            "INSERT INTO productDetails(category,name,scheme,price,sellingPrice,qty,totalPrice,status,location,Date,Time) values(?,?,?,?,?,?,?,?,?,?,?)",
                            (
                                self.var_cat.get(),
                                self.var_name.get(),
                                self.var_scheme.get(),
                                self.var_price.get(),
                                self.var_selling_price.get(),
                                self.var_qty.get(),
                                total,
                                self.var_status.get(),
                                self.var_loc.get(),
                                self.addDate,
                                self.addTime
                            ))
                        con.commit()
                else:  # ----- Adding Data in Product table If There is no similar data exist.
                    cur.execute(
                        "INSERT INTO product(cid,category,name,scheme,price,sellingPrice,qty,totalPrice,status,location) values(?,?,?,?,?,?,?,?,?,?)",
                        (
                            catID,
                            self.var_cat.get(),
                            self.var_name.get(),
                            self.var_scheme.get(),
                            self.var_price.get(),
                            self.var_selling_price.get(),
                            self.var_qty.get(),
                            total,
                            self.var_status.get(),
                            self.var_loc.get(),
                        ))
                    con.commit()
                    messagebox.showinfo("Success", "Product Added Successfully", parent=self.root)
                    self.showAll()
                    self.clearWidgets(e)
                    cur.execute(
                        "INSERT INTO productDetails(category,name,scheme,price,sellingPrice,qty,totalPrice,status,location,Date,Time) values(?,?,?,?,?,?,?,?,?,?,?)",
                        (
                            self.var_cat.get(),
                            self.var_name.get(),
                            self.var_scheme.get(),
                            self.var_price.get(),
                            self.var_selling_price.get(),
                            self.var_qty.get(),
                            total,
                            self.var_status.get(),
                            self.var_loc.get(),
                            self.addDate,
                            self.addTime
                        ))
                    con.commit()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def showAll(self):
        con = sqlite3.connect(database=r'std.db')
        cur = con.cursor()
        try:
            cur.execute(
                "SELECT cid,pid,category,name,scheme,price,sellingPrice,qty,totalPrice,status,location FROM product")
            rows = cur.fetchall()
            self.product_table.delete(*self.product_table.get_children())
            for row in rows:
                self.product_table.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def get_rows_data(self, ev):
        try:
            f = self.product_table.focus()
            content = (self.product_table.item(f))
            row = content['values']
            self.var_pid.set(row[1])
            self.var_cat.set(row[2])
            self.var_name.set(row[3])
            self.var_scheme.set(row[4])
            self.var_price.set(row[5])
            self.var_selling_price.set(row[6])
            self.var_qty.set(row[7])
            self.var_status.set(row[9])
            self.var_loc.set(row[10])
        except (Exception,):
            pass

    def updateData(self, e):
        try:
            con = sqlite3.connect(database=r'std.db')
            cur = con.cursor()
            cur.execute("SELECT * FROM product WHERE pid=?", (self.var_pid.get(),))
            row = cur.fetchone()

            Quant = int(self.var_qty.get()) + int(row[5])
            total = int(self.var_price.get()) * int(Quant)

            if self.var_pid.get() == "":
                messagebox.showerror("Error", "Please Select Product From List", parent=self.root)
            else:
                cur.execute("SELECT * FROM product WHERE pid=?", (self.var_pid.get(),))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Invalid Product", parent=self.root)
                else:
                    cur.execute(
                        "UPDATE product set name=?, status=? WHERE pid=?",
                        (
                            self.var_name.get(),
                            self.var_status.get(),
                            self.var_pid.get(),
                        ))
                    con.commit()
                    con.close()
                    messagebox.showinfo("Success", "Status updated successfully", parent=self.root)
                    self.showAll()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def delete_selected_rows(self, event):
        try:
            selected_items = self.product_table.selection()
            if event is None or len(selected_items) > 0:
                confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete the selected rows?")
                if confirm:
                    conn = sqlite3.connect(database='std.db')
                    cursor = conn.cursor()
                    for item in selected_items:
                        # Get data from the selected row (assuming the first column contains the unique row ID)
                        row_id = self.product_table.item(item)['values'][1]
                        cursor.execute("DELETE FROM product WHERE pid=?", (row_id,))
                    conn.commit()
                    conn.close()
                    # Refresh or update the table after deletion
                    self.showAll()  # Call your function to refresh the table
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def clearWidgets(self, e):
        self.var_cat.set("Select")
        self.var_loc.set("Select")
        self.var_name.set("")
        self.var_scheme.set("")
        self.var_price.set(0)
        self.var_selling_price.set(0)
        self.var_qty.set(0)
        self.var_status.set("Active")
        self.var_pid.set("")
        self.var_searchtxt.set("")
        self.var_searchby.set("Select")

        self.showAll()

    def search(self, e):
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
                    self.product_table.delete(*self.product_table.get_children())
                    for row in rows:
                        self.product_table.insert('', END, values=row)
                else:
                    messagebox.showerror("Error", "No record found!!!", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)


if __name__ == "__main__":
    root = ctk.CTk()
    obj = productClass(root)
    root.mainloop()
