from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
import os

def create_pdf(month, pre_orders, pre_orders_bag_board_qty, foc_adds, foc_adds_bag_board_qty, credits, credits_bag_board_qty, bag_board_type, shipping_type, apply_sales_tax, folder_path):
    # Define the output folder
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    file_path = os.path.join(folder_path, f"{month}_invoice.pdf")
    pdf = SimpleDocTemplate(file_path, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()

    # Custom styles with Helvetica font
    title_style = ParagraphStyle(name='TitleStyle', fontSize=16, alignment=1, fontName='Helvetica-Bold', spaceAfter=12)
    section_header_style = ParagraphStyle(name='SectionHeaderStyle', fontSize=12, fontName='Helvetica-Bold', spaceAfter=8)
    table_header_style = ParagraphStyle(name='TableHeaderStyle', fontSize=7, fontName='Helvetica-Bold', textColor=colors.white)
    cell_style = ParagraphStyle(name='CellStyle', fontSize=7, fontName='Helvetica', wordWrap='LTR')

    # Add Title
    title = Paragraph(f"Invoice for {month}", title_style)
    elements.append(title)
    elements.append(Spacer(1, 12))

    # Add Pre-Orders Section
    elements.append(Paragraph("Pre-Orders", section_header_style))
    elements.append(Spacer(1, 6))

    pre_orders_table_data = [["ITEM", "QTY", "DESCRIPTION", "PRICE", "EXT"]]
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
            pre_orders_table_data.append([
                Paragraph(item_code.strip(), cell_style),  # Apply cell_style to ITEM
                Paragraph(str(qty), cell_style),          # Apply cell_style to QTY
                Paragraph(description.strip(), cell_style),  # Apply cell_style to DESCRIPTION
                Paragraph(f"${price:.2f}", cell_style),   # Apply cell_style to PRICE
                Paragraph(f"${ext:.2f}", cell_style)      # Apply cell_style to EXT
            ])
        except ValueError:
            print(f"Skipping malformed line: {order}")

    pre_orders_table = Table(pre_orders_table_data, colWidths=[80, 40, 200, 60, 60])
    pre_orders_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 7),  # Updated font size to 7
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),  # Adjust padding for dynamic row height
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
    ]))
    elements.append(pre_orders_table)
    elements.append(Spacer(1, 12))

    # Add FOC Adds Section
    elements.append(Paragraph("FOC or Special Order Additions", section_header_style))
    elements.append(Spacer(1, 6))

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
            foc_table_data.append([
                Paragraph(item_code.strip(), cell_style),  # Apply cell_style to ITEM
                Paragraph(str(qty), cell_style),          # Apply cell_style to QTY
                Paragraph(description.strip(), cell_style),  # Apply cell_style to DESCRIPTION
                Paragraph(f"${price:.2f}", cell_style),   # Apply cell_style to PRICE
                Paragraph(f"${ext:.2f}", cell_style)      # Apply cell_style to EXT
            ])
        except ValueError:
            print(f"Skipping malformed line: {order}")

    foc_table = Table(foc_table_data, colWidths=[80, 40, 200, 60, 60])
    foc_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 7),  # Updated font size to 7
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),  # Adjust padding for dynamic row height
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
    ]))
    elements.append(foc_table)
    elements.append(Spacer(1, 12))

    # Add Credits Section
    elements.append(Paragraph("Credits", section_header_style))
    elements.append(Spacer(1, 6))

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
            credits_table_data.append([
                Paragraph(item_code.strip(), cell_style),  # Apply cell_style to ITEM
                Paragraph(str(qty), cell_style),          # Apply cell_style to QTY
                Paragraph(description.strip(), cell_style),  # Apply cell_style to DESCRIPTION
                Paragraph(f"${price:.2f}", cell_style),   # Apply cell_style to PRICE
                Paragraph(f"-${ext:.2f}", cell_style)      # Apply cell_style to EXT
            ])
        except ValueError:
            print(f"Skipping malformed line: {order}")

    credits_table = Table(credits_table_data, colWidths=[80, 40, 200, 60, 60])
    credits_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 7),  # Updated font size to 7
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),  # Adjust padding for dynamic row height
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
    ]))
    elements.append(credits_table)
    elements.append(Spacer(1, 12))

    # Bags and Boards Pricing
    bags_board_price = {
        "None": 0.00,
        "Current Size BCW Bag & Board": 0.15,
        "Mylites2 with Half Back": 0.40,
        "Mylites 2 with Full Back": 0.50
    }

    # Ensure bag_board_type is valid
    bag_board_price = bags_board_price.get(bag_board_type, 0.00)

    # Calculate Bags and Boards Totals
    pre_orders_bags_board_total = bag_board_price * pre_orders_bag_board_qty
    foc_adds_bags_board_total = bag_board_price * foc_adds_bag_board_qty
    credits_bags_board_total = bag_board_price * credits_bag_board_qty

    # Total Bags and Boards
    bags_boards_total = pre_orders_bags_board_total + foc_adds_bags_board_total
    bag_board_credits_total = credits_bags_board_total

    # Calculate Subtotal
    subtotal = pre_orders_subtotal + foc_subtotal - credits_subtotal

    # Calculate Taxable Subtotal
    taxable_subtotal = subtotal + bags_boards_total - bag_board_credits_total

    # Calculate Shipping Charges
    shipping_price = {"Local Pick Up": 0.00, "Monthly Shipping": 7.50, "Twice Monthly": 15.00, "Weekly": 23.00}
    shipping_total = shipping_price.get(shipping_type, 0.00)

    # Calculate Tax
    tax = taxable_subtotal * 0.05 if apply_sales_tax else 0.00

    # Calculate Total
    total = taxable_subtotal + shipping_total + tax

    # Add Totals Summary
    summary_data = [
        ["Pre-Orders Subtotal", f"${pre_orders_subtotal:.2f}"],
        ["FOC Subtotal", f"${foc_subtotal:.2f}"],
        ["Credits Subtotal", f"-${credits_subtotal:.2f}"],
        ["Bags and Boards", f"${bags_boards_total:.2f}"],
        ["Bag and Board Credits", f"-${bag_board_credits_total:.2f}"],
        ["Shipping Charges", f"${shipping_total:.2f}"],
        ["Tax (5%)", f"${tax:.2f}" if apply_sales_tax else "$0.00"],
        ["Total", f"${total:.2f}"]
    ]

    summary_table = Table(summary_data, colWidths=[320, 100])
    summary_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 7),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
    ]))
    elements.append(summary_table)
    elements.append(Spacer(1, 12))

    # Add Footer
    footer = Paragraph("Thank you for your business!", ParagraphStyle(name='FooterStyle', fontSize=10, fontName='Helvetica'))
    elements.append(footer)

    # Build the PDF
    pdf.build(elements)
    print(f"Invoice generated: {file_path}")