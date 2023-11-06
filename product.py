# -------Importing Modules
import sqlite3
from tkinter import *
import customtkinter as ctk
from tkinter import ttk, messagebox
from PIL import Image
import time
from datetime import datetime


class productClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x600+220+148")
        self.root.title("UA")
        self.root.config(bg="#242424")
        self.root.focus_force()

        ctk.set_appearance_mode("System")  # Modes: system (default), light, dark
        ctk.set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green

        # ===== Style =====
        style = ttk.Style(self.root)

        icon = PhotoImage(file='images/logo.png')
        self.root.iconphoto(False, icon)

        # ================== Variables ======================
        self.var_searchby = StringVar(value="Select")
        self.var_searchtxt = StringVar()

        self.var_pid = StringVar()
        self.var_cat = StringVar()
        self.var_loc = StringVar()

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
        self.title.pack(side=TOP, fill=X)

        # ============== PRODUCT FRAME =================
        self.product_Frame = ctk.CTkFrame(self.root)
        self.product_Frame.place(x=10, y=90, width=550, height=600)

        titleFont = ('Agency FB', 25)

        # ====== Column 1 ======
        self.lbl_category = ctk.CTkLabel(self.product_Frame, text="Category", font=(titleFont))
        self.lbl_category.place(x=30, y=30)

        self.lbl_location = ctk.CTkLabel(self.product_Frame, text="Location", font=(titleFont))
        self.lbl_location.place(x=30, y=80)

        self.lbl_product_name = ctk.CTkLabel(self.product_Frame, text="Name", font=(titleFont))
        self.lbl_product_name.place(x=30, y=130)

        self.lbl_scheme = ctk.CTkLabel(self.product_Frame, text="Scheme", font=(titleFont))
        self.lbl_scheme.place(x=30, y=180)

        self.lbl_price = ctk.CTkLabel(self.product_Frame, text="Price", font=(titleFont))
        self.lbl_price.place(x=30, y=230)

        self.lbl_selling_price = ctk.CTkLabel(self.product_Frame, text="Selling Price", font=(titleFont))
        self.lbl_selling_price.place(x=30, y=280)

        self.lbl_qty = ctk.CTkLabel(self.product_Frame, text="Quantity", font=(titleFont))
        self.lbl_qty.place(x=30, y=330)

        self.lbl_status = ctk.CTkLabel(self.product_Frame, text="Status", font=(titleFont))
        self.lbl_status.place(x=30, y=380)

        # ====== Column 2 ======
        cmb_cat = ctk.CTkComboBox(self.product_Frame, variable=self.var_cat, values=self.cat_list, justify=CENTER,
                                  font=("Agency FB", 20))
        cmb_cat.place(x=150, y=32, width=200)

        cmb_loc = ctk.CTkComboBox(self.product_Frame, variable=self.var_loc, values=self.loc_list, justify=CENTER,
                                  font=("Agency FB", 20))
        cmb_loc.place(x=150, y=82, width=200)

        txt_name = ctk.CTkEntry(self.product_Frame, textvariable=self.var_name,
                                font=("goudy old style", 17)).place(x=150, y=132, width=200)

        txt_scheme = ctk.CTkEntry(self.product_Frame, textvariable=self.var_scheme,
                                  font=("goudy old style", 17)).place(x=150, y=182, width=200)

        txt_price = ctk.CTkEntry(self.product_Frame, textvariable=self.var_price,
                                 font=("goudy old style", 17)).place(x=150, y=232, width=200)

        txt_selling_price = ctk.CTkEntry(self.product_Frame, textvariable=self.var_selling_price,
                                         font=("goudy old style", 17)).place(x=150, y=282, width=200)

        txt_qty = ctk.CTkEntry(self.product_Frame, textvariable=self.var_qty,
                               font=("goudy old style", 17)).place(x=150, y=332, width=200)

        cmb_status = ctk.CTkComboBox(self.product_Frame, variable=self.var_status,
                                     values=("Active", "Inactive"), justify=CENTER, font=("Agency FB", 20))
        cmb_status.place(x=150, y=382, width=200)

        # ====== Buttons ======
        self.addIcon = ctk.CTkImage(light_image=Image.open("images/add.png"), size=(32, 32))
        self.btn_add = ctk.CTkButton(self.product_Frame, text="Add", image=self.addIcon, font=("Agency FB", 20),
                                     cursor="hand2", compound=LEFT, width=80, height=25, border_width=0,
                                     corner_radius=8)
        self.btn_add.place(x=30, y=430)
        self.btn_add.bind("<Return>", self.add)
        self.btn_add.bind("<ButtonRelease-1>", self.add)

        self.updateIcon = ctk.CTkImage(light_image=Image.open("images/update.png"), size=(32, 32))
        self.btn_update = ctk.CTkButton(self.product_Frame, text="Update", image=self.updateIcon,
                                        font=("Agency FB", 20),
                                        cursor="hand2", compound=LEFT, width=80, height=25, border_width=0,
                                        corner_radius=8)
        self.btn_update.place(x=120, y=430)
        self.btn_update.bind("<Return>", self.update)
        self.btn_update.bind("<ButtonRelease-1>", self.update)

        self.deleteIcon = ctk.CTkImage(light_image=Image.open("images/delete.png"), size=(32, 32))
        self.btn_delete = ctk.CTkButton(self.product_Frame, text="Delete", image=self.deleteIcon,
                                        font=("Agency FB", 20),
                                        cursor="hand2", compound=LEFT, width=80, height=25, border_width=0,
                                        corner_radius=8)
        self.btn_delete.place(x=225, y=430)
        self.btn_delete.bind("<Return>", self.delete)
        self.btn_delete.bind("<ButtonRelease-1>", self.delete)

        self.clearIcon = ctk.CTkImage(light_image=Image.open("images/clear.png"), size=(32, 32))
        self.btn_clear = ctk.CTkButton(self.product_Frame, text="Clear All", image=self.clearIcon,
                                       font=("Agency FB", 20),
                                       cursor="hand2", compound=LEFT, width=80, height=25, border_width=0,
                                       corner_radius=8)
        self.btn_clear.place(x=325, y=430)
        self.btn_clear.bind("<Return>", self.clear)
        self.btn_clear.bind("<ButtonRelease-1>", self.clear)

        # ====== Search Frame ======
        self.SearchFrame = ctk.CTkFrame(self.root)
        self.SearchFrame.place(x=500, y=90, width=600, height=95)

        self.lbl_searchby = ctk.CTkLabel(self.SearchFrame, text="Search By Anything", font=('Agency FB', 22))
        self.lbl_searchby.place(x=10, y=0)

        cmb_search = ctk.CTkComboBox(self.SearchFrame, variable=self.var_searchby,
                                     values=("Select", "Category", "Location", "Name"), justify=CENTER,
                                     font=("Agency FB", 20))
        cmb_search.place(x=10, y=42, width=180, height=35)

        txt_search = ctk.CTkEntry(self.SearchFrame, textvariable=self.var_searchtxt,
                                  font=("goudy old style", 17)).place(x=170, y=42, width=200, height=35)

        self.searchIcon = ctk.CTkImage(light_image=Image.open('images/search.png'))
        self.btn_search = ctk.CTkButton(self.SearchFrame, text='Search', image=self.searchIcon, command=self.search,
                                        font=("goudy old style", 20), cursor="hand2", compound=LEFT, width=80,
                                        height=20, border_width=0,
                                        corner_radius=8)
        self.btn_search.place(x=350, y=40)

        # ====== Product Details ======
        self.p_Frame = ctk.CTkFrame(self.root)
        self.p_Frame.place(x=500, y=180, width=635, height=440)

        style.configure("Treeview", background="#333333", foreground="white", fieldbackground="#333333", rowheight=30,
                        font=("Arial", 18))
        style.map("Treeview", background=[("selected", "#0078D7")])
        style.configure("Treeview.Heading", font=('Constantia', 18))
        style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])  # Remove the borders

        self.product_table = ttk.Treeview(self.p_Frame, style="Treeview", columns=(
            "pid", "category", "name", "scheme", "price", "sellingPrice", "qty", "totalPrice", "status", "location"))
        for column in self.product_table["columns"]:
            self.product_table.column(column, anchor=CENTER)

        scrolly = ctk.CTkScrollbar(self.p_Frame, orientation=VERTICAL, command=self.product_table.yview)
        scrolly.pack(side=RIGHT, fill=Y)
        self.product_table.configure(yscrollcommand=scrolly.set)

        scrollx = ctk.CTkScrollbar(self.p_Frame, orientation=HORIZONTAL, command=self.product_table.xview)
        scrollx.pack(side=BOTTOM, fill=X)
        self.product_table.configure(xscrollcommand=scrollx.set)

        self.product_table.heading("pid", text="Id")
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

        self.product_table.column("pid", width=80, minwidth=80)
        self.product_table.column("category", width=140, minwidth=140)
        self.product_table.column("name", width=140, minwidth=140)
        self.product_table.column("scheme", width=100, minwidth=100)
        self.product_table.column("price", width=100, minwidth=100)
        self.product_table.column("sellingPrice", width=140, minwidth=140)
        self.product_table.column("qty", width=100, minwidth=100)
        self.product_table.column("totalPrice", width=140, minwidth=140)
        self.product_table.column("status", width=100, minwidth=100)
        self.product_table.column("location", width=120, minwidth=120)

        self.product_table.pack(fill=BOTH, expand=1)
        self.product_table.bind("<ButtonRelease-1>", self.get_data)

        self.show()

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
            self.addDate = datetime.now().strftime("%m/%d/%Y")
            self.addTime = time.strftime("%I:%M:%S")
            total = int(self.var_price.get()) * int(self.var_qty.get())

            if self.var_cat.get() == "Select" or self.var_cat.get() == "Empty" or self.var_name.get() == "":
                messagebox.showerror("Error", "All fields are required", parent=self.root)
            else:
                cur.execute("SELECT * FROM product WHERE name=? AND price=?",
                            (self.var_name.get(), self.var_price.get()))
                row = cur.fetchone()
                if row is not None:
                    op = messagebox.askyesno("Warning", "Product already present, do you really want to add more",
                                             parent=self.root)
                    if op is True:
                        # ----- Updating row if already exist
                        cur.execute(
                            "UPDATE product set qty = qty+?, totalPrice = totalPrice+? WHERE pid=?",
                            (
                                self.var_qty.get(),
                                total,
                                self.var_pid.get(),
                            ))
                        con.commit()
                        messagebox.showinfo("Success", "More items added successfully", parent=self.root)
                        self.show()
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
                        "INSERT INTO product(category,name,scheme,price,sellingPrice,qty,totalPrice,status,location) values(?,?,?,?,?,?,?,?,?)",
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
                        ))
                    con.commit()
                    messagebox.showinfo("Success", "Product Added Successfully", parent=self.root)
                    self.show()
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

    def show(self):
        con = sqlite3.connect(database=r'std.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM product")
            rows = cur.fetchall()
            self.product_table.delete(*self.product_table.get_children())
            for row in rows:
                self.product_table.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def get_data(self, ev):
        try:
            f = self.product_table.focus()
            content = (self.product_table.item(f))
            row = content['values']
            self.var_pid.set(row[0])
            self.var_cat.set(row[1])
            self.var_name.set(row[2])
            self.var_scheme.set(row[3])
            self.var_price.set(row[4])
            self.var_selling_price.set(row[5])
            self.var_qty.set(row[6])
            self.var_status.set(row[8])
            self.var_loc.set(row[9])
        except (Exception,):
            pass

    def update(self, e):
        try:
            con = sqlite3.connect(database=r'std.db')
            cur = con.cursor()
            cur.execute("SELECT * FROM product WHERE pid=?", (self.var_pid.get(),))
            row = cur.fetchone()
            Quant = int(self.var_qty.get()) + int(row[4])
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
                        "UPDATE product set name=? status=? WHERE pid=?",
                        (
                            self.var_name.get(),
                            self.var_status.get(),
                            self.var_pid.get()
                            # self.var_cat.get(),
                            # self.var_loc.get(),
                        ))
                    con.commit()
                    con.close()
                    messagebox.showinfo("Success", "Status updated successfully", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def delete(self, e):
        con = sqlite3.connect(database=r'std.db')
        cur = con.cursor()
        try:
            if self.var_pid.get() == "":
                messagebox.showerror("Error", "Select Product From List", parent=self.root)
            else:
                cur.execute("SELECT * FROM Product WHERE pid=?", (self.var_pid.get(),))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Invalid Product", parent=self.root)
                else:
                    op = messagebox.askyesno("Confirm", "Do you really want to delete?", parent=self.root)
                    if op is True:
                        cur.execute("DELETE FROM product WHERE pid=?", (self.var_pid.get(),))
                        con.commit()
                        messagebox.showinfo("Delete", "Product Deleted Successfully", parent=self.root)
                        self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def clear(self, e):
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

        self.show()

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
