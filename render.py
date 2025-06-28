import reportlab.pdfgen.canvas as canvas
from reportlab.lib.units import inch
import reportlab.platypus as platypus
import datetime
import locale

import constants


def drawText(
    c: canvas.Canvas,
    text: str,
    x: float,
    y: float,
    font_size: int = 12,
    font: str = "Helvetica",
) -> None:
    c.setFont("Helvetica", font_size)
    c.drawString(x, y, text)


def drawCentredText(
    c: canvas.Canvas,
    text: str,
    x: float,
    y: float,
    font_size: int = 12,
    font: str = "Helvetica",
) -> None:
    c.setFont("Helvetica", font_size)
    c.drawCentredString(x, y, text)


def drawCompanyInformation(
    c: canvas.Canvas, COMPANY: str, ADRESS: str, POSTAL_CODE: str, CITY: str, PHONE_NUMBER: str
) -> None:
    # Create the company information table
    table_data = [
        [COMPANY],
        [ADRESS],
        [f"{POSTAL_CODE} {CITY}"],
        [f"Tel: {PHONE_NUMBER}"],
    ]

    table_style = platypus.TableStyle(
        [("FONTSIZE", (0, 0), (0, 0), 16), ("BOTTOMPADDING", (0, 0), (0, 0), 10)]
    )

    table = platypus.Table(
        table_data, style=table_style
    )
    table.wrapOn(c, constants.LEFT, 8 * inch)
    table.drawOn(c, constants.LEFT, 8 * inch)


def drawClientInformation(
    c: canvas.Canvas, CLIENT: str, ADRESS: str, POSTAL_CODE: str, CITY: str
) -> None:
    # Create the client information table
    table_data = [
        [CLIENT],
        [ADRESS],
        [f"{POSTAL_CODE} {CITY}"],
    ]

    table = platypus.Table(table_data)
    table.wrapOn(c, constants.RIGHT, constants.HEIGHT)
    table.drawOn(c, constants.RIGHT, 8 * inch)


def drawPaymentInformation(
    c: canvas.Canvas,
    invoice_total: str,
    COMPANY: str,
    COMPANY_ADDRESS: str,
    CEO: str,
    BANK: str,
    COMPANY_POSTAL_CODE: str,
    COMPANY_CITY: str,
    COMPANY_PHONE_NUMBER: str,
    ACCOUNT_NUMBER: str,
    COMPANY_ORGANIZATION_NUMBER: str,
    EMAIL: str,
    IBAN: str,
    BIC: str,
    invoice_number: str,
    CLIENT_NUMBER: str,
    CLIENT_REFERENCE: str,
    CLIENT_ORGANIZATION_NUMBER: str,
    PAYMENT_DAYS: int,
) -> None:
    invoice_date = datetime.date.today()
    locale.setlocale(locale.LC_ALL, 'sv_SE')
    expiration_date = invoice_date + datetime.timedelta(days=PAYMENT_DAYS)

    table_data = [
        ["Att betala SEK", invoice_total, ""],
        ["Förfallodatum", expiration_date, ""],
        ["Referensnummer/OCR", f"{invoice_date.strftime("%Y%m")}{invoice_number}", ""],
        [COMPANY, "", "Betalningsinformation"],
        [COMPANY_ADDRESS, CEO, f"Bank: {BANK}"],
        [
            f"{COMPANY_POSTAL_CODE} {COMPANY_CITY}",
            f"Tel: {COMPANY_PHONE_NUMBER}",
            f"Kontonummer: {ACCOUNT_NUMBER}",
        ],
        [f"Org. nummer: {COMPANY_ORGANIZATION_NUMBER}", EMAIL, f"IBAN: {IBAN}"],
        ["Godkänd för F-skatt", "", f"SWIFT/BIC: {BIC}"],
        ["Fakturadatum", str(invoice_date), ""],
        ["Kundnummer", f"{CLIENT_NUMBER}", ""],
        ["Er referens", f"{CLIENT_REFERENCE}", ""],
        ["Kundens org. nummer", f"{CLIENT_ORGANIZATION_NUMBER}", ""],
        ["Fakturanummer", f"{invoice_date.strftime("%Y%m")}-{invoice_number}", ""],
        ["Betalningsvillkor", f"{PAYMENT_DAYS} dagar", ""],
        ["Vid utebliven betalning tar vi ut dröjsmålsränta\nenligt räntelagen ochbetalningspåminnelseavgift\neller förseningsersättning.", "", ""],
        ["Tjänsterna utförda", invoice_date.strftime("%B").capitalize(), ""],
    ]
    
    table_style = platypus.TableStyle(
        [
            # Body
            ("BOX", (0, 0), (-1, -1), 0.5, (0, 0, 0)),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 12),
            ("FONTSIZE", (0, 14), (0, 14), 9),
        ]
    )
    
    table = platypus.Table(table_data, style=table_style)
    table.wrapOn(c, constants.LEFT, 1 * inch)
    table.drawOn(c, constants.LEFT, 3.5 * inch)


def drawInvoiceItems(c: canvas.Canvas, data: list[str]) -> None:
    # Create the invoice table
    table_data = [
        ["Tjänst", "Beskrivning", "Antal", "Á-pris", "Belopp"],
        *[list(row.values()) for row in data],
    ]

    table_style = platypus.TableStyle(
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

    table = platypus.Table(table_data, style=table_style)
    table.wrapOn(c, constants.LEFT, 1 * inch)
    table.drawOn(c, constants.LEFT, 2.5 * inch)
