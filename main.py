from tkinter import *
import customtkinter as ctk
from PIL import ImageTk, Image
from employee import employeeClass
from category import categoryClass
from locations import locationClass
from addCustomers import Customers
from product import productClass
from billing import BillClass
from customerBilling import customersBilling
from returned_items import returnedItems
from summary import allSummary
from shopExpenses import shopExpenses


class stockManagement:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1425x700+50+20")
        self.root.title("Sindh Traders")

        self.root.protocol("WM_DELETE_WINDOW", self.root.quit)

        ctk.set_appearance_mode("light")  # Modes: system (default), light, dark
        ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

        # ===== Background Image =====
        self.bgFrame = Frame()
        self.bgFrame.place(relwidth=1, relheight=1)
        self.bg = Image.open("images/bg2.png")
        self.bg = self.bg.resize((1920, 1080), Image.LANCZOS)
        self.bg = ImageTk.PhotoImage(self.bg)
        self.bgImage = Label(self.bgFrame, image=self.bg).place(x=0, y=0, relwidth=1, relheight=1)

        # ===== Icon image =====
        icon = PhotoImage(file='images/logo.png')
        self.root.iconphoto(False, icon)

        # ====== Title =======
        self.titleFrame = ctk.CTkFrame(self.root, bg_color="#eeba2b", corner_radius=5)
        self.titleFrame.pack(side=TOP, fill=X)
        self.title = ctk.CTkLabel(self.titleFrame, text="Sindh Traders", bg_color="#eeba2b", text_color="#fff",
                                  font=("Brush Script MT", 70, "bold"), anchor="n")
        self.title.pack(side=TOP, fill=X)

        # ===== Logo Image =====
        # self.logo = ImageTk.PhotoImage(file="images/logoB.png")
        # self.logoImage = Label(self.root, image=self.logo).place(x=5, y=5, width=120, height=80)

        # ===== Menu Bar =====
        foregroundColor = '#0e0d0b'
        fontColor = "#fff"
        hoverColor = '#1e1f22'
        textColor = "#fff"
        borderColor = "#e6b42b"
        self.lbl_menu = Frame(bg="#fff")
        self.lbl_menu.pack(side=TOP, fill=X, ipady=20)

        self.btnEmployee = ctk.CTkButton(self.lbl_menu, text="EMPLOYEE", command=self.employee, border_width=2,
                                         font=("times new roman", 15, "bold"), fg_color=foregroundColor,
                                         hover_color=hoverColor, text_color=fontColor, border_color=borderColor, corner_radius=5, cursor="hand2")
        self.btnEmployee.place(x=5, y=5, width=130, height=30)

        self.btnCategory = ctk.CTkButton(self.lbl_menu, text="CATEGORY", command=self.category, border_width=2,
                                         font=("times new roman", 15, "bold"), fg_color=foregroundColor,
                                         hover_color=hoverColor, text_color=fontColor, border_color=borderColor, corner_radius=5, cursor="hand2")
        self.btnCategory.place(x=110, y=5, width=130, height=30)

        self.btnLocation = ctk.CTkButton(self.lbl_menu, text="LOCATIONS", command=self.location, border_width=2,
                                         font=("times new roman", 15, "bold"), fg_color=foregroundColor,
                                         hover_color=hoverColor, text_color=fontColor, border_color=borderColor, corner_radius=5, cursor="hand2")
        self.btnLocation.place(x=215, y=5, width=130, height=30)

        self.btnAddCustomers = ctk.CTkButton(self.lbl_menu, text="ADD CUSTOMERS", command=self.AddCustomers,
                                             border_width=2,
                                             font=("times new roman", 15, "bold"), fg_color=foregroundColor,
                                             hover_color=hoverColor, text_color=fontColor, border_color=borderColor, corner_radius=5, cursor="hand2")
        self.btnAddCustomers.place(x=320, y=5, width=180, height=30)

        self.btnProduct = ctk.CTkButton(self.lbl_menu, text="PRODUCT", command=self.product, border_width=2,
                                        font=("times new roman", 15, "bold"), fg_color=foregroundColor,
                                        hover_color=hoverColor, text_color=fontColor, border_color=borderColor, corner_radius=5, cursor="hand2")
        self.btnProduct.place(x=465, y=5, width=110, height=30)

        self.btnBilling = ctk.CTkButton(self.lbl_menu, text="BILLING", command=self.billing, border_width=2,
                                        font=("times new roman", 15, "bold"), fg_color=foregroundColor,
                                        hover_color=hoverColor, text_color=fontColor, border_color=borderColor, corner_radius=5, cursor="hand2")
        self.btnBilling.place(x=554, y=5, width=90, height=30)

        self.btnCustomersBilling = ctk.CTkButton(self.lbl_menu, text="PAYMENT RECOVERY", command=self.paymentRecovery,
                                                 border_width=2,
                                                 font=("times new roman", 15, "bold"), fg_color=foregroundColor,
                                                 hover_color=hoverColor, text_color=fontColor, border_color=borderColor, corner_radius=5, cursor="hand2")
        self.btnCustomersBilling.place(x=628, y=5, width=220, height=30)

        self.btnReturnedItems = ctk.CTkButton(self.lbl_menu, text="RETURN", command=self.returnedItem, border_width=2,
                                              font=("times new roman", 15, "bold"), fg_color=foregroundColor,
                                              hover_color=hoverColor, text_color=fontColor, border_color=borderColor, corner_radius=5, cursor="hand2")
        self.btnReturnedItems.place(x=805, y=5, width=90, height=30)

        self.btnSummary = ctk.CTkButton(self.lbl_menu, text="SUMMARY", command=self.summary, border_width=2,
                                        font=("times new roman", 15, "bold"), fg_color=foregroundColor,
                                        hover_color=hoverColor, text_color=fontColor, border_color=borderColor, corner_radius=5, cursor="hand2")
        self.btnSummary.place(x=878, y=5, width=110, height=30)

        self.btnExpenses = ctk.CTkButton(self.lbl_menu, text="EXPENSES", command=self.expenses, border_width=2,
                                         font=("times new roman", 15, "bold"), fg_color=foregroundColor,
                                         hover_color=hoverColor, text_color=fontColor, border_color=borderColor, corner_radius=5, cursor="hand2")
        self.btnExpenses.place(x=968, y=5, width=110, height=30)

    def employee(self):
        self.emp_win = ctk.CTkToplevel(self.root)
        self.emp_obj = employeeClass(self.emp_win)

    def category(self):
        self.cat_win = ctk.CTkToplevel(self.root)
        self.cat_obj = categoryClass(self.cat_win)

    def location(self):
        self.loc_win = ctk.CTkToplevel(self.root)
        self.loc_obj = locationClass(self.loc_win)

    def AddCustomers(self):
        self.add_cust_win = ctk.CTkToplevel(self.root)
        self.add_cust_obj = Customers(self.add_cust_win)

    def product(self):
        self.prod_win = ctk.CTkToplevel(self.root)
        self.prod_obj = productClass(self.prod_win)

    def billing(self):
        self.bill_win = ctk.CTkToplevel(self.root)
        self.bill_obj = BillClass(self.bill_win)

    def paymentRecovery(self):
        self.recovery_win = ctk.CTkToplevel(self.root)
        self.recovery_obj = customersBilling(self.recovery_win)

    def returnedItem(self):
        self.return_win = ctk.CTkToplevel(self.root)
        self.return_obj = returnedItems(self.return_win)

    def summary(self):
        self.summary_win = ctk.CTkToplevel(self.root)
        self.summary_obj = allSummary(self.summary_win)

    def expenses(self):
        self.expenses_win = ctk.CTkToplevel(self.root)
        self.expenses_obj = shopExpenses(self.expenses_win)


if __name__ == "__main__":
    root = ctk.CTk()
    obj = stockManagement(root)
    root.mainloop()

# Software By Usman Amjad(UA)
