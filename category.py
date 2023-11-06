# -------Importing Modules
from tkinter import *
import customtkinter as ctk
from tkinter import ttk, messagebox
import sqlite3


class categoryClass():
    def __init__(self, root):
        self.root = root
        self.root.geometry("800x500+450+148")
        self.root.title("Category")
        self.root.focus_force()

        ctk.set_appearance_mode("System")  # Modes: system (default), light, dark
        ctk.set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green

        # ===== Variables =====
        self.var_cat_id = StringVar()
        self.var_name = StringVar()

        # ===== Style =====
        style = ttk.Style(self.root)

        icon = PhotoImage(file='images/logo.png')
        self.root.iconphoto(False, icon)

        # ====== Title ======
        self.lbl_title = ctk.CTkLabel(self.root, text="Manage Product Category", font=("Brush Script MT", 50))
        self.lbl_title.pack(side=TOP, fill=X)

        self.lbl_name = ctk.CTkLabel(self.root, text="Enter Category Name", font=("Agency FB", 30))
        self.lbl_name.place(x=50, y=120)

        self.txt_name = ctk.CTkEntry(self.root, textvariable=self.var_name, font=("Agency FB", 20))
        self.txt_name.place(x=50, y=170, width=300, height=40)
        self.txt_name.focus()

        btn_add = ctk.CTkButton(self.root, text="Add", font=("Agency FB", 20), cursor="hand2")
        btn_add.place(x=110, y=230, width=100, height=35)
        btn_add.bind("<Return>", self.add)
        btn_add.bind("<ButtonRelease-1>", self.add)

        btn_delete = ctk.CTkButton(self.root, text="Delete", font=("Agency FB", 20), cursor="hand2")
        btn_delete.place(x=210, y=230, width=100, height=35)
        btn_delete.bind("<Return>", self.delete)
        btn_delete.bind("<ButtonRelease-1>", self.delete)

        # ====== Category Details ======
        cat_frame = ctk.CTkFrame(self.root)
        cat_frame.place(x=350, y=100, width=500, height=450)

        style.configure("Treeview", background="#333333", foreground="white", fieldbackground="#333333", rowheight=30,
                        font=("Arial", 18))
        style.map("Treeview", background=[("selected", "#0078D7")])
        style.configure("Treeview.Heading", font=('Constantia', 18))
        style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])  # Remove the borders

        self.categoryTable = ttk.Treeview(cat_frame, style="Treeview", columns=("cid", "name"))
        for column in self.categoryTable["columns"]:
            self.categoryTable.column(column, anchor=CENTER)

        scrolly = ctk.CTkScrollbar(cat_frame, command=self.categoryTable.yview)
        scrolly.pack(side=RIGHT, fill=Y)
        self.categoryTable.configure(yscrollcommand=scrolly.set)

        self.categoryTable.heading("cid", text="Id")
        self.categoryTable.heading("name", text="Name")

        self.categoryTable["show"] = "headings"

        self.categoryTable.column("cid", width=30, minwidth=30)
        self.categoryTable.column("name", width=100, minwidth=110)

        self.categoryTable.pack(fill=BOTH, expand=1)

        self.categoryTable.bind("<ButtonRelease-1>", self.get_data)
        self.show()
    # ========================= Functions ==============================

    def add(self, e):
        con = sqlite3.connect(database=r'std.db')
        cur = con.cursor()
        try:
            if self.var_name.get() == "":
                messagebox.showerror("Error", "Category Name must be required", parent=self.root)
            else:
                cur.execute("SELECT * FROM category WHERE name=?", (self.var_name.get(),))
                row = cur.fetchone()
                if row is not None:
                    messagebox.showerror("Error", "Category already present, try different", parent=self.root)
                else:
                    cur.execute("INSERT INTO category(name) values(?)", (self.var_name.get(),))
                    con.commit()
                    messagebox.showinfo("Success", "Category Added Successfully", parent=self.root)
                    self.show()
                    self.var_cat_id.set("")
                    self.var_name.set("")
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def show(self):
        con = sqlite3.connect(database=r'std.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM category")
            rows = cur.fetchall()
            self.categoryTable.delete(*self.categoryTable.get_children())
            for row in rows:
                self.categoryTable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def get_data(self, ev):
        try:
            f = self.categoryTable.focus()
            content = (self.categoryTable.item(f))
            row = content['values']
            self.var_cat_id.set(row[0])
            self.var_name.set(row[1])
        except (Exception,):
            pass

    def delete(self, e):
        con = sqlite3.connect(database=r'std.db')
        cur = con.cursor()
        try:
            if self.var_cat_id.get() == "":
                messagebox.showerror("Error", "Please Select Category From The List", parent=self.root)
            else:
                cur.execute("SELECT * FROM category WHERE cid=?", (self.var_cat_id.get(),))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Error, Please try Again", parent=self.root)
                else:
                    op = messagebox.askyesno("Confirm", "Do you really want to delete?", parent=self.root)
                    if op is True:
                        cur.execute("DELETE FROM category WHERE cid=?", (self.var_cat_id.get(),))
                        con.commit()
                        messagebox.showinfo("Delete", "Category Deleted Successfully", parent=self.root)
                        self.show()
                        self.var_cat_id.set("")
                        self.var_name.set("")
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)


if __name__ == "__main__":
    root = ctk.CTk()
    obj = categoryClass(root)
    root.mainloop()
