import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import os

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

        # Bags and Boards
        ttk.Label(root, text="Bags and Boards Type:").grid(row=2, column=0, padx=10, pady=5)
        self.bag_board_option = tk.StringVar()
        self.bag_board_options = ["None", "Current Size BCW Bag & Board", "Mylites2 with Half Back", "Mylites 2 with Full Back"]
        self.bag_board_option.set(self.bag_board_options[1])
        ttk.OptionMenu(root, self.bag_board_option, *self.bag_board_options).grid(row=2, column=1, padx=10, pady=5)

        # Shipping
        ttk.Label(root, text="Shipping:").grid(row=3, column=0, padx=10, pady=5)
        self.shipping_option = tk.StringVar()
        self.shipping_options = ["Local Pick Up", "Monthly Shipping", "Twice Monthly", "Weekly"]
        self.shipping_option.set(self.shipping_options[3])
        ttk.OptionMenu(root, self.shipping_option, *self.shipping_options).grid(row=3, column=1, padx=10, pady=5)

        # Sales Tax
        ttk.Label(root, text="Sales Tax:").grid(row=4, column=0, padx=10, pady=5)
        self.sales_tax_option = tk.BooleanVar()
        self.sales_tax_option.set(False)
        ttk.Checkbutton(root, text="Apply 5% Sales Tax", variable=self.sales_tax_option).grid(row=4, column=1, padx=10, pady=5)

        # Folder Selection Button
        ttk.Button(root, text="Select Folder", command=self.select_folder).grid(row=5, column=0, padx=10, pady=10)
        self.folder_path = tk.StringVar()

        # Display selected folder path
        ttk.Label(root, textvariable=self.folder_path).grid(row=5, column=1, padx=10, pady=10)

        # Generate Invoice Button
        ttk.Button(root, text="Generate Invoice", command=self.generate_invoice).grid(row=6, column=0, columnspan=2, padx=10, pady=10)

    def select_folder(self):
        folder_selected = filedialog.askdirectory()
        self.folder_path.set(folder_selected)
        print(f"Selected folder: {folder_selected}")

    def generate_invoice(self):
        month = self.month_entry.get()
        pre_orders = self.pre_orders_text.get("1.0", tk.END).strip().split('\n')
        pre_orders_bag_board_qty = int(self.pre_orders_bag_board_qty.get())
        bag_board_type = self.bag_board_option.get()
        shipping_type = self.shipping_option.get()
        apply_sales_tax = self.sales_tax_option.get()
        folder_path = self.folder_path.get()

        if not folder_path:
            print("No folder selected.")
            return

        # Placeholder for PDF generation
        self.create_pdf(month, pre_orders, pre_orders_bag_board_qty, bag_board_type, shipping_type, apply_sales_tax, folder_path)

    def create_pdf(self, month, pre_orders, pre_orders_bag_board_qty, bag_board_type, shipping_type, apply_sales_tax, folder_path):
        # Define the output folder
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        file_path = os.path.join(folder_path, f"{month}_invoice.pdf")
        pdf = SimpleDocTemplate(file_path, pagesize=letter)
        elements = []
        styles = getSampleStyleSheet()
        
        # Add header
        header = Paragraph(f"Deep Discount Comics Invoice - {month}", styles['Title'])
        elements.append(header)
        elements.append(Spacer(1, 12))

        # Add Pre-Orders
        table_data = [["ITEM", "QTY", "DESCRIPTION", "PRICE", "EXT"]]
        for order in pre_orders:
            try:
                item_code, qty, description, price = order.split('\t')
                qty = int(qty.strip())
                price = float(price.strip().replace('$', ''))
                ext = qty * price
                description_para = Paragraph(description.strip(), styles['Normal'])
                table_data.append([item_code.strip(), qty, description_para, f"${price:.2f}", f"${ext:.2f}"])
            except ValueError:
                print(f"Skipping malformed line: {order}")

        invoice_table = Table(table_data, colWidths=[100, 50, 200, 60, 60])
        invoice_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ]))
        elements.append(invoice_table)
        elements.append(Spacer(1, 12))

        # Add Bags and Boards
        bags_board_price = {"None": 0.00, "Current Size BCW Bag & Board": 0.15, "Mylites2 with Half Back": 0.40, "Mylites 2 with Full Back": 0.50}
        pre_orders_bags_board_total = bags_board_price[bag_board_type] * pre_orders_bag_board_qty
        bags_boards_table = Table(
            [["Bags and Boards", pre_orders_bag_board_qty, f"${bags_board_price[bag_board_type]: .2f}", f"${pre_orders_bags_board_total:.2f}"]], 
            colWidths=[320, 60, 80, 80]
        )
        elements.append(bags_boards_table)
        elements.append(Spacer(1, 12))

        # Add Shipping
        shipping_price = {"Local Pick Up": 0.00, "Monthly Shipping": 7.50, "Twice Monthly": 15.00, "Weekly": 23.00}
        shipping_total = shipping_price[shipping_type]
        shipping_table = Table([["Shipping", 1, f"${shipping_total:.2f}", f"${shipping_total:.2f}"]], colWidths=[320, 60, 80, 80])
        elements.append(shipping_table)
        elements.append(Spacer(1, 12))

        # Add Subtotal, Total and Sales Tax
        subtotal = sum(float(row[-1][1:]) for row in table_data[1:]) + pre_orders_bags_board_total + shipping_total
        tax = subtotal * 0.05 if apply_sales_tax else 0.00
        total = subtotal + tax
        totals_table = Table([["Subtotal", f"${subtotal:.2f}"], ["Tax", f"${tax:.2f}"], ["Total", f"${total:.2f}"]], colWidths=[400, 140])
        elements.append(totals_table)
        elements.append(Spacer(1, 12))

        # Build the PDF
        pdf.build(elements)
        print(f"Invoice generated: {file_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = InvoiceApp(root)
    root.mainloop()
