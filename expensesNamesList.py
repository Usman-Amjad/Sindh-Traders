# -------Importing Modules
from tkinter import *
import customtkinter as ctk
from tkinter import ttk, messagebox
import sqlite3


class shopExpensesNamesList:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x600+250+190")
        self.root.title("Sindh Traders")
        self.root.focus_force()

        ctk.set_appearance_mode("light")  # Modes: system (default), light, dark
        ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

        # ===== Style =====
        style = ttk.Style(self.root)

        # ==Declaring Variables==
        self.expName = StringVar()
        self.expID = IntVar()
        self.sc1 = StringVar()  # For search

        # ===== Title Label =====
        lbl_title = ctk.CTkLabel(self.root, text="Expenses Names", font=("Brush Script MT", 50, "bold")).pack(side=TOP, fill=X,
                                                                                                      padx=10, pady=0, ipady=0)

        # ===== Details Adding Frame =====
        self.frame2 = ctk.CTkFrame(self.root)
        self.frame2.pack(fill=BOTH, expand=1)

        titleFont = ('Bell Gothic Std Black', 20)

        lbl_cust_name = ctk.CTkLabel(self.frame2, text="Name", font=(titleFont)).place(x=20, y=45)
        txt_cust_name = ctk.CTkEntry(self.frame2, textvariable=self.expName, font=("Bell Gothic Std Black", 20)).place(
            x=100, y=45, width=250)

        addBtn = ctk.CTkButton(self.frame2, text="Add", font=(titleFont), cursor="hand2")
        addBtn.place(x=320, y=45, width=90)
        addBtn.bind("<Return>", self.Add)
        addBtn.bind("<ButtonRelease-1>", self.Add)

        deleteBtn = ctk.CTkButton(self.frame2, text="Delete", font=(titleFont), cursor="hand2")
        deleteBtn.place(x=400, y=45, width=90)
        deleteBtn.bind("<Return>", self.delete)
        deleteBtn.bind("<ButtonRelease-1>", self.delete)

        # ==Details Frame==
        self.wrapper2 = ctk.CTkFrame(self.root)
        self.wrapper2.pack(fill=BOTH, expand=1)

        style.configure("Treeview", background="#ebebeb", foreground="black", fieldbackground="#ebebeb", rowheight=30,
                        font=("Bell Gothic Std Black", 18))
        style.map("Treeview", background=[("selected", "#333333")])
        style.configure("Treeview.Heading", font=('Bell Gothic Std Black', 18))
        style.layout("Treeview",
                     [('Treeview.treearea', {'sticky': 'nswe'})])  # Remove the borders

        self.product_table = ttk.Treeview(self.wrapper2, style="Treeview", columns=(
            "expId", "expName"))
        for column in self.product_table["columns"]:
            self.product_table.column(column, anchor=CENTER)

        scrolly = ctk.CTkScrollbar(self.wrapper2, orientation=VERTICAL, command=self.product_table.yview)
        scrolly.pack(side=RIGHT, fill=Y)
        self.product_table.configure(yscrollcommand=scrolly.set)

        scrollx = ctk.CTkScrollbar(self.wrapper2, orientation=HORIZONTAL, command=self.product_table.xview)
        scrollx.pack(side=BOTTOM, fill=X)
        self.product_table.configure(xscrollcommand=scrollx.set)

        self.product_table.heading("expId", text="ID")
        self.product_table.heading("expName", text="Name")

        self.product_table["show"] = "headings"

        self.product_table.column("expId", width=40, minwidth=40)
        self.product_table.column("expName", width=100, minwidth=100)

        self.product_table.pack(fill=BOTH, expand=1)
        self.product_table.bind("<ButtonRelease-1>", self.getRow)

        self.show()

    def Add(self, e):
        conn = sqlite3.connect(database=r'std.db')
        cursor = conn.cursor()
        try:
            if self.expName.get() == "":
                messagebox.showerror("Error", "Please enter name", parent=self.root)
            else:
                cursor.execute("INSERT INTO shopExpensesNames(expName) VALUES(?)",
                               (self.expName.get(),))
                conn.commit()
                messagebox.showinfo("Added", "Expenses Added Successfully", parent=self.root)
                self.clear1()
                conn.close()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def delete(self, e):
        con = sqlite3.connect(database=r'std.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM shopExpensesNames WHERE expName=?", (self.expName.get(),))
            row = cur.fetchone()
            if self.expName.get() == "" or row is None:
                messagebox.showerror("Error", "Error, please try again", parent=self.root)
            else:
                op = messagebox.askyesno("Confirm", "Do you really want to delete?", parent=self.root)
                if op is True:
                    cur.execute("DELETE FROM shopExpensesNames WHERE expName=? or expID=?",
                                (self.expName.get(), self.expID.get()))
                    con.commit()
                    messagebox.showinfo("Delete", "Name Deleted Successfully", parent=self.root)
                    con.close()
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def clear1(self):
        self.expName.set("")

        self.show()

    def update1(self, fetch):
        self.product_table.delete(*self.product_table.get_children())
        for data in fetch:
            self.product_table.insert('', 'end', values=(data))

    def show(self):
        conn = sqlite3.connect(database=r'std.db')
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT expID, expName FROM shopExpensesNames")
            rows = cursor.fetchall()
            self.product_table.delete(*self.product_table.get_children())
            for row in rows:
                self.product_table.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def getRow(self, event):
        try:
            f = self.product_table.focus()
            content = (self.product_table.item(f))
            row = content['values']
            self.expID.set(row[0])
            self.expName.set(row[1])
        except (Exception,):
            pass


if __name__ == "__main__":
    root = ctk.CTk()
    obj = shopExpensesNamesList(root)
    root.mainloop()
