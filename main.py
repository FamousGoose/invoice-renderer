import csv
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.platypus import TableStyle, Table
from jproperties import Properties


import render

COMPANY_KEY = "COMPANY"
ADRESS_KEY = "ADRESS"
POSTAL_CODE_KEY = "POSTAL_CODE"
CITY_KEY = "CITY"
PHONE_NUMBER_KEY = "PHONE_NUMBER"

WIDHT = 8.27 * inch
HEIGHT = 11.69 * inch

LEFT = 1 * inch


def main():
    config = Properties()
    with open("invoice.properties", "rb") as config_file:
        config.load(config_file)

    COMPANY = config.get(COMPANY_KEY).data
    ADRESS = config.get(ADRESS_KEY).data
    POSTAL_CODE = config.get(POSTAL_CODE_KEY).data
    CITY = config.get(CITY_KEY).data
    PHONE_NUMBER = config.get(PHONE_NUMBER_KEY).data
    # Set up the PDF file
    c = canvas.Canvas("invoice.pdf", pagesize=letter)

    # Set up the font and font size
    c.setFont("Helvetica", 12)

    # Read the CSV file
    with open("sample_invoice_data.csv", "r") as csvfile:
        reader = csv.DictReader(
            csvfile,
            fieldnames=["Tjänst", "Beskrivning", "Antal", "Á-pris", "Belopp"],
            delimiter=";",
        )
        data = [row for row in reader]

    # Remove the header
    data = data[1:]

    # Create the invoice header
    render.drawCentredText(c, "Faktura", WIDHT / 2, 10 * inch, 24)

    # Create the company information table
    company_information_header_data = [
        [COMPANY],
        [ADRESS],
        [f"{POSTAL_CODE} {CITY}"],
        [f"Tel: {PHONE_NUMBER}"],
    ]

    company_information_header_style = TableStyle(
        [("FONTSIZE", (0, 0), (0, 0), 16), ("BOTTOMPADDING", (0, 0), (0, 0), 10)]
    )

    company_information_header = Table(
        company_information_header_data, style=company_information_header_style
    )
    company_information_header.wrapOn(c, LEFT, 8 * inch)
    company_information_header.drawOn(c, LEFT, 8 * inch)

    # Create the invoice table
    invoice_items_data = [
        ["Tjänst", "Beskrivning", "Antal", "Á-pris", "Belopp"],
        *[list(row.values()) for row in data],
    ]

    table_style = TableStyle(
        [
            # Header
            ("GRID", (0, 0), (4, 0), 0.5, (0, 0, 0)),
            ("TEXTCOLOR", (0, 0), (4, 0), (1, 1, 1)),  # text color (blue)
            ("BACKGROUND", (0, 0), (4, 0), (0, 0, 0)),  # background color (light gray)
            # Body
            ("BOX", (0, 0), (-1, -1), 0.5, (0, 0, 0)),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 12),
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ]
    )

    table = Table(invoice_items_data, style=table_style)
    table.wrapOn(c, LEFT, 1 * inch)
    table.drawOn(c, LEFT, 7 * inch)

    # Create the invoice footer
    total = sum(float(row["Belopp"].replace(",", ".")) for row in data)
    c.drawString(6 * inch, 1 * inch, "Totalt: " + str(total))

    # Save the PDF file
    c.save()


if __name__ == "__main__":
    main()
