# -------Importing Modules
from tkinter import *
from tkinter import ttk, messagebox
import sqlite3
from tkcalendar import DateEntry
import customtkinter as ctk


class customersBilling:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x600+220+145")
        self.root.title("Sindh Traders")
        # self.root.config(bg="#333333")
        self.root.focus_force()

        ctk.set_appearance_mode("System")  # Modes: system (default), light, dark
        ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

        # ===== Style =====
        self.style = ttk.Style(self.root)

        # ====== Icon Image ======
        icon = PhotoImage(file='images/logo.png')
        self.root.iconphoto(False, icon)

        # ==Declaring Variables==
        self.cust_id = StringVar()
        self.cust_name = StringVar()
        self.custDues = StringVar()
        self.custPaidAmount = StringVar()
        self.sc1 = StringVar()  # For search

        self.varStatus = StringVar()

        # ===== Title Label =====
        lbl_title = ctk.CTkLabel(self.root, text="Payments Recovery", font=("Brush Script MT", 50)).pack(side=TOP,
                                                                                                         fill=X, pady=0)

        # ===== Search Frame =====
        self.searchFrame = ctk.CTkFrame(self.root)
        self.searchFrame.place(x=480, y=100, width=600, height=90)

        lbl_search = ctk.CTkLabel(self.searchFrame, text="Search Customer | By Id",
                                  font=("Bell Gothic Std Black", 15, "bold")).place(x=2, y=5)
        txt_search = ctk.CTkEntry(self.searchFrame, textvariable=self.sc1, font=("Bell Gothic Std Black", 16)).place(
            x=5, y=35, width=200)

        btn_search = ctk.CTkButton(self.searchFrame, text="Search", command=self.search1, font=("Bell Gothic Std Black", 15),
                                   cursor="hand2").place(x=285, y=45, width=100, height=30)
        btn_show_all = ctk.CTkButton(self.searchFrame, text="Show All", command=self.show, font=("Bell Gothic Std Black", 15),
                                     cursor="hand2").place(x=285, y=10, width=100, height=30)

        # ===== Details Adding Frame =====
        self.frame4 = ctk.CTkFrame(self.root)
        self.frame4.place(x=10, y=100, width=450, height=482)

        titleBg = '#333333'
        titleFg = 'white'
        titleFont = ('Bell Gothic Std Black', 18)

        lbl_cust_id = ctk.CTkLabel(self.frame4, text="Id", font=(titleFont)).place(x=20, y=5)
        txt_cust_id = ctk.CTkEntry(self.frame4, textvariable=self.cust_id, font=(titleFont)).place(x=140, y=5,
                                                                                                   width=200)

        lbl_cust_name = ctk.CTkLabel(self.frame4, text="Name", font=(titleFont)).place(x=20, y=45)
        txt_cust_name = ctk.CTkEntry(self.frame4, textvariable=self.cust_name, font=(titleFont)).place(x=140, y=45,
                                                                                                       width=200)

        lbl_cust_dues = ctk.CTkLabel(self.frame4, text="Dues", font=(titleFont)).place(x=20, y=85)
        txt_cust_dues = ctk.CTkEntry(self.frame4, textvariable=self.custDues, state='readonly', font=(titleFont)).place(
            x=140, y=85, width=200)

        lbl_cust_paid = ctk.CTkLabel(self.frame4, text="Amount Paid", font=(titleFont)).place(x=20, y=125)
        txt_cust_paid = ctk.CTkEntry(self.frame4, textvariable=self.custPaidAmount, font=(titleFont)).place(x=140,
                                                                                                            y=125,
                                                                                                            width=200)

        lbl_search_date = ctk.CTkLabel(self.frame4, text="Date", font=(titleFont, 17))
        lbl_search_date.place(x=20, y=165)
        self.cal = DateEntry(self.frame4, selectmode='day', background="#242424", disabledbackground="#242424",
                             bordercolor="#242424", font=("Bell Gothic Std Black", 15, "bold"),
                             headersbackground="#242424", normalbackground="#242424", foreground='white',
                             normalforeground='white', headersforeground='white', state='readonly')
        self.cal.place(x=175, y=210, width=200, height=30)

        # ------row3 Add Button
        btnFont = ('Bell Gothic Std Black', 17)

        addBtn = ctk.CTkButton(self.frame4, text="Add", font=(btnFont), cursor="hand2")
        addBtn.place(x=165, y=220, width=80, height=40)
        addBtn.bind("<Return>", self.Add)
        addBtn.bind("<ButtonRelease-1>", self.Add)

        # updateBtn = Button(self.frame4, text="Update", font=(bs), bg=backgroundColor, fg=foregroundColor,
        #                    cursor="hand2")
        # updateBtn.place(x=180, y=250, width=80)
        # updateBtn.bind("<Return>", self.Update)
        # updateBtn.bind("<ButtonRelease-1>", self.Update)

        deleteBtn = ctk.CTkButton(self.frame4, text="Delete", font=(btnFont), cursor="hand2")
        deleteBtn.place(x=235, y=220, width=80, height=40)
        deleteBtn.bind("<Return>", self.delete_product)
        deleteBtn.bind("<ButtonRelease-1>", self.delete_product)

        # ==Database Frame==
        self.wrapper2 = ctk.CTkFrame(self.root)
        self.wrapper2.place(x=480, y=180, width=600, height=390)

        self.style.configure("Treeview", background="#3c3c3c", foreground="white", fieldbackground="#333333",
                             rowheight=30,
                             font=("Arial", 17))
        self.style.map("Treeview", background=[("selected", "#0078D7")])
        self.style.configure("Treeview.Heading", font=('Bell Gothic Std Black', 17))
        self.style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])  # Remove the borders

        self.product_table = ttk.Treeview(self.wrapper2, style="Treeview", columns=(
            "custId", "custName", "custBalance", "custStatus"))
        for column in self.product_table["columns"]:
            self.product_table.column(column, anchor=CENTER)

        scrolly = ctk.CTkScrollbar(self.wrapper2, orientation=VERTICAL, command=self.product_table.yview)
        scrolly.pack(side=RIGHT, fill=Y)
        self.product_table.configure(yscrollcommand=scrolly.set)

        scrollx = ctk.CTkScrollbar(self.wrapper2, orientation=HORIZONTAL, command=self.product_table.xview)
        scrollx.pack(side=BOTTOM, fill=X)
        self.product_table.configure(xscrollcommand=scrollx.set)

        self.product_table.heading("custId", text="ID")
        self.product_table.heading("custName", text="Name")
        self.product_table.heading("custBalance", text="Balance")
        # self.product_table.heading("custPayType", text="Payment Type")
        self.product_table.heading("custStatus", text="Status")

        self.product_table["show"] = "headings"

        self.product_table.column("custId", width=50, minwidth=50)
        self.product_table.column("custName", width=100, minwidth=100)
        self.product_table.column("custBalance", width=100, minwidth=100)
        # self.product_table.column("custPayType", width=100, minwidth=100)
        self.product_table.column("custStatus", width=100, minwidth=100)

        self.product_table.pack(fill=BOTH, expand=1)
        self.product_table.bind("<ButtonRelease-1>", self.getData)

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
            cursor.execute("SELECT * FROM customersDetails")
            rows = cursor.fetchall()
            self.product_table.delete(*self.product_table.get_children())
            for row in rows:
                self.product_table.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def clear1(self):
        self.cust_id.set("")
        self.cust_name.set("")
        self.custDues.set("")
        self.custPaidAmount.set("")
        # self.varStatus.set("Select")

        self.show()

    def update1(self, fetch):
        self.product_table.delete(*self.product_table.get_children())
        for data in fetch:
            self.product_table.insert('', 'end', values=(data))

    def getData(self, event):
        try:
            f = self.product_table.focus()
            content = (self.product_table.item(f))
            row = content['values']
            self.cust_id.set(row[0])
            self.cust_name.set(row[1])
            self.custDues.set(row[2])
        except (Exception,):
            pass

    def delete_product(self, e):
        conn = sqlite3.connect(database=r'std.db')
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM customersDetails WHERE custId=?", (self.cust_id.get(),))
            conn.commit()
            messagebox.showinfo("Delete", "Customer Deleted Successfully", parent=self.root)
            self.clear1()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def Add(self, e):
        try:
            conn = sqlite3.connect(database=r'std.db')
            cursor = conn.cursor()
            if int(self.custPaidAmount.get()) > int(self.custDues.get()) or int(self.custPaidAmount.get()) < 0:
                messagebox.showerror('Error', 'Please enter valid amount amount cannot be less or greater than dues!!')
            else:
                remainingBalance = int(self.custDues.get()) - int(self.custPaidAmount.get())
                cursor.execute("SELECT * FROM customersDetails WHERE custName=? OR custId=?",
                               (self.cust_name.get(), self.cust_id.get()))
                row = cursor.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Select customer from the list", parent=self.root)
                else:
                    cursor.execute(
                        "INSERT INTO custPaymentDetails(custId, custName, custBalance, custPaid, custTotalBalance, custPayDate, custStatus) VALUES(?,?,?,?,?,?,?)",
                        (self.cust_id.get(), self.cust_name.get(), self.custDues.get(), self.custPaidAmount.get(),
                         remainingBalance, self.cal.get(), self.varStatus.get()))
                    conn.commit()
                    cursor.execute("UPDATE customersDetails SET custBalance=? WHERE custId=? ",
                                   (remainingBalance, self.cust_id.get()))
                    conn.commit()
                    messagebox.showinfo("Added", "Customer Payment Added Successfully", parent=self.root)
                    self.clear1()
                    conn.close()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    # def Update(self, e):
    #     conn = sqlite3.connect(database=r'std.db')
    #     cursor = conn.cursor()
    #     try:
    #         cursor.execute("UPDATE customersDetails SET custName=?, custStatus=? WHERE custId=?",
    #                        (self.cust_name.get(), self.varStatus.get(), self.cust_id.get()))
    #         conn.commit()
    #         messagebox.showinfo("Update", "Customer Details Updated Successfully", parent=self.root)
    #         self.clear1()
    #     except Exception as ex:
    #         messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)


if __name__ == "__main__":
    root = ctk.CTk()
    obj = customersBilling(root)
    root.mainloop()
