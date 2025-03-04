from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def get_styles():
    styles = getSampleStyleSheet()
    item_style = ParagraphStyle(name='ItemStyle', alignment=0, fontName='Helvetica', fontSize=8)  # Left-justified, Helvetica, size 8
    cell_style = ParagraphStyle(name='CellStyle', alignment=1, fontName='Helvetica', fontSize=8)  # Centered, Helvetica, size 8
    header_style = ParagraphStyle(name='HeaderStyle', alignment=1, fontName='Helvetica-Bold', fontSize=10, textColor=colors.black)  # Centered, Helvetica-Bold, size 10, black text
    return styles, item_style, cell_style, header_style

def get_table_style():
    return [
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, 0), 8),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('LEFTPADDING', (0, 0), (0, -1), 10),
        ('INNERGRID', (0, 0), (-1, -1), 0, colors.white),  # Remove inner grid
        ('BOX', (0, 0), (-1, -1), 0, colors.white),  # Remove outer box
    ]