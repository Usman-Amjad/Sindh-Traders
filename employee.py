# -------Importing Modules
from tkinter import *
from tkinter import ttk, messagebox
import sqlite3
from PIL import Image
from datetime import datetime
import customtkinter as ctk


class employeeClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x600+200+148")
        self.root.title("UA")
        self.root.focus_force()
        self.root.resizable(False, False)

        ctk.set_appearance_mode("System")  # Modes: system (default), light, dark
        ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

        # ========================================
        # ============ All variables ===========
        self.var_searchby = StringVar(value="Select")
        self.var_searchtxt = StringVar()

        self.var_emp_id = StringVar()
        self.var_gender = StringVar(value="Select")
        self.var_contact = StringVar()
        self.var_name = StringVar()
        self.var_dob = StringVar()  # Date of Birth
        self.var_doj = StringVar()  # Date of joining
        self.var_email = StringVar()
        self.var_pass = StringVar()
        self.var_utype = StringVar(value="Select")  # User Type
        self.var_salary = StringVar()

        # Label Styling
        fontStyle = ("Bell Gothic Std Black", 17, 'bold')

        # ===== Icon image =====
        icon = PhotoImage(file='images/logo.png')
        self.root.iconphoto(False, icon)

        # ===== Style =====
        self.style = ttk.Style(self.root)

        # ====== Title =======
        self.title = ctk.CTkLabel(self.root, text="Return Products", font=("Brush Script MT", 38, "bold"))
        self.title.pack(side=TOP, fill=X)

        # ===== Logo Image =====
        stLogo = ctk.CTkImage(Image.open("images/logo.png"), size=(120, 120))
        logoImage = (ctk.CTkLabel(self.root, image=stLogo))
        logoImage.configure(text="")
        logoImage.place(x=5, y=10, width=120, height=95)

        # ====== Search Frame ======
        self.SearchFrame = ctk.CTkLabel(self.root, font=(fontStyle, 12, "bold"))
        self.SearchFrame.pack(padx=300, pady=10, ipady=20, fill=X)

        # ====== Options ======
        cmb_search = ctk.CTkComboBox(self.SearchFrame, variable=self.var_searchby,
                                     values=("Select", "Email", "Name", "Contact"), state='readonly',
                                     justify=CENTER, text_color=("#000"),
                                     font=("Agency FB", 20, "bold"))
        cmb_search.place(x=10, y=15, width=180, height=35)

        self.txtSearch = ctk.CTkEntry(self.SearchFrame, textvariable=self.var_searchtxt, font=(fontStyle, 15))
        self.txtSearch.place(x=185, y=15, height=35)

        btn_search = ctk.CTkButton(self.SearchFrame, text="Search", command=self.search, font=(fontStyle, 18),
                                   cursor="hand2").place(x=350, y=15, width=150, height=35)

        # ====== Title ======
        title = ctk.CTkLabel(self.root, text="Employee Details", font=(fontStyle, 15, 'bold'),
                             bg_color="#0f4d7d")
        title.pack(padx=50, pady=10, fill=X)

        # ===== Content ======
        # ====== Row 1 ======
        xAxisOneLabel = 50
        xAxisTwoLabel = 450
        xAxisThreeLabel = 810

        xAxisOneEntry = 180
        xAxisTwoEntry = 550
        xAxisThreeEntry = 905

        self.lblEmpId = ctk.CTkLabel(self.root, text="Employee ID", font=fontStyle)
        self.lblEmpId.place(x=xAxisOneLabel, y=200)
        self.lblGender = ctk.CTkLabel(self.root, text="Gender", font=fontStyle)
        self.lblGender.place(x=xAxisTwoLabel, y=200)
        self.lblContact = ctk.CTkLabel(self.root, text="Contact", font=fontStyle)
        self.lblContact.place(x=xAxisThreeLabel, y=200)

        self.txtEmpId = ctk.CTkEntry(self.root, textvariable=self.var_emp_id, font=(fontStyle, 15))
        self.txtEmpId.place(x=xAxisOneEntry, y=200, width=180)
        cmb_gender = ctk.CTkComboBox(self.root, variable=self.var_gender,
                                     values=("Select", "Male", "Female", "Other"), justify=CENTER,
                                     font=(fontStyle, 15))
        cmb_gender.place(x=xAxisTwoEntry, y=200, width=180)

        self.txtContact = ctk.CTkEntry(self.root, textvariable=self.var_contact, font=(fontStyle, 15))
        self.txtContact.place(x=xAxisThreeEntry, y=200, width=180)

        # ====== Row 2 ======

        self.lblName = ctk.CTkLabel(self.root, text="Name", font=fontStyle)
        self.lblName.place(x=xAxisOneLabel, y=240)
        self.lblDob = ctk.CTkLabel(self.root, text="D.O.B", font=fontStyle)
        self.lblDob.place(x=xAxisTwoLabel, y=240)
        self.lblDoj = ctk.CTkLabel(self.root, text="D.O.J", font=fontStyle)
        self.lblDoj.place(x=xAxisThreeLabel, y=240)

        self.txtName = ctk.CTkEntry(self.root, textvariable=self.var_name, font=(fontStyle, 15))
        self.txtName.place(x=xAxisOneEntry, y=240, width=180)
        self.txtDob = ctk.CTkEntry(self.root, textvariable=self.var_dob, font=(fontStyle, 15))
        self.txtDob.place(x=xAxisTwoEntry, y=240, width=180)
        self.txtDoj = ctk.CTkEntry(self.root, textvariable=self.var_doj, font=(fontStyle, 15))
        self.txtDoj.place(x=xAxisThreeEntry, y=240, width=180)

        # ====== Row 3 ======
        self.lblEmail = ctk.CTkLabel(self.root, text="Email", font=fontStyle)
        self.lblEmail.place(x=xAxisOneLabel, y=280)
        self.lblPass = ctk.CTkLabel(self.root, text="Password", font=fontStyle)
        self.lblPass.place(x=xAxisTwoLabel, y=280)
        self.lblUtype = ctk.CTkLabel(self.root, text="User Type", font=fontStyle)
        self.lblUtype.place(x=xAxisThreeLabel, y=280)

        self.txtEmail = ctk.CTkEntry(self.root, textvariable=self.var_email, font=(fontStyle, 15))
        self.txtEmail.place(x=xAxisOneEntry, y=280, width=180)
        self.txtPass = ctk.CTkEntry(self.root, textvariable=self.var_pass, font=(fontStyle, 15))
        self.txtPass.place(x=xAxisTwoEntry, y=280, width=180)
        cmb_utype = ctk.CTkComboBox(self.root, variable=self.var_utype,
                                    values=("Admin", "Employee"), justify=CENTER,
                                    font=(fontStyle, 15))
        cmb_utype.place(x=xAxisThreeEntry, y=280, width=180)

        # ====== Row 4 ======
        self.lblAddress = ctk.CTkLabel(self.root, text="Address", font=fontStyle)
        self.lblAddress.place(x=50, y=330)
        self.lblSalary = ctk.CTkLabel(self.root, text="Salary", font=fontStyle)
        self.lblSalary.place(x=450, y=330)

        self.txtAddress = ctk.CTkTextbox(self.root, font=(fontStyle, 15))
        self.txtAddress.place(x=180, y=330, width=300, height=80)
        self.txtSalary = ctk.CTkEntry(self.root, textvariable=self.var_salary, font=(fontStyle, 15))
        self.txtSalary.place(x=550, y=330, width=180)

        # ====== Buttons ======
        btnFontStyle = "Bell Gothic Std Black"
        self.addIcon = ctk.CTkImage(Image.open("images/add.png"), size=(30, 30))
        self.btn_add = ctk.CTkButton(self.root, text="Add", image=self.addIcon, font=(btnFontStyle, 18),
                                     cursor="hand2", compound=RIGHT)
        self.btn_add.place(x=640, y=370, width=110)
        self.btn_add.bind("<Return>", self.add)
        self.btn_add.bind("<ButtonRelease-1>", self.add)

        self.updateIcon = ctk.CTkImage(Image.open("images/update.png"), size=(30, 30))
        self.btn_update = ctk.CTkButton(self.root, text="Update", image=self.updateIcon, font=(btnFontStyle, 18),
                                        cursor="hand2", compound=RIGHT)
        self.btn_update.place(x=734, y=370, width=130)
        self.btn_update.bind("<Return>", self.update)
        self.btn_update.bind("<ButtonRelease-1>", self.update)

        self.deleteIcon = ctk.CTkImage(Image.open("images/delete.png"), size=(30, 30))
        self.btn_delete = ctk.CTkButton(self.root, text="Delete", image=self.deleteIcon, font=(btnFontStyle, 18),
                                        cursor="hand2", compound=RIGHT)
        self.btn_delete.place(x=845, y=370, width=110)
        self.btn_delete.bind("<Return>", self.delete)
        self.btn_delete.bind("<ButtonRelease-1>", self.delete)

        self.clearIcon = ctk.CTkImage(Image.open("images/clear.png"), size=(30, 30))
        self.btn_clear = ctk.CTkButton(self.root, text="Clear All", image=self.clearIcon, font=(btnFontStyle, 18),
                                       cursor="hand2", compound=RIGHT)
        self.btn_clear.place(x=940, y=370, width=130)
        self.btn_clear.bind("<Return>", self.clear)
        self.btn_clear.bind("<ButtonRelease-1>", self.clear)

        # ====== Employee Details ======
        emp_frame = ctk.CTkFrame(self.root)
        emp_frame.place(x=0, y=450, relwidth=1, height=180)

        self.style.configure("Treeview", background="#3c3c3c", foreground="white", fieldbackground="#333333",
                             rowheight=30,
                             font=("Arial", 17))
        self.style.map("Treeview", background=[("selected", "#0078D7")])
        self.style.configure("Treeview.Heading", font=('Bell Gothic Std Black', 17))
        self.style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])  # Remove the borders

        self.EmployeeTable = ttk.Treeview(emp_frame, style='Treeview', columns=(
            "eid", "name", "email", "gender", "contact", "dob", "doj", "pass", "utype", "address", "salary"))
        for column in self.EmployeeTable["columns"]:
            self.EmployeeTable.column(column, anchor=CENTER)

        scrolly = ctk.CTkScrollbar(emp_frame, orientation=VERTICAL, command=self.EmployeeTable.yview)
        scrolly.pack(side=RIGHT, fill=Y)
        self.EmployeeTable.configure(yscrollcommand=scrolly.set)

        scrollx = ctk.CTkScrollbar(emp_frame, orientation=HORIZONTAL, command=self.EmployeeTable.xview)
        scrollx.pack(side=BOTTOM, fill=X)
        self.EmployeeTable.configure(xscrollcommand=scrollx.set)

        self.EmployeeTable.heading("eid", text="ID")
        self.EmployeeTable.heading("name", text="Name")
        self.EmployeeTable.heading("email", text="Email")
        self.EmployeeTable.heading("gender", text="Gender")
        self.EmployeeTable.heading("contact", text="Contact")
        self.EmployeeTable.heading("dob", text="D.O.B")
        self.EmployeeTable.heading("doj", text="D.O.J")
        self.EmployeeTable.heading("pass", text="Password")
        self.EmployeeTable.heading("utype", text="User Type")
        self.EmployeeTable.heading("address", text="Address")
        self.EmployeeTable.heading("salary", text="Salary")

        self.EmployeeTable["show"] = "headings"

        self.EmployeeTable.column("eid", width=100, minwidth=100)
        self.EmployeeTable.column("name", width=200, minwidth=200)
        self.EmployeeTable.column("email", width=230, minwidth=250)
        self.EmployeeTable.column("gender", width=150, minwidth=150)
        self.EmployeeTable.column("contact", width=200, minwidth=200)
        self.EmployeeTable.column("dob", width=200, minwidth=200)
        self.EmployeeTable.column("doj", width=200, minwidth=200)
        self.EmployeeTable.column("pass", width=200, minwidth=200)
        self.EmployeeTable.column("utype", width=200, minwidth=200)
        self.EmployeeTable.column("address", width=220)
        self.EmployeeTable.column("salary", width=200, minwidth=200)

        self.EmployeeTable.pack(fill=BOTH, expand=1)
        self.EmployeeTable.bind("<ButtonRelease-1>", self.get_data)

        self.show()
        # ========================================================================================

    def add(self, e):
        con = sqlite3.connect(database=r'std.db')
        cur = con.cursor()
        try:
            self.addDate = datetime.now().strftime("%m/%d/%Y")
            if self.var_emp_id.get() == "":
                messagebox.showerror("Error", "Employee Id Must be required", parent=self.root)
            else:
                cur.execute("SELECT * FROM employee WHERE eid=?", (self.var_emp_id.get(),))
                row = cur.fetchone()
                if row is not None:
                    messagebox.showerror("Error", "This Employee ID already assigned, try different", parent=self.root)
                else:
                    cur.execute(
                        "INSERT INTO employee (eid,name,email,gender,contact,dob,doj,pass,utype,address,salary) values(?,?,?,?,?,?,?,?,?,?,?)",
                        (
                            self.var_emp_id.get(),
                            self.var_name.get(),
                            self.var_email.get(),
                            self.var_gender.get(),
                            self.var_contact.get(),
                            self.var_dob.get(),
                            self.var_doj.get(),
                            self.var_pass.get(),
                            self.var_utype.get(),
                            self.txtAddress.get('1.0', END),
                            self.var_salary.get()
                        ))
                    con.commit()
                    messagebox.showinfo("Success", "Employee Added Successfully", parent=self.root)
                    self.show()

                cur.execute("SELECT expDesc FROM shopExpenses WHERE expDesc=?", ("Salary",))
                row = cur.fetchone()
                if row is not None:
                    messagebox.showerror("Error", "This name is not in the list of shop expenses page",
                                         parent=self.root)
                else:
                    cur.execute(
                        "INSERT INTO shopExpenses (expDesc, expPrice, expDate) values(?,?,?)",
                        (
                            self.var_name.get(),
                            self.var_salary.get(),
                            self.addDate
                        ))
                    con.commit()
                    con.close()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def show(self):
        con = sqlite3.connect(database=r'std.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM employee")
            rows = cur.fetchall()
            self.EmployeeTable.delete(*self.EmployeeTable.get_children())
            for row in rows:
                self.EmployeeTable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def get_data(self, ev):
        try:
            f = self.EmployeeTable.focus()
            content = (self.EmployeeTable.item(f))
            row = content['values']
            self.var_emp_id.set(row[0])
            self.var_name.set(row[1])
            self.var_email.set(row[2])
            self.var_gender.set(row[3])
            self.var_contact.set(row[4])
            self.var_dob.set(row[5])
            self.var_doj.set(row[6])
            self.var_pass.set(row[7])
            self.var_utype.set(row[8])
            self.txtAddress.delete('1.0', END),
            self.txtAddress.insert(END, row[9]),
            self.var_salary.set(row[10])
        except (Exception,):
            pass

    def update(self, e):
        con = sqlite3.connect(database=r'std.db')
        cur = con.cursor()
        try:
            if self.var_emp_id.get() == "":
                messagebox.showerror("Error", "Employee Id Must be required", parent=self.root)
            else:
                cur.execute("SELECT * FROM employee WHERE eid=?", (self.var_emp_id.get(),))
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror("Error", "Invalid Employee ID", parent=self.root)
                else:
                    cur.execute(
                        "UPDATE employee set name=?,email=?,gender=?,contact=?,dob=?,doj=?,pass=?,utype=?,address=?,salary=? WHERE eid=?",
                        (
                            self.var_name.get(),
                            self.var_email.get(),
                            self.var_gender.get(),
                            self.var_contact.get(),
                            self.var_dob.get(),
                            self.var_doj.get(),
                            self.var_pass.get(),
                            self.var_utype.get(),
                            self.txtAddress.get('1.0', END),
                            self.var_salary.get(),
                            self.var_emp_id.get()
                        ))
                    con.commit()
                    messagebox.showinfo("Success", "Employee Updated Successfully", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def delete(self, e):
        con = sqlite3.connect(database=r'std.db')
        cur = con.cursor()
        try:
            if self.var_emp_id.get() == "":
                messagebox.showerror("Error", "Employee Id Must be required", parent=self.root)
            else:
                cur.execute("SELECT * FROM employee WHERE eid=?", (self.var_emp_id.get(),))
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror("Error", "Invalid Employee ID", parent=self.root)
                else:
                    op = messagebox.askyesno("Confirm", "Do you really want to delete?", parent=self.root)
                    if op == True:
                        cur.execute("DELETE FROM employee WHERE eid=?", (self.var_emp_id.get(),))
                        con.commit()
                        messagebox.showinfo("Delete", "Employee Deleted Successfully", parent=self.root)
                        self.clear(e)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def clear(self, e):
        self.var_emp_id.set("")
        self.var_name.set("")
        self.var_email.set("")
        self.var_gender.set("Select")
        self.var_contact.set("")
        self.var_dob.set("")
        self.var_doj.set("")
        self.var_pass.set("")
        self.var_utype.set("Admin")
        self.txtAddress.delete('1.0', END)
        self.var_salary.set("")
        self.var_searchtxt.set("")
        self.var_searchby.set("Select")

        self.show()

    def search(self):
        con = sqlite3.connect(database=r'std.db')
        cur = con.cursor()
        try:
            if self.var_searchby.get() == "Select":
                messagebox.showerror("Error", "Select Search By Option", parent=self.root)
            elif self.var_searchtxt.get() == "":
                messagebox.showerror("Error", "Select input should be required", parent=self.root)
            else:
                cur.execute(
                    "SELECT * FROM employee WHERE " + self.var_searchby.get() + " LIKE '%" + self.var_searchtxt.get() + "%'")
                rows = cur.fetchall()
                if len(rows) != 0:
                    self.EmployeeTable.delete(*self.EmployeeTable.get_children())
                    for row in rows:
                        self.EmployeeTable.insert('', END, values=row)
                else:
                    messagebox.showerror("Error", "No record found!!!", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)


if __name__ == "__main__":
    root = ctk.CTk()
    obj = employeeClass(root)
    root.mainloop()
