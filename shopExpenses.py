# -------Importing Modules
from tkinter import *
import customtkinter as ctk
from tkinter import ttk, messagebox
import sqlite3
from tkcalendar import DateEntry
from expensesNamesList import shopExpensesNamesList

switch_value = True


class shopExpenses:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x600+220+145")
        self.root.title("Sindh Traders")
        self.root.focus_force()

        # ===== Style =====
        style = ttk.Style(self.root)

        # ==Declaring Variables==
        self.expensesNamesList = []
        self.fetch_names()  # Calling Function

        self.expId = StringVar()
        self.expDesc = StringVar(value="Select Name")
        self.expPrice = StringVar()
        self.sc1 = StringVar()  # For search

        # ===== Title Label =====
        lbl_title = ctk.CTkLabel(self.root, text="Shop Expenses", font=("Brush Script MT", 50)).pack(side=TOP, fill=X, padx=10, pady=0, ipady=0)

        # ===== Expenses Name List Frame =====
        expensesNameBtn = ctk.CTkButton(self.root, text="Expenses Name", font=('Agency FB', 22), cursor="hand2")
        expensesNameBtn.place(x=10, y=60, width=150)
        expensesNameBtn.bind("<Return>", self.expensesNameWin)
        expensesNameBtn.bind("<ButtonRelease-1>", self.expensesNameWin)

        # ===== Details Adding Frame =====
        self.frame1 = ctk.CTkFrame(self.root)
        self.frame1.place(x=10, y=100, width=450, height=482)

        titleFont = ('Agency FB', 28)

        lbl_cust_name = ctk.CTkLabel(self.frame1, text="Name", font=(titleFont)).place(x=20, y=45)
        cmbCustName = ctk.CTkComboBox(self.frame1, font=("times new roman", 20), variable=self.expDesc,
                                      values=self.expensesNamesList, state="readonly", justify=CENTER, width=170,
                                      fg_color=("#333333"), text_color=("#3c3c3c"))
        cmbCustName.place(x=150, y=45, width=200)

        lbl_cust_name = ctk.CTkLabel(self.frame1, text="Amount", font=(titleFont)).place(x=20, y=90)
        txt_cust_name = ctk.CTkEntry(self.frame1, textvariable=self.expPrice, font=("goudy old style", 16)).place(x=150, y=90, width=200)

        lbl_search_date = ctk.CTkLabel(self.frame1, text="Date", font=(titleFont))
        lbl_search_date.place(x=20, y=135)
        self.cal = DateEntry(self.frame1, selectmode='day', background="black", disabledbackground="black",
                             bordercolor="black", font=("Agency FB", 15, "bold"),
                             headersbackground="black", normalbackground="black", foreground='white',
                             normalforeground='white', headersforeground='white', state='readonly')
        self.cal.place(x=190, y=175, width=190, height=28)

        addBtn = ctk.CTkButton(self.frame1, text="Add", font=('Agency FB', 22), cursor="hand2")
        addBtn.place(x=160, y=210, width=85)
        addBtn.bind("<Return>", self.Add)
        addBtn.bind("<ButtonRelease-1>", self.Add)

        updateBtn = ctk.CTkButton(self.frame1, text="Update", font=('Agency FB', 22), cursor="hand2")
        updateBtn.place(x=240, y=210, width=85)
        updateBtn.bind("<Return>", self.Update)
        updateBtn.bind("<ButtonRelease-1>", self.Update)

        # ===== Search Frame =====
        self.searchFrame = ctk.CTkFrame(self.root)
        self.searchFrame.place(x=400, y=100, width=600, height=90)

        lbl_search = ctk.CTkLabel(self.searchFrame, text="Search Customer | By Id",
                                  font=("times new roman", 18, "bold")).place(x=2, y=5)
        txt_search = ctk.CTkEntry(self.searchFrame, textvariable=self.sc1, font=("Neue Helvetica", 20)).place(x=5, y=35, width=200)

        btn_search = ctk.CTkButton(self.searchFrame, text="Search", font=("Neue Helvetica", 18), cursor="hand2", width=100, height=25)
        btn_search.place(x=240, y=35)
        btn_search.bind("<Return>", self.search1)
        btn_search.bind("<ButtonRelease-1>", self.search1)

        btn_show_all = ctk.CTkButton(self.searchFrame, text="Show All", command=self.show, font=("Neue Helvetica", 18), cursor="hand2", width=100, height=25)
        btn_show_all.place(x=350, y=35)

        # ==Details Frame==
        self.wrapper1 = ctk.CTkFrame(self.root)
        self.wrapper1.place(x=400, y=180, width=600, height=390)

        style.configure("Treeview", background="#333333", foreground="white", fieldbackground="#333333", rowheight=30,
                        font=("Arial", 18))
        style.map("Treeview", background=[("selected", "#0078D7")])
        style.configure("Treeview.Heading", font=('Constantia', 18))
        style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])  # Remove the borders

        self.product_table = ttk.Treeview(self.wrapper1, style="Treeview", columns=(
            "expId", "expDesc", "expPrice", "expDate"))
        for column in self.product_table["columns"]:
            self.product_table.column(column, anchor=CENTER)

        scrolly = ctk.CTkScrollbar(self.wrapper1, orientation=VERTICAL, command=self.product_table.yview)
        scrolly.pack(side=RIGHT, fill=Y)
        self.product_table.configure(yscrollcommand=scrolly.set)

        scrollx = ctk.CTkScrollbar(self.wrapper1, orientation=HORIZONTAL, command=self.product_table.xview)
        scrollx.pack(side=BOTTOM, fill=X)
        self.product_table.configure(xscrollcommand=scrollx.set)

        self.product_table.heading("expId", text="ID")
        self.product_table.heading("expDesc", text="Name")
        self.product_table.heading("expPrice", text="Price")
        self.product_table.heading("expDate", text="Date")

        self.product_table["show"] = "headings"

        self.product_table.column("expId", width=50, minwidth=50)
        self.product_table.column("expDesc", width=100, minwidth=100)
        self.product_table.column("expPrice", width=100, minwidth=100)
        self.product_table.column("expDate", width=100, minwidth=100)

        self.product_table.pack(fill=BOTH, expand=1)
        self.product_table.bind("<ButtonRelease-1>", self.getRow)

        self.show()

    def fetch_names(self):
        try:
            self.expensesNamesList.append("Empty")

            con = sqlite3.connect(database=r'std.db')
            cur = con.cursor()

            cur.execute("SELECT expDesc FROM shopExpensesNames")
            loc = cur.fetchall()
            if len(loc) > 0:
                del self.expensesNamesList[:]
                self.expensesNamesList.append("Select")
                for i in loc:
                    self.expensesNamesList.append(i[0])

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def search1(self, e):
        conn = sqlite3.connect(database=r'std.db')
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT * FROM shopExpenses WHERE expId LIKE '%" + self.sc1.get() + "%' OR expDesc LIKE '%" + self.sc1.get() + "%' ")
            fetch = cursor.fetchall()
            self.update1(fetch)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def show(self):
        conn = sqlite3.connect(database=r'std.db')
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM shopExpenses")
            rows = cursor.fetchall()
            self.product_table.delete(*self.product_table.get_children())
            for row in rows:
                self.product_table.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def clear1(self):
        self.expDesc.set("")
        self.expPrice.set(0)

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
            self.expId.set(row[0])
            self.expDesc.set(row[1])
            self.expPrice.set(row[2])
            self.cal.set_date(row[3])
        except (Exception,):
            pass

    def Add(self, e):
        try:
            conn = sqlite3.connect(database=r'std.db')
            cursor = conn.cursor()

            dt = self.cal.get_date()
            date1 = str(dt.strftime("%m/%d/%Y"))

            if self.expDesc.get() == "Select Name" and self.expPrice.get() == "" or self.expDesc.get() == "":
                messagebox.showerror("Error", "Please select name or enter price", parent=self.root)
            else:
                cursor.execute("INSERT INTO shopExpenses(expDesc, expPrice, expDate) VALUES(?,?,?)",
                               (self.expDesc.get(), int(self.expPrice.get()), date1))
                conn.commit()
                messagebox.showinfo("Added", "Expenses Added Successfully", parent=self.root)
                self.clear1()
                conn.close()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def Update(self, e):
        try:
            conn = sqlite3.connect(database=r'std.db')
            cursor = conn.cursor()

            cursor.execute("UPDATE shopExpenses SET expDesc=?, expPrice=? WHERE expId=?", (self.expDesc.get(), self.expPrice.get(), self.expId.get()))
            conn.commit()
            messagebox.showinfo("Update", "Expenses Information Updated Successfully", parent=self.root)
            self.clear1()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def expensesNameWin(self, e):
        self.expenses_win = ctk.CTkToplevel(self.root)
        self.expenses_obj = shopExpensesNamesList(self.expenses_win)


if __name__ == "__main__":
    root = ctk.CTk()
    obj = shopExpenses(root)
    root.mainloop()
