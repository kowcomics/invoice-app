from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
import os
from styles import get_styles, get_table_style

def create_pdf(month, pre_orders, pre_orders_bag_board_qty, foc_adds, foc_adds_bag_board_qty, credits, credits_bag_board_qty, bag_board_type, shipping_type, apply_sales_tax, folder_path):
    # Define the output folder
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    file_path = os.path.join(folder_path, f"{month}_invoice.pdf")
    pdf = SimpleDocTemplate(file_path, pagesize=letter)
    elements = []
    styles, item_style, cell_style, header_style = get_styles()

    # Add header
    header = Paragraph(f"Deep Discount Comics Invoice - {month}", styles['Title'])
    elements.append(header)
    elements.append(Spacer(1, 12))

    # Add Pre-Orders
    pre_orders_header = Paragraph("Pre-Orders", header_style)
    elements.append(pre_orders_header)
    elements.append(Spacer(1, 12))

    table_data = [["ITEM", "QTY", "DESCRIPTION", "PRICE", "EXT"]]
    pre_orders_subtotal = 0
    for order in pre_orders:
        try:
            parts = order.split('\t')
            if len(parts) != 4:
                raise ValueError("Incorrect number of fields")
            item_code, qty, description, price = parts
            qty = int(qty.strip())
            price = float(price.strip().replace('$', ''))
            ext = qty * price
            pre_orders_subtotal += ext
            description_para = Paragraph(description.strip(), cell_style)
            table_data.append([Paragraph(item_code.strip(), item_style), qty, description_para, f"${price:.2f}", f"${ext:.2f}"])
        except ValueError:
            print(f"Skipping malformed line: {order}")

    invoice_table = Table(table_data, colWidths=[100, 50, 200, 60, 60])
    invoice_table.setStyle(TableStyle(get_table_style()))
    elements.append(invoice_table)
    elements.append(Spacer(1, 12))

    # Add FOC Adds
    foc_header = Paragraph("FOC or Special Order Additions", header_style)
    elements.append(foc_header)
    elements.append(Spacer(1, 12))

    foc_table_data = [["ITEM", "QTY", "DESCRIPTION", "PRICE", "EXT"]]
    foc_subtotal = 0
    for order in foc_adds:
        try:
            parts = order.split('\t')
            if len(parts) != 4:
                raise ValueError("Incorrect number of fields")
            item_code, qty, description, price = parts
            qty = int(qty.strip())
            price = float(price.strip().replace('$', ''))
            ext = qty * price
            foc_subtotal += ext
            description_para = Paragraph(description.strip(), cell_style)
            foc_table_data.append([Paragraph(item_code.strip(), item_style), qty, description_para, f"${price:.2f}", f"${ext:.2f}"])
        except ValueError:
            print(f"Skipping malformed line: {order}")

    if len(foc_table_data) > 1:
        foc_table = Table(foc_table_data, colWidths=[100, 50, 200, 60, 60])
        foc_table.setStyle(TableStyle(get_table_style()))
        elements.append(foc_table)
        elements.append(Spacer(1, 12))

    # Initialize bag and board totals
    pre_orders_bags_board_total = 0
    foc_adds_bags_board_total = 0
    credits_bags_board_total = 0

    # Add Credits
    credits_header = Paragraph("Credits", header_style)
    elements.append(credits_header)
    elements.append(Spacer(1, 12))

    credits_table_data = [["ITEM", "QTY", "DESCRIPTION", "PRICE", "EXT"]]
    credits_subtotal = 0
    for order in credits:
        try:
            parts = order.split('\t')
            if len(parts) != 4:
                raise ValueError("Incorrect number of fields")
            item_code, qty, description, price = parts
            qty = int(qty.strip())
            price = float(price.strip().replace('$', ''))
            ext = qty * price
            credits_subtotal += ext
            description_para = Paragraph(description.strip(), cell_style)
            credits_table_data.append([Paragraph(item_code.strip(), item_style), qty, description_para, f"${price:.2f}", f"-${ext:.2f}"])
        except ValueError:
            print(f"Skipping malformed line: {order}")

    if len(credits_table_data) > 1:
        credits_table = Table(credits_table_data, colWidths=[100, 50, 200, 60, 60])
        credits_table.setStyle(TableStyle(get_table_style()))
        elements.append(credits_table)
        elements.append(Spacer(1, 12))

    credits_subtotal += credits_bags_board_total if bag_board_type != 'None' else 0

    # Add Bags and Boards
    if bag_board_type != 'None':
        bags_board_price = {"None": 0.00, "Current Size BCW Bag & Board": 0.15, "Mylites2 with Half Back": 0.40, "Mylites 2 with Full Back": 0.50}
        pre_orders_bags_board_total = bags_board_price[bag_board_type] * pre_orders_bag_board_qty
        foc_adds_bags_board_total = bags_board_price[bag_board_type] * foc_adds_bag_board_qty
        credits_bags_board_total = bags_board_price[bag_board_type] * credits_bag_board_qty

        bags_boards_data = [["Bags and Boards", pre_orders_bag_board_qty, f"${bags_board_price[bag_board_type]:.2f}", f"${pre_orders_bags_board_total:.2f}"]]
        if foc_adds and any(foc_adds):
            bags_boards_data.append(["FOC Adds Bags and Boards", foc_adds_bag_board_qty, f"${bags_board_price[bag_board_type]:.2f}", f"${foc_adds_bags_board_total:.2f}"])
        if credits and any(credits):
            bags_boards_data.append(["Credits Bags and Boards", credits_bag_board_qty, f"${bags_board_price[bag_board_type]:.2f}", f"-${credits_bags_board_total:.2f}"])

        if len(bags_boards_data) > 1:
            bags_boards_table = Table(bags_boards_data, colWidths=[320, 60, 80, 80])
            bags_boards_table.setStyle(TableStyle(get_table_style()))
            elements.append(bags_boards_table)
            elements.append(Spacer(1, 12))

    # Add Shipping
    if shipping_type != "Local Pick Up":
        shipping_price = {"Local Pick Up": 0.00, "Monthly Shipping": 7.50, "Twice Monthly": 15.00, "Weekly": 23.00}
        shipping_total = shipping_price[shipping_type]
        shipping_table = Table([["Shipping", 1, f"${shipping_total:.2f}", f"${shipping_total:.2f}"]], colWidths=[320, 60, 80, 80])
        shipping_table.setStyle(TableStyle(get_table_style()))
        elements.append(shipping_table)
        elements.append(Spacer(1, 12))
    else:
        shipping_total = 0.00

    # Add Subtotals
    subtotals_data = []
    if pre_orders_subtotal > 0:
        subtotals_data.append(["Pre-Orders Subtotal", f"${pre_orders_subtotal:.2f}"])
    if foc_subtotal > 0:
        subtotals_data.append(["FOC Subtotal", f"${foc_subtotal:.2f}"])
    if pre_orders_bags_board_total + foc_adds_bags_board_total > 0:
        subtotals_data.append(["Bags and Boards Subtotal", f"${pre_orders_bags_board_total + foc_adds_bags_board_total:.2f}"])

    if subtotals_data:
        subtotals_table = Table(subtotals_data, colWidths=[320, 60, 80, 80])
        subtotals_table.setStyle(TableStyle(get_table_style()))
        elements.append(subtotals_table)
        elements.append(Spacer(1, 12))

    # Add underline beneath the subtotal of bags and boards
    if pre_orders_bags_board_total + foc_adds_bags_board_total > 0:
        elements.append(Spacer(1, 6))
        elements.append(Paragraph("<u></u>", styles['Normal']))
        elements.append(Spacer(1, 6))

    # Calculate New Item Total
    new_item_total = pre_orders_subtotal + foc_subtotal + (pre_orders_bags_board_total + foc_adds_bags_board_total if pre_orders_bags_board_total + foc_adds_bags_board_total > 0 else 0)
    new_item_total_data = [["New Item Total", f"${new_item_total:.2f}"]]
    new_item_total_table = Table(new_item_total_data, colWidths=[320, 60, 80, 80])
    new_item_total_table.setStyle(TableStyle(get_table_style()))
    elements.append(new_item_total_table)
    elements.append(Spacer(1, 12))

    # Add line beneath New Item Total
    elements.append(Spacer(1, 6))
    elements.append(Paragraph("<u></u>", styles['Normal']))
    elements.append(Spacer(1, 6))

    # Add Credit Item Subtotal
    credit_item_subtotal_data = [["Credit Item Subtotal", f"-${credits_subtotal:.2f}"]]
    credit_item_subtotal_table = Table(credit_item_subtotal_data, colWidths=[320, 60, 80, 80])
    credit_item_subtotal_table.setStyle(TableStyle(get_table_style()))
    elements.append(credit_item_subtotal_table)
    elements.append(Spacer(1, 12))

    # Add Credit Bag and Board (if applicable)
    if credits_bags_board_total > 0:
        credit_bag_board_data = [["Credit Bag and Board", f"-${credits_bags_board_total:.2f}"]]
        credit_bag_board_table = Table(credit_bag_board_data, colWidths=[320, 60, 80, 80])
        credit_bag_board_table.setStyle(TableStyle(get_table_style()))
        elements.append(credit_bag_board_table)
        elements.append(Spacer(1, 12))

    # Add Credit Item Total
    credit_item_total = credits_subtotal + (credits_bags_board_total if credits_bags_board_total > 0 else 0)
    credit_item_total_data = [["Credit Item Total", f"-${credit_item_total:.2f}"]]
    credit_item_total_table = Table(credit_item_total_data, colWidths=[320, 60, 80, 80])
    credit_item_total_table.setStyle(TableStyle(get_table_style()))
    elements.append(credit_item_total_table)
    elements.append(Spacer(1, 12))

    # Add Sales Tax (if applicable)
    tax = new_item_total * 0.05 if apply_sales_tax else 0.00
    if apply_sales_tax:
        tax_data = [["Sales Tax", f"${tax:.2f}"]]
        tax_table = Table(tax_data, colWidths=[320, 60, 80, 80])
        tax_table.setStyle(TableStyle(get_table_style()))
        elements.append(tax_table)
        elements.append(Spacer(1, 12))

    # Add double line
    elements.append(Spacer(1, 6))
    elements.append(Paragraph("<u></u>", styles['Normal']))
    elements.append(Spacer(1, 6))
    elements.append(Paragraph("<u></u>", styles['Normal']))
    elements.append(Spacer(1, 6))

    # Calculate Total
    total = new_item_total - credit_item_total + tax
    total_data = [["Total", f"${total:.2f}"]]
    total_table = Table(total_data, colWidths=[320, 60, 80, 80])
    total_table.setStyle(TableStyle(get_table_style()))
    elements.append(total_table)
    elements.append(Spacer(1, 12))

    # Add summary
    summary = f"Thank you for your business! Total Amount Due: ${total:.2f}"
    summary_para = Paragraph(summary, cell_style)
    elements.append(summary_para)

    # Build the PDF
    pdf.build(elements)
    print(f"Invoice generated: {file_path}")