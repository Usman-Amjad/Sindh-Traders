# -------Importing Modules
from tkinter import *
import customtkinter as ctk
from tkinter import ttk, messagebox
import sqlite3
from PIL import Image


class locationClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+200+148")
        self.root.title("ASB")
        self.root.focus_force()

        ctk.set_appearance_mode("System")  # Modes: system (default), light, dark
        ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

        # ===== Variables =====
        self.var_loc_id = StringVar()
        self.var_name = StringVar()
        self.address = StringVar()

        # ===== Style =====
        self.style = ttk.Style(self.root)

        # ====== Icon Image ======
        icon = PhotoImage(file='images/logo.png')
        self.root.iconphoto(False, icon)

        # ====== Title ======
        self.lbl_title = ctk.CTkLabel(self.root, text="Manage Location", font=("Brush Script MT", 50))
        self.lbl_title.pack(side=TOP, fill=X)

        # ====== Logo ======
        self.logo = ctk.CTkImage(Image.open("images/logo.png"), size=(120, 120))
        self.logoImage = ctk.CTkLabel(self.root, image=self.logo)
        self.logoImage.configure(text="")
        self.logoImage.place(x=5, y=10, width=120, height=95)

        self.lbl_name = ctk.CTkLabel(self.root, text="Name \t             Address", font=("goudy old style", 25))
        self.lbl_name.place(x=50, y=105)

        self.txt_name = ctk.CTkEntry(self.root, textvariable=self.var_name, font=("Bell Gothic Std Black", 18))
        self.txt_name.place(x=50, y=160, width=200)
        self.txt_name.focus()

        self.txtAddress = ctk.CTkEntry(self.root, textvariable=self.address, font=("Bell Gothic Std Black", 18))
        self.txtAddress.place(x=235, y=160, width=300)

        self.addIcon = ctk.CTkImage(Image.open("images/add.png"), size=(30, 30))
        self.btn_add = ctk.CTkButton(self.root, text="Add", image=self.addIcon, font=("Bell Gothic Std Black", 17), compound=RIGHT, cursor="hand2")
        self.btn_add.place(x=280, y=220, width=120, height=50)
        self.btn_add.bind("<Return>", self.add)
        self.btn_add.bind("<ButtonRelease-1>", self.add)

        self.deleteIcon = ctk.CTkImage(Image.open("images/delete.png"), size=(30, 30))
        self.btn_delete = ctk.CTkButton(self.root, text="Delete", image=self.deleteIcon, font=("Bell Gothic Std Black", 17), compound=RIGHT, cursor="hand2")
        self.btn_delete.place(x=380, y=220, width=120, height=50)
        self.btn_delete.bind("<Return>", self.delete)
        self.btn_delete.bind("<ButtonRelease-1>", self.delete)

        # ====== Location Details ======
        loc_frame = ctk.CTkFrame(self.root)
        loc_frame.place(x=700, y=100, width=500, height=500)

        self.style.configure("Treeview", background="#3c3c3c", foreground="white", fieldbackground="#333333",
                             rowheight=30,
                             font=("Arial", 17))
        self.style.map("Treeview", background=[("selected", "#0078D7")])
        self.style.configure("Treeview.Heading", font=('Bell Gothic Std Black', 17))
        self.style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])  # Remove the borders

        self.locationTable = ttk.Treeview(loc_frame, style="Treeview", columns=("lid", "name", "address"))
        for column in self.locationTable["columns"]:
            self.locationTable.column(column, anchor=CENTER)

        scrolly = ctk.CTkScrollbar(loc_frame, orientation=VERTICAL, command=self.locationTable.yview)
        scrolly.pack(side=RIGHT, fill=Y)
        self.locationTable.configure(yscrollcommand=scrolly.set)

        scrollx = ctk.CTkScrollbar(loc_frame, orientation=HORIZONTAL, command=self.locationTable.xview)
        scrollx.pack(side=BOTTOM, fill=X)
        self.locationTable.configure(xscrollcommand=scrollx.set)

        self.locationTable.heading("lid", text="Location ID")
        self.locationTable.heading("name", text="Name")
        self.locationTable.heading("address", text="Address")

        self.locationTable["show"] = "headings"

        self.locationTable.column("lid", width=60, minwidth=60)
        self.locationTable.column("name", width=100, minwidth=100)
        self.locationTable.column("address", width=100)

        self.locationTable.pack(fill=BOTH, expand=1)

        self.locationTable.bind("<ButtonRelease-1>", self.get_data)
        self.show()

    # ========================= Functions ==============================

    def add(self, e):
        con = sqlite3.connect(database=r'std.db')
        cur = con.cursor()
        try:
            if self.var_name.get() == "":
                messagebox.showerror("Error", "Location Name must be required", parent=self.root)
            else:
                cur.execute("SELECT * FROM locations WHERE name=?", (self.var_name.get(),))
                row = cur.fetchone()
                if row is not None:
                    messagebox.showerror("Error", "Location already present, try different", parent=self.root)
                else:
                    cur.execute("INSERT INTO locations(name, address) values(?,?)",
                                (self.var_name.get(), self.address.get()))
                    con.commit()
                    messagebox.showinfo("Success", "Location Added Successfully", parent=self.root)
                    self.show()
                    self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def show(self):
        con = sqlite3.connect(database=r'std.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM locations")
            rows = cur.fetchall()
            self.locationTable.delete(*self.locationTable.get_children())
            for row in rows:
                self.locationTable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def clear(self):
        self.var_loc_id.set("")
        self.var_name.set("")
        self.address.set("")

    def get_data(self, ev):
        try:
            f = self.locationTable.focus()
            content = (self.locationTable.item(f))
            row = content['values']
            self.var_loc_id.set(row[0])
            self.var_name.set(row[1])
            self.address.set(row[2])
        except (Exception,):
            pass

    def delete(self, e):
        con = sqlite3.connect(database=r'std.db')
        cur = con.cursor()
        try:
            if self.var_loc_id.get() == "":
                messagebox.showerror("Error", "Please Select Location From The List", parent=self.root)
            else:
                cur.execute("SELECT * FROM locations WHERE lid=?", (self.var_loc_id.get(),))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Error, Please try Again", parent=self.root)
                else:
                    op = messagebox.askyesno("Confirm", "Do you really want to delete?", parent=self.root)
                    if op is True:
                        cur.execute("DELETE FROM locations WHERE lid=?", (self.var_loc_id.get(),))
                        con.commit()
                        messagebox.showinfo("Delete", "Location Deleted Successfully", parent=self.root)
                        self.show()
                        self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)


if __name__ == "__main__":
    root = ctk.CTk()
    obj = locationClass(root)
    root.mainloop()
