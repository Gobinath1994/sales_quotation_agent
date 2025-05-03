import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak

def create_pdf(quote_id, customer, brand, model, price, quote_text):
    output_dir = "quotes"
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, f"quote_{quote_id}.pdf")

    doc = SimpleDocTemplate(file_path, pagesize=A4)
    styles = getSampleStyleSheet()
    body_style = ParagraphStyle(name="Body", parent=styles["Normal"], leading=16, fontSize=11)

    flowables = []
    flowables.append(Paragraph(f"<b>Quote ID:</b> {quote_id}", styles["Normal"]))
    flowables.append(Paragraph(f"<b>Customer:</b> {customer}", styles["Normal"]))
    flowables.append(Paragraph(f"<b>Brand:</b> {brand} - <b>Model:</b> {model}", styles["Normal"]))
    flowables.append(Paragraph(f"<b>Price:</b> ${price:,.2f}", styles["Normal"]))
    flowables.append(Paragraph(f"<b>Date:</b> {datetime.now().strftime('%Y-%m-%d')}", styles["Normal"]))
    flowables.append(Spacer(1, 20))

    # Wrap long paragraphs properly
    for line in quote_text.strip().split("\n"):
        if line.strip() == "":
            flowables.append(Spacer(1, 10))
        else:
            flowables.append(Paragraph(line.strip(), body_style))

    flowables.append(PageBreak())

    doc.build(flowables)
    return file_path