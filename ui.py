import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from pdf_generator import create_pdf  # Import the create_pdf function

class InvoiceApp:
    def __init__(self, root):
        self.root = root
        root.title("Deep Discount Comics Invoice Generator")

        # Invoice Month
        ttk.Label(root, text="Invoice Month:").grid(row=0, column=0, padx=10, pady=5)
        self.month_entry = ttk.Entry(root)
        self.month_entry.grid(row=0, column=1, padx=10, pady=5)

        # Pre-Orders Section
        ttk.Label(root, text="Pre-Orders:").grid(row=1, column=0, padx=10, pady=5)
        self.pre_orders_text = tk.Text(root, height=10, width=50)
        self.pre_orders_text.grid(row=1, column=1, padx=10, pady=5)

        # Pre-Orders Bags and Boards
        ttk.Label(root, text="Pre-Orders Bag & Board Qty:").grid(row=1, column=2, padx=10, pady=5)
        self.pre_orders_bag_board_qty = ttk.Entry(root)
        self.pre_orders_bag_board_qty.grid(row=1, column=3, padx=10, pady=5)

        # FOC Adds Section
        ttk.Label(root, text="FOC Adds:").grid(row=2, column=0, padx=10, pady=5)
        self.foc_adds_text = tk.Text(root, height=10, width=50)
        self.foc_adds_text.grid(row=2, column=1, padx=10, pady=5)

        # FOC Adds Bags and Boards
        ttk.Label(root, text="FOC Adds Bag & Board Qty:").grid(row=2, column=2, padx=10, pady=5)
        self.foc_adds_bag_board_qty = ttk.Entry(root)
        self.foc_adds_bag_board_qty.grid(row=2, column=3, padx=10, pady=5)

        # Credits Section
        ttk.Label(root, text="Credits:").grid(row=3, column=0, padx=10, pady=5)
        self.credits_text = tk.Text(root, height=10, width=50)
        self.credits_text.grid(row=3, column=1, padx=10, pady=5)

        # Credits Bags and Boards
        ttk.Label(root, text="Credits Bag & Board Qty:").grid(row=3, column=2, padx=10, pady=5)
        self.credits_bag_board_qty = ttk.Entry(root)
        self.credits_bag_board_qty.grid(row=3, column=3, padx=10, pady=5)

        # Bags and Boards
        ttk.Label(root, text="Bags and Boards Type:").grid(row=4, column=0, padx=10, pady=5)
        self.bag_board_option = tk.StringVar()
        self.bag_board_options = ["None", "Current Size BCW Bag & Board", "Mylites2 with Half Back", "Mylites 2 with Full Back"]
        self.bag_board_option.set(self.bag_board_options[0])
        self.bag_board_menu = ttk.OptionMenu(root, self.bag_board_option, *self.bag_board_options)
        self.bag_board_menu.grid(row=4, column=1, padx=10, pady=5)

        # Shipping
        ttk.Label(root, text="Shipping:").grid(row=5, column=0, padx=10, pady=5)
        self.shipping_option = tk.StringVar()
        self.shipping_options = ["Local Pick Up", "Monthly Shipping", "Twice Monthly", "Weekly"]
        self.shipping_option.set(self.shipping_options[0])
        self.shipping_menu = ttk.OptionMenu(root, self.shipping_option, *self.shipping_options)
        self.shipping_menu.grid(row=5, column=1, padx=10, pady=5)

        # Sales Tax
        ttk.Label(root, text="Sales Tax:").grid(row=6, column=0, padx=10, pady=5)
        self.sales_tax_option = tk.BooleanVar()
        self.sales_tax_option.set(False)
        ttk.Checkbutton(root, text="Apply 5% Sales Tax", variable=self.sales_tax_option).grid(row=6, column=1, padx=10, pady=5)

        # Folder Selection Button
        ttk.Button(root, text="Select Folder", command=self.select_folder).grid(row=7, column=0, padx=10, pady=10)
        self.folder_path = tk.StringVar()

        # Display selected folder path
        ttk.Label(root, textvariable=self.folder_path).grid(row=7, column=1, padx=10, pady=10)

        # Generate Invoice Button
        ttk.Button(root, text="Generate Invoice", command=self.generate_invoice).grid(row=8, column=0, columnspan=2, padx=10, pady=10)

    def select_folder(self):
        folder_selected = filedialog.askdirectory()
        self.folder_path.set(folder_selected)
        print(f"Selected folder: {folder_selected}")

    def generate_invoice(self):
        month = self.month_entry.get()
        pre_orders = self.pre_orders_text.get("1.0", tk.END).strip().split('\n')
        pre_orders_bag_board_qty = int(self.pre_orders_bag_board_qty.get() or 0)
        foc_adds = self.foc_adds_text.get("1.0", tk.END).strip().split('\n')
        foc_adds_bag_board_qty = int(self.foc_adds_bag_board_qty.get() or 0)
        credits = self.credits_text.get("1.0", tk.END).strip().split('\n')
        credits_bag_board_qty = int(self.credits_bag_board_qty.get() or 0)
        bag_board_type = self.bag_board_option.get()
        shipping_type = self.shipping_option.get()
        apply_sales_tax = self.sales_tax_option.get()
        folder_path = self.folder_path.get()

        if not folder_path:
            print("No folder selected.")
            return

        # Generate the PDF
        create_pdf(month, pre_orders, pre_orders_bag_board_qty, foc_adds, foc_adds_bag_board_qty, credits, credits_bag_board_qty, bag_board_type, shipping_type, apply_sales_tax, folder_path)

if __name__ == "__main__":
    root = tk.Tk()
    app = InvoiceApp(root)
    root.mainloop()