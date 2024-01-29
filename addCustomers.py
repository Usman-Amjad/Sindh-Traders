# -------Importing Modules
from tkinter import *
import customtkinter as ctk
from tkinter import ttk, messagebox
import sqlite3


class Customers:
    def __init__(self, root):
        super().__init__()
        self.root = root
        self.root.geometry("960x500+350+190")
        self.root.title("Sindh Traders")
        self.root.focus_force()

        ctk.set_appearance_mode("light")  # Modes: system (default), light, dark
        ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

        # ===== Style =====
        style = ttk.Style(self.root)

        # ==Declaring Variables==
        self.cust_id = StringVar()
        self.cust_name = StringVar()
        self.cust_balance = IntVar()
        self.sc1 = StringVar()  # For search

        self.varStatus = StringVar(value="Active")

        # ===== Title Label =====
        lbl_title = ctk.CTkLabel(self.root, text="Add Customer", font=("Brush Script MT", 50, "bold")).pack(side=TOP,
                                                                                                            fill=X,
                                                                                                            padx=10,
                                                                                                            pady=0)

        # ===== Search Frame =====
        self.searchFrame = ctk.CTkFrame(self.root, width=450, height=80)
        self.searchFrame.place(relx=0.01, rely=0.12)

        textColor = "#fff"

        lbl_search = ctk.CTkLabel(self.searchFrame, text="Search Customer | By Id",
                                  font=("Bell Gothic Std Black", 15, "bold")).place(x=5, y=5)
        txt_search = ctk.CTkEntry(self.searchFrame, textvariable=self.sc1, font=("Bell Gothic Std Black", 16),
                                  width=160,
                                  height=30,
                                  border_width=2,
                                  corner_radius=5).place(relx=0.01, rely=0.5)

        btn_show_all = ctk.CTkButton(self.searchFrame, text="Show All", command=self.show,
                                     font=("Bell Gothic Std Black", 17),
                                     width=100, height=32, border_width=0, text_color=textColor,
                                     corner_radius=8, cursor="hand2").place(relx=0.65, rely=0.48)
        btn_search = ctk.CTkButton(self.searchFrame, text="Search", command=self.search1,
                                   font=("Bell Gothic Std Black", 17),
                                   width=100, height=32, border_width=0, text_color=textColor,
                                   corner_radius=8, cursor="hand2").place(relx=0.4, rely=0.48)

        # ===== Details Adding Frame =====
        bg_color = "#333333"
        fg_color = "white"

        self.frame4 = ctk.CTkFrame(self.root, width=450, height=250)
        self.frame4.place(relx=0.01, rely=0.3)

        titleFont = ('Bell Gothic Std Black', 20)

        # ------row1
        lbl_cust_id = ctk.CTkLabel(self.frame4, text="Id", font=(titleFont)).place(x=20, y=5)
        txt_cust_id = ctk.CTkEntry(self.frame4, textvariable=self.cust_id, font=("Bell Gothic Std Black", 16)).place(
            x=120, y=5, width=200)

        # ------row2
        lbl_cust_name = ctk.CTkLabel(self.frame4, text="Name", font=(titleFont)).place(x=20, y=45)
        txt_cust_name = ctk.CTkEntry(self.frame4, textvariable=self.cust_name,
                                     font=("Bell Gothic Std Black", 16)).place(x=120, y=45, width=200)

        # ------row3
        lbl_cust_name = ctk.CTkLabel(self.frame4, text="Balance", font=(titleFont)).place(x=20, y=90)
        txt_cust_name = ctk.CTkEntry(self.frame4, textvariable=self.cust_balance, font=("Bell Gothic Std Black", 16),
                                     state=DISABLED).place(x=120, y=90, width=200)

        self.lbl_status = ctk.CTkLabel(self.frame4, text="Status", font=(titleFont))
        self.lbl_status.place(x=20, y=135)
        cmbStatus = ctk.CTkOptionMenu(self.frame4, variable=self.varStatus, dropdown_fg_color="#fff",
                                      dropdown_hover_color="light blue", dropdown_text_color="#000",
                                      values=("Active", "Inactive"), state='readonly',
                                      font=("Bell Gothic Std Black", 17), text_color="#fff")
        cmbStatus.place(x=120, y=135, width=200)

        # ------row3 Add Button
        btnStyle = ('Bell Gothic Std Black', 20)

        addBtn = ctk.CTkButton(self.frame4, text="Add", font=btnStyle, text_color=textColor, cursor="hand2")
        addBtn.place(x=120, y=180, width=100)
        addBtn.bind("<Return>", self.Add)
        addBtn.bind("<ButtonRelease-1>", self.Add)

        updateBtn = ctk.CTkButton(self.frame4, text="Update", font=btnStyle, text_color=textColor, cursor="hand2")
        updateBtn.place(x=205, y=180, width=100)
        updateBtn.bind("<Return>", self.Update)
        updateBtn.bind("<ButtonRelease-1>", self.Update)

        deleteBtn = ctk.CTkButton(self.frame4, text="Delete", font=btnStyle, text_color=textColor, cursor="hand2")
        deleteBtn.place(x=290, y=180, width=100)
        deleteBtn.bind("<Return>", self.delete_product)
        deleteBtn.bind("<ButtonRelease-1>", self.delete_product)

        # ==Database Frame==
        self.wrapper2 = LabelFrame(self.root, bd=1, relief=RIDGE)
        self.wrapper2.place(x=590, y=75, width=600, height=430)

        style.configure("Treeview", background="#333333", foreground="white", fieldbackground="#333333", rowheight=30,
                        font=("Arial", 17))
        style.map("Treeview", background=[("selected", "#0078D7")])
        style.configure("Treeview.Heading", font=('Bell Gothic Std Black', 16))
        style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])  # Remove the borders

        scrolly = Scrollbar(self.wrapper2, orient=VERTICAL)
        scrollx = Scrollbar(self.wrapper2, orient=HORIZONTAL)

        self.product_table = ttk.Treeview(self.wrapper2, style="Treeview", columns=(
            "custId", "custName", "custStatus"),
                                          yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        for column in self.product_table["columns"]:
            self.product_table.column(column, anchor=CENTER)

        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.product_table.xview)
        scrolly.config(command=self.product_table.yview)

        self.product_table.heading("custId", text="ID")
        self.product_table.heading("custName", text="Name")
        self.product_table.heading("custStatus", text="Status")

        self.product_table["show"] = "headings"

        self.product_table.column("custId", width=50)
        self.product_table.column("custName", width=100)
        self.product_table.column("custStatus", width=100)

        self.product_table.pack(fill=BOTH, expand=1)
        self.product_table.bind("<ButtonRelease-1>", self.getRow)

        self.show()

    def search1(self):
        conn = sqlite3.connect(database=r'std.db')
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT * FROM customersDetails WHERE custId LIKE '%" + self.sc1.get() + "%' ")
            fetch = cursor.fetchall()
            self.update1(fetch)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def show(self):
        conn = sqlite3.connect(database=r'std.db')
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT custId, custName, custStatus FROM customersDetails")
            rows = cursor.fetchall()
            self.product_table.delete(*self.product_table.get_children())
            for row in rows:
                self.product_table.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def clear1(self):
        self.cust_id.set("")
        self.cust_name.set("")
        self.varStatus.set("Select")

        self.show()

    def update1(self, fetch):
        self.product_table.delete(*self.product_table.get_children())
        for data in fetch:
            self.product_table.insert('', 'end', values=(data))

    def getRow(self, event):
        try:
            f = self.product_table.focus()
            content = (self.product_table.item(f))
            row = content['values']
            self.cust_id.set(row[0])
            self.cust_name.set(row[1])
            self.varStatus.set(row[2])
        except (Exception,):
            pass

    def delete_product(self, e):
        conn = sqlite3.connect(database=r'std.db')
        cursor = conn.cursor()
        try:
            op = messagebox.askyesno("Confirm", "Do you really want to delete?", parent=self.root)
            if op is True:
                cursor.execute("DELETE FROM customersDetails WHERE custId=?", (self.cust_id.get(),))
                conn.commit()
                messagebox.showinfo("Delete", "Customer Deleted Successfully", parent=self.root)
                self.clear1()
            else:
                pass
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def Add(self, e):
        conn = sqlite3.connect(database=r'std.db')
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM customersDetails WHERE custName=? OR custId=?",
                           (self.cust_name.get(), self.cust_id.get()))
            row = cursor.fetchone()
            if row is not None:
                messagebox.showerror("Error", "Customer already present, try different", parent=self.root)
            else:
                cursor.execute(
                    "INSERT INTO customersDetails(custId, custName, custBalance, custStatus) VALUES(?,?,?,?)",
                    (self.cust_id.get(), self.cust_name.get(), self.cust_balance.get(), self.varStatus.get()))
                conn.commit()
                messagebox.showinfo("Added", "Customer Added Successfully", parent=self.root)
                self.clear1()
                conn.close()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def Update(self, e):
        conn = sqlite3.connect(database=r'std.db')
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE customersDetails SET custName=?, custStatus=? WHERE custId=?",
                           (self.cust_name.get(), self.varStatus.get(), self.cust_id.get()))
            conn.commit()
            messagebox.showinfo("Update", "Customer Details Updated Successfully", parent=self.root)
            self.clear1()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)


if __name__ == "__main__":
    root = ctk.CTk()
    obj = Customers(root)
    root.mainloop()
